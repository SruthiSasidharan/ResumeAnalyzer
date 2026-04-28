"""
Module 5: Job Recommendation - Based on predicted role.
Prefers live Adzuna API when configured;
Falls back to RemoteOK (free, no credentials), then DB, then static fallback.
"""
from django.apps import apps

from .job_api_client import adzuna_configured, fetch_adzuna_jobs, fetch_remoteok_jobs, role_key_to_search_query
from .datasets import FALLBACK_JOBS


class JobRecommender:
    """Recommend jobs based on predicted role."""

    def recommend(self, role_slug: str = None, role_name: str = None, limit: int = 10) -> list:
        """Get job listings: Adzuna first, then RemoteOK, then DB, then curated fallback."""
        role_key = (role_slug or role_name or "").strip()
        query = role_key_to_search_query(role_key)

        # Try Adzuna if configured
        if adzuna_configured():
            live = fetch_adzuna_jobs(query, limit=limit)
            if live:
                return live[:limit]
        
        # Fallback to RemoteOK (free API, no credentials required)
        remote_jobs = fetch_remoteok_jobs(query, limit=limit)
        if remote_jobs:
            return remote_jobs[:limit]

        # Try database jobs
        jobs = self._from_db(role_key, limit)
        if not jobs and role_key:
            # Last resort: static fallback dataset
            jobs = self._fallback_jobs(role_key, limit)
        return jobs[:limit]

    def _from_db(self, role: str, limit: int) -> list:
        try:
            JobListing = apps.get_model('career_app', 'JobListing')
            qs = JobListing.objects.filter(is_active=True)
            if role:
                qs = qs.filter(role_slug__icontains=role.replace(" ", "-"))
            return [
                {
                    "title": j.title,
                    "company": j.company,
                    "location": j.location,
                    "url": j.url,
                    "skills": j.skills_required,
                }
                for j in qs[:limit]
            ]
        except Exception:
            return []

    def _fallback_jobs(self, role: str, limit: int) -> list:
        """Fallback curated job dataset when DB/API has no data."""
        slug = (role or "").lower().replace(" ", "-")
        filtered = [j for j in FALLBACK_JOBS if slug in j["title"].lower().replace(" ", "-") or slug in j["company"].lower()]
        if not filtered:
            filtered = FALLBACK_JOBS
        return filtered[:limit]
