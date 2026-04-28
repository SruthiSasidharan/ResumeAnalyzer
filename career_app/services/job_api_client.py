"""
Live job listings via Adzuna Jobs API (https://developer.adzuna.com/) and
RemoteOK public API (https://remoteok.com/api — no credentials required).
Set ADZUNA_APP_ID and ADZUNA_APP_KEY in environment for Adzuna support.
"""
from __future__ import annotations

import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import List

from django.conf import settings

# Map internal role slugs to search keywords (Adzuna "what" parameter)
ROLE_SLUG_TO_QUERY = {
    "data-scientist": "data scientist",
    "frontend-developer": "frontend developer",
    "backend-developer": "backend developer",
    "fullstack-developer": "full stack developer",
    "ml-engineer": "machine learning engineer",
    "devops-engineer": "devops engineer",
    "data-analyst": "data analyst",
    "software-engineer": "software engineer",
    "cloud-architect": "cloud architect",
    "cybersecurity-engineer": "cybersecurity engineer",
    "android-developer": "android developer",
    "ios-developer": "ios developer",
}

# RemoteOK tag keywords per role slug — used to filter remote jobs by relevance
_ROLE_SLUG_TO_TAGS = {
    "data-scientist": ["python", "machine-learning", "data-science", "r", "tensorflow", "statistics"],
    "frontend-developer": ["react", "javascript", "typescript", "frontend", "vue", "angular", "html", "css"],
    "backend-developer": ["python", "java", "nodejs", "backend", "api", "django", "flask", "ruby"],
    "fullstack-developer": ["fullstack", "react", "node", "javascript", "python", "rails"],
    "ml-engineer": ["machine-learning", "python", "tensorflow", "pytorch", "ai", "deep-learning", "nlp"],
    "devops-engineer": ["devops", "docker", "kubernetes", "aws", "cicd", "linux", "terraform"],
    "data-analyst": ["sql", "python", "data-analysis", "analytics", "tableau", "excel"],
    "software-engineer": ["python", "java", "javascript", "software-engineer", "backend", "golang"],
    "cloud-architect": ["aws", "azure", "gcp", "cloud", "kubernetes", "terraform"],
    "cybersecurity-engineer": ["security", "cybersecurity", "penetration-testing", "compliance"],
    "android-developer": ["android", "kotlin", "java", "mobile"],
    "ios-developer": ["ios", "swift", "objective-c", "mobile", "xcode"],
}

# Module-level cache for RemoteOK response (avoids hammering the API)
_remoteok_cache: dict = {"data": [], "fetched_at": 0.0}
REMOTEOK_CACHE_TTL = 1800  # 30 minutes


def role_key_to_search_query(role_key: str) -> str:
    """Turn slug or free text into an Adzuna search string."""
    if not role_key or not role_key.strip():
        return "software developer"
    k = role_key.strip().lower().replace(" ", "-")
    if k in ROLE_SLUG_TO_QUERY:
        return ROLE_SLUG_TO_QUERY[k]
    return role_key.strip().replace("-", " ")


def adzuna_configured() -> bool:
    app_id = getattr(settings, "ADZUNA_APP_ID", "") or ""
    app_key = getattr(settings, "ADZUNA_APP_KEY", "") or ""
    return bool(app_id.strip() and app_key.strip())


def fetch_adzuna_jobs(keywords: str, limit: int = 20) -> List[dict]:
    """
    Return normalized job dicts: title, company, location, url, skills (list), source.
    Empty list if API keys missing or request fails.
    """
    if not adzuna_configured():
        # Debug: log that API not configured
        import sys
        print("⚠️  Adzuna API not configured. Set ADZUNA_APP_ID and ADZUNA_APP_KEY environment variables.", file=sys.stderr)
        return []

    app_id = settings.ADZUNA_APP_ID.strip()
    app_key = settings.ADZUNA_APP_KEY.strip()
    country = (getattr(settings, "ADZUNA_COUNTRY", "in") or "in").strip().lower()

    base = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": str(min(max(limit, 1), 50)),
        "what": keywords,
    }
    url = f"{base}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "CareerGuidance/1.0 (Django)"})

    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=20, context=ctx) as response:
            raw = response.read().decode()
        data = json.loads(raw)
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, OSError) as e:
        import sys
        print(f"❌ Adzuna API Error: {str(e)}", file=sys.stderr)
        return []

    out: List[dict] = []
    for item in data.get("results", [])[:limit]:
        company = item.get("company") or {}
        loc = item.get("location") or {}
        if isinstance(company, dict):
            company_name = company.get("display_name", "") or ""
        else:
            company_name = str(company)
        if isinstance(loc, dict):
            location = loc.get("display_name", "") or ""
        else:
            location = str(loc)

        redirect_url = (item.get("redirect_url") or item.get("url") or "").strip()
        if not redirect_url:
            continue

        out.append(
            {
                "title": (item.get("title") or "Job")[:200],
                "company": company_name[:200] if company_name else "Company",
                "location": location[:200] if location else "",
                "url": redirect_url,
                "skills": [],
                "source": "adzuna",
            }
        )
    return out


def fetch_remoteok_jobs(keywords: str, limit: int = 20) -> List[dict]:
    """
    Fetch remote jobs from RemoteOK API (no authentication required).
    Returns normalized job dicts: title, company, location, url, skills, source.
    """
    global _remoteok_cache
    current_time = time.time()
    
    # Use cache if available and fresh
    if _remoteok_cache["data"] and (current_time - _remoteok_cache["fetched_at"]) < REMOTEOK_CACHE_TTL:
        jobs = _remoteok_cache["data"]
    else:
        # Fetch fresh data
        url = "https://remoteok.com/api"
        req = urllib.request.Request(url, headers={"User-Agent": "CareerGuidance/1.0"})
        
        try:
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
                raw = response.read().decode()
            data = json.loads(raw)
            _remoteok_cache["data"] = data
            _remoteok_cache["fetched_at"] = current_time
            jobs = data
        except Exception as e:
            import sys
            print(f"⚠️  RemoteOK API Error: {str(e)}", file=sys.stderr)
            return []
    
    # Filter jobs by keywords and return up to limit
    out: List[dict] = []
    keywords_lower = keywords.lower().split()
    
    for job in jobs:
        if len(out) >= limit:
            break
        
        # Skip metadata items (first item usually has 'legal' or missing title)
        if not isinstance(job, dict) or ('legal' in job and 'title' not in job):
            continue
        
        # Get job title and company
        title = (job.get("title") or job.get("position") or "").strip().lower()
        company = (job.get("company") or "").strip()
        
        # If no title, try slug field
        if not title:
            slug = job.get("slug", "")
            if slug:
                title = slug.replace("-", " ").lower()
            else:
                continue
        
        # Extract tags/skills
        tags = job.get("tags", []) or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]
        tags_lower = [t.lower() for t in tags]
        
        # Match keywords in title or tags
        matches = any(kw in title for kw in keywords_lower) or any(kw in " ".join(tags_lower) for kw in keywords_lower)
        if not matches:
            continue
        
        url = job.get("url") or job.get("redirect_url") or ""
        if not url:
            continue
        
        # Format title properly
        title_display = title.title() if title else "Remote Job"
        
        out.append({
            "title": title_display[:200],
            "company": company[:200] if company else "Remote Company",
            "location": "Remote",
            "url": url,
            "skills": [t for t in tags if t and len(t) > 1][:8],
            "source": "remoteok",
        })
    
    return out
