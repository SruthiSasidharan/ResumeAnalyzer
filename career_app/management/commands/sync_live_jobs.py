"""
Pull live jobs from Adzuna into JobListing (optional cache for offline / faster pages).

Requires ADZUNA_APP_ID and ADZUNA_APP_KEY.

  python manage.py sync_live_jobs --all-roles --limit 10
  python manage.py sync_live_jobs --role data-scientist --limit 20
"""
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from career_app.services.job_api_client import adzuna_configured, fetch_adzuna_jobs, role_key_to_search_query


class Command(BaseCommand):
    help = "Fetch jobs from Adzuna and upsert into JobListing"

    def add_arguments(self, parser):
        parser.add_argument("--role", type=str, default="", help="Role slug or search text")
        parser.add_argument("--limit", type=int, default=15)
        parser.add_argument(
            "--all-roles",
            action="store_true",
            help="Sync for every CareerRole in the database",
        )

    def handle(self, *args, **options):
        if not adzuna_configured():
            raise CommandError(
                "Set ADZUNA_APP_ID and ADZUNA_APP_KEY (see .env.example and developer.adzuna.com)."
            )

        JobListing = apps.get_model("career_app", "JobListing")
        CareerRole = apps.get_model("career_app", "CareerRole")
        limit = max(1, min(options["limit"], 50))
        total = 0

        if options["all_roles"]:
            roles = list(CareerRole.objects.all().values_list("slug", flat=True))
            if not roles:
                self.stdout.write(self.style.WARNING("No CareerRole rows; run load_dataset first."))
            for slug in roles:
                total += self._upsert_for_slug(JobListing, slug, limit)
        elif options["role"]:
            total += self._upsert_for_slug(JobListing, options["role"], limit)
        else:
            raise CommandError("Pass --role <slug-or-text> or --all-roles")

        self.stdout.write(self.style.SUCCESS(f"Upserted {total} job listing(s)."))

    def _upsert_for_slug(self, JobListing, role_key: str, limit: int) -> int:
        query = role_key_to_search_query(role_key)
        slug_norm = role_key.strip().lower().replace(" ", "-")
        jobs = fetch_adzuna_jobs(query, limit=limit)
        n = 0
        for j in jobs:
            url = j.get("url") or ""
            if not url:
                continue
            JobListing.objects.update_or_create(
                url=url[:512],
                defaults={
                    "title": j["title"][:200],
                    "company": j["company"][:200],
                    "location": (j.get("location") or "")[:200],
                    "role_slug": slug_norm[:100],
                    "skills_required": j.get("skills") or [],
                    "is_active": True,
                },
            )
            n += 1
        self.stdout.write(f"  {slug_norm!r} ({query!r}): {n} jobs")
        return n
