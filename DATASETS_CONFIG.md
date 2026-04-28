# Dataset Configuration Guide

All hardcoded datasets have been centralized in [`career_app/services/datasets.py`](career_app/services/datasets.py) for easy configuration.

## Overview

The configuration system is now organized into 4 main sections:

### 1. **Resume Analyzer Datasets**
Located in `datasets.py`, these control what skills and education patterns are recognized in resumes.

#### Configurable Items:
- **`SKILL_KEYWORDS`** - List of technical and professional skills to extract
  - Programming languages, frameworks, tools, certifications
  - Current tech stack (2024-2025)
  
- **`EDUCATION_PATTERNS`** - Regex patterns for detecting education qualifications
  - B.Tech, M.Tech, Bachelor's, Master's, PhD, Diploma degrees
  
- **`EXPERIENCE_PATTERNS`** - Regex patterns for detecting work experience
  - Job titles, company names, employment duration

#### How to Update:
Edit the lists directly in `datasets.py`:

```python
SKILL_KEYWORDS = [
    "Python", "Java", "JavaScript", 
    # Add your skills here
]

EDUCATION_PATTERNS = [
    r'(?i)(?:b\.?tech|...)',  # Add regex patterns
]

EXPERIENCE_PATTERNS = [
    r'(?i)(?:worked|...',  # Add regex patterns
]
```

---

### 2. **Career Prediction Datasets**
Defines available career roles and their required/optional skills.

#### Configurable Item:
- **`CAREER_ROLES`** - List of job roles with skill requirements
  - Each role has: name, slug, required_skills, optional_skills
  - Current roles: Data Scientist, Backend Developer, Frontend Developer, etc.

#### How to Update:
Add or modify roles in `CAREER_ROLES` list:

```python
CAREER_ROLES = [
    {
        "name": "Your New Role",
        "slug": "your-new-role",
        "required_skills": ["Skill1", "Skill2", ...],
        "optional_skills": ["Skill3", "Skill4", ...],
    },
    # ... more roles
]
```

---

### 3. **Job Recommendation Datasets**
Fallback job listings when API/Database don't have data.

#### Configurable Item:
- **`FALLBACK_JOBS`** - List of job postings with details
  - Each job has: title, company, location, url, skills

#### How to Update:
Edit the `FALLBACK_JOBS` list:

```python
FALLBACK_JOBS = [
    {
        "title": "Senior Data Scientist",
        "company": "Tech Company",
        "location": "Remote",
        "url": "https://careers.example.com/job123",
        "skills": ["Python", "ML", "SQL"],
    },
    # ... more jobs
]
```

---

### 4. **Learning Recommendation Datasets**
Courses, certifications, and resources for skill development.

#### Configurable Items:

**`LEARNING_PATHS`** - Structured learning roadmaps for each career role
```python
LEARNING_PATHS = {
    "data-scientist": [
        {"course": "Python Fundamentals", "duration": "2 weeks", "priority": "high"},
        # ... more courses
    ],
}
```

**`LEARNING_RESOURCES`** - Detailed resources (courses, books, YouTube, certifications) for each skill
```python
LEARNING_RESOURCES = {
    "Python": {
        "courses": ["Course 1", "Course 2"],
        "certifications": ["PCEP"],
        "youtube": ["Channel 1", "Channel 2"],
        "books": ["Book 1"],
    },
}
```

---

## Usage in Services

Each service module imports its datasets:

### Resume Analyzer (`resume_analyzer.py`)
```python
from .datasets import SKILL_KEYWORDS, EDUCATION_PATTERNS, EXPERIENCE_PATTERNS
```

### Career Predictor (`career_predictor.py`)
```python
from .datasets import CAREER_ROLES
```

### Job Recommender (`job_recommender.py`)
```python
from .datasets import FALLBACK_JOBS
```

### Learning Recommender (`learning_recommender.py`)
```python
from .datasets import LEARNING_RESOURCES
```

---

## Data Priority/Fallback Chain

### 1. Resume Analysis
1. Extract from resume using configured `SKILL_KEYWORDS`
2. Use `EDUCATION_PATTERNS` to find education
3. Use `EXPERIENCE_PATTERNS` to find work experience

### 2. Career Prediction
1. Check Django database (`CareerRole` model)
2. Fall back to `CAREER_ROLES` in `datasets.py`

### 3. Job Recommendations
1. Use Adzuna API (if ADZUNA_APP_ID and ADZUNA_APP_KEY env vars set)
2. Check Django database (`JobListing` model)
3. Fall back to `FALLBACK_JOBS` in `datasets.py`

### 4. Learning Resources
1. Check Django database (`LearningResource` model)
2. Fall back to `LEARNING_RESOURCES` in `datasets.py`

---

## Best Practices

1. **Keep datasets.py organized** - Use clear section headers and comments
2. **Version control** - Track changes to dataset configurations
3. **Duplicate skills** - Avoid duplicate skill names (case-sensitive)
4. **Slug consistency** - Use lowercase + hyphens for role slugs (e.g., "data-scientist")
5. **Database first** - Always populate the Django database for production (datasets.py is fallback)
6. **Test changes** - After updating datasets, test resume analysis and job recommendations

---

## Database vs Configuration File

| Source | Use Case | Priority |
|--------|----------|----------|
| Django Database | Production data, user-specific customizations | 1st (Highest) |
| datasets.py | Default fallback, development, quick testing | 2nd |
| API (Adzuna) | Real-time job listings | 1st for jobs |

---

## Example: Adding a New Career Role

**File:** `career_app/services/datasets.py`

```python
CAREER_ROLES = [
    # ... existing roles ...
    {
        "name": "Cloud Architect",
        "slug": "cloud-architect",
        "required_skills": ["AWS", "Azure", "Docker", "Kubernetes", "Networking"],
        "optional_skills": ["Terraform", "CI/CD", "Linux", "Python"],
    },
]
```

Then add corresponding learning resources:

```python
LEARNING_RESOURCES = {
    # ... existing resources ...
    "Kubernetes": {
        "courses": ["Kubernetes for Beginners (Udemy)"],
        "certifications": ["CKA", "CKAD"],
        "youtube": ["TechWorld with Nana - Kubernetes"],
        "books": ["Kubernetes in Action"],
    },
}
```

---

## Example: Adding New Skills

**File:** `career_app/services/datasets.py`

```python
SKILL_KEYWORDS = [
    # ... existing skills ...
    "GraphQL",
    "Next.js",
    "Blockchain",
    "Solidity",
    "Web3",
    "Rust",
]
```

Update corresponding role requirements:

```python
{
    "name": "Blockchain Developer",
    "slug": "blockchain-developer",
    "required_skills": ["Solidity", "Web3", "Blockchain"],
    "optional_skills": ["JavaScript", "Python", "Ethereum"],
}
```

---

## Reloading Configuration

After editing `datasets.py`:

1. **Django development server** - Automatically reloads (no restart needed)
2. **Production** - Restart your application server
3. **Cache issues** - Clear any application caches if running

---

## Questions?

For issues or to extend datasets:
- Edit `career_app/services/datasets.py` directly
- All changes are backward compatible
- Database models always take priority over default configurations
