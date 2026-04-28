#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_guidance.settings')
django.setup()

from career_app.services.job_recommender import JobRecommender
from career_app.services.job_api_client import adzuna_configured

print("=" * 60)
print("TESTING JOB SEARCH FUNCTIONALITY")
print("=" * 60)

# Check Adzuna config
print(f"\n📋 Adzuna Configured: {adzuna_configured()}")
print("   (If False, will use RemoteOK as fallback)")

recommender = JobRecommender()

# Test 1: Backend Developer
print("\n✓ Testing Backend Developer role...")
jobs = recommender.recommend(role_slug="backend-developer", limit=3)
if jobs:
    print(f"  Found {len(jobs)} jobs:")
    for i, job in enumerate(jobs[:2], 1):
        print(f"  {i}. {job['title']}")
        print(f"     {job['company']} | {job['location']}")
        print(f"     Source: {job.get('source', 'unknown')}")
else:
    print("  ⚠️  No jobs found (RemoteOK may be rate-limited)")

# Test 2: Python Developer
print("\n✓ Testing Python Developer role...")
jobs = recommender.recommend(role_name="python developer", limit=2)
if jobs:
    print(f"  Found {len(jobs)} jobs")
    print(f"  Source: {jobs[0].get('source', 'unknown')}")
else:
    print("  ⚠️  No jobs found")

print("\n" + "=" * 60)
print("✅ Job Search Tests Complete!")
print("=" * 60)
