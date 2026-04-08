"""
Live job listings via Adzuna Jobs API (https://developer.adzuna.com/).
Set ADZUNA_APP_ID and ADZUNA_APP_KEY in environment or Django settings.
"""
from __future__ import annotations

import json
import ssl
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
}


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
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, OSError):
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
