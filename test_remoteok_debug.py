#!/usr/bin/env python
import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request

print("=" * 60)
print("DEBUG: REMOTEOK RAW API TEST")
print("=" * 60)

url = "https://remoteok.com/api"
req = urllib.request.Request(url, headers={"User-Agent": "CareerGuidance/1.0"})

try:
    ctx = ssl.create_default_context()
    print(f"\n📡 Fetching from: {url}")
    with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
        raw = response.read().decode()
    data = json.loads(raw)
    
    print(f"✅ API Response received!")
    print(f"   Total jobs: {len(data)}")
    
    # Show first 3 jobs
    if data:
        print(f"\n📋 First 3 jobs from API:")
        for i, job in enumerate(data[:3], 1):
            print(f"\n{i}. Title: {job.get('title', 'N/A')}")
            print(f"   Company: {job.get('company', job.get('name', 'N/A'))}")
            print(f"   Tags: {job.get('tags', [])}")
    
    # Show sample job structure
    if data:
        print(f"\n🔍 Sample job structure:")
        print(json.dumps(data[0], indent=2)[:500])
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {str(e)}")
    print("\n   Possible issues:")
    print("   - Network connectivity problem")
    print("   - RemoteOK API is down")
    print("   - SSL certificate issue")

print("\n" + "=" * 60)
