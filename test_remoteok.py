#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_guidance.settings')
django.setup()

from career_app.services.job_api_client import fetch_remoteok_jobs

print("=" * 60)
print("TESTING REMOTEOK API DIRECTLY")
print("=" * 60)

# Test RemoteOK API
print("\n🔍 Fetching remote jobs for 'python developer'...")
jobs = fetch_remoteok_jobs("python developer", limit=5)

if jobs:
    print(f"\n✅ SUCCESS! Found {len(jobs)} remote jobs:")
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        if job['skills']:
            print(f"   Tags: {', '.join(job['skills'])}")
        print(f"   Source: {job['source']}")
else:
    print("\n❌ No jobs found from RemoteOK")
    print("   This could be:")
    print("   - RemoteOK API is temporarily down")
    print("   - Network connectivity issue")
    print("   - No matching jobs for the search query")

print("\n" + "=" * 60)
