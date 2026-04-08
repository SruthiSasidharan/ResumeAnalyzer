"""
Module 5: Job Recommendation - Based on predicted role.
Prefers live Adzuna API when ADZUNA_APP_ID and ADZUNA_APP_KEY are set;
otherwise uses JobListing rows from the DB, then static fallback.
"""
from django.apps import apps

from .job_api_client import adzuna_configured, fetch_adzuna_jobs, role_key_to_search_query


class JobRecommender:
    """Recommend jobs based on predicted role."""

    def recommend(self, role_slug: str = None, role_name: str = None, limit: int = 10) -> list:
        """Get job listings: live API first, then DB, then curated fallback."""
        role_key = (role_slug or role_name or "").strip()
        query = role_key_to_search_query(role_key)

        if adzuna_configured():
            live = fetch_adzuna_jobs(query, limit=limit)
            if live:
                return live[:limit]

        jobs = self._from_db(role_key, limit)
        if not jobs and role_key:
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
        all_jobs = [
            {"title": "Data Scientist", "company": "TechCorp", "location": "Remote", "url": "https://example.com/job1", "skills": ["Python", "ML", "SQL"]},
            {"title": "Senior Data Scientist", "company": "DataInc", "location": "Bangalore, India", "url": "https://example.com/job2", "skills": ["Python", "TensorFlow", "NLP"]},
            {"title": "Frontend Developer", "company": "WebWorks", "location": "Hyderabad", "url": "https://example.com/job3", "skills": ["React", "JavaScript", "CSS"]},
            {"title": "Full Stack Developer", "company": "StartupX", "location": "Remote", "url": "https://example.com/job4", "skills": ["Node.js", "React", "MongoDB"]},
            {"title": "Backend Engineer", "company": "APILabs", "location": "Chennai", "url": "https://example.com/job5", "skills": ["Python", "Django", "PostgreSQL"]},
            {"title": "ML Engineer", "company": "AIM Labs", "location": "Mumbai", "url": "https://example.com/job6", "skills": ["PyTorch", "TensorFlow", "Python"]},
            {"title": "DevOps Engineer", "company": "CloudTech", "location": "Pune", "url": "https://example.com/job7", "skills": ["AWS", "Docker", "Kubernetes"]},
            {"title": "Data Analyst", "company": "AnalyticsPro", "location": "Delhi", "url": "https://example.com/job8", "skills": ["SQL", "Python", "Tableau"]},
        ]
        filtered = [j for j in all_jobs if slug in j["title"].lower().replace(" ", "-") or slug in j["company"].lower()]
        if not filtered:
            filtered = all_jobs
        return filtered[:limit]
