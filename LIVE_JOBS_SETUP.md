# Live Job Search Setup Guide

## Current Status

The application now supports **two ways** to fetch live job listings:

### ✅ RemoteOK API (WORKS NOW - No Setup Needed)
- **Status**: Enabled and working by default
- **Source**: Free remote job listings from RemoteOK
- **Setup**: No credentials required!
- **Fallback**: Used automatically when Adzuna is not configured

### 🔧 Adzuna API (Optional - Better Results)
- **Status**: Can be enabled with credentials
- **Source**: Comprehensive job listings (Adzuna)
- **Setup**: Requires API credentials
- **Priority**: Used first if configured

---

## How It Works (Priority Order)

1. **Adzuna API** (if configured with credentials) → Comprehensive job listings
2. **RemoteOK API** (free, no setup) → Remote job listings
3. **Database** (if jobs manually added) → Local job listings
4. **Fallback Dataset** → Pre-loaded sample jobs

---

## Setup Adzuna API (Optional - For Better Results)

### Step 1: Get API Credentials
1. Go to https://developer.adzuna.com/signup
2. Sign up for a free developer account
3. Go to your dashboard and get your:
   - `APP_ID`
   - `APP_KEY`

### Step 2: Set Environment Variables

Create or edit `.env` file in the project root:

```bash
ADZUNA_APP_ID=your_app_id_here
ADZUNA_APP_KEY=your_app_key_here
ADZUNA_COUNTRY=in
```

**Or set environment variables via command line:**

**Windows (PowerShell):**
```powershell
$env:ADZUNA_APP_ID = "your_app_id_here"
$env:ADZUNA_APP_KEY = "your_app_key_here"
$env:ADZUNA_COUNTRY = "in"
```

**Windows (CMD):**
```cmd
set ADZUNA_APP_ID=your_app_id_here
set ADZUNA_APP_KEY=your_app_key_here
set ADZUNA_COUNTRY=in
```

**Linux/Mac:**
```bash
export ADZUNA_APP_ID="your_app_id_here"
export ADZUNA_APP_KEY="your_app_key_here"
export ADZUNA_COUNTRY="in"
```

### Step 3: Restart Django Server
```bash
python manage.py runserver
```

### Supported Countries
- `in` - India
- `gb` - United Kingdom
- `us` - United States
- `au` - Australia
- `ca` - Canada
- `de` - Germany
- `fr` - France
- `etc...` - See Adzuna docs for full list

---

## Testing Live Job Search

### Via Web Interface
1. Upload a resume
2. Get career analysis results
3. Check "Recommended Jobs" section - should show remote jobs from RemoteOK

### Via Django Shell
```python
python manage.py shell

from career_app.services.job_recommender import JobRecommender

recommender = JobRecommender()

# Test with a role
jobs = recommender.recommend(role_slug="backend-developer", limit=5)
for job in jobs:
    print(f"✓ {job['title']} at {job['company']}")
    print(f"  Location: {job['location']}")
    print(f"  Source: {job['source']}")
    print()
```

---

## Troubleshooting

### "No live jobs showing"
1. **Check RemoteOK API**: Should work by default
   - If RemoteOK fails, check console for error messages
   - May be rate-limited or API down temporarily

2. **If using Adzuna**:
   - Verify API credentials are correct
   - Check that `.env` file exists or env vars are set
   - Restart Django server after setting env vars
   - Check error logs in console

3. **Test API connectivity**:
   ```python
   python manage.py shell
   
   from career_app.services.job_api_client import adzuna_configured, fetch_adzuna_jobs, fetch_remoteok_jobs
   
   # Check Adzuna config
   print(f"Adzuna configured: {adzuna_configured()}")
   
   # Test RemoteOK
   jobs = fetch_remoteok_jobs("python developer", limit=3)
   print(f"RemoteOK jobs found: {len(jobs)}")
   
   # Test Adzuna (if configured)
   if adzuna_configured():
       jobs = fetch_adzuna_jobs("python developer", limit=3)
       print(f"Adzuna jobs found: {len(jobs)}")
   ```

### API Rate Limiting
- **RemoteOK**: Caches results for 30 minutes to avoid rate limiting
- **Adzuna**: May have request limits based on your plan

### Network Issues
- Ensure your system can access external APIs
- Check firewall/proxy settings if behind corporate network
- Try VPN if connection is blocked by ISP

---

## API Documentation

- **RemoteOK API**: https://remoteok.com/api
- **Adzuna API**: https://developer.adzuna.com/docs

---

## What to Do Next

### If RemoteOK Works (Default):
✅ Nothing needed! Job search is working.

### To Improve Results:
1. Register with Adzuna for comprehensive job listings
2. Set up API credentials (see Step 1-3 above)
3. Restart Django server
4. Now you'll get Adzuna jobs in addition to RemoteOK
