# AI Career Guidance & Skill Gap Analyzer

A Django-based system that helps students and professionals:
- **Upload resume** (PDF/DOC)
- **Analyze skills** using NLP
- **Predict suitable career roles** (e.g., Python + ML → Data Scientist)
- **Identify missing skills** (Skill Gap Detection)
- **Suggest learning paths** (Courses, Certifications, YouTube, Books)
- **Recommend jobs** based on predicted role

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML + Bootstrap 5 |
| Backend | Django 4.2 (Python 3.8+) |
| AI/NLP | Python, spaCy, NLP-based parsing |
| ML | scikit-learn (optional), rule-based career prediction |
| Database | MySQL (SQLite supported for dev) |

## Modules

1. **Resume Analyzer** - Extract skills, education, experience from PDF/DOC using NLP
2. **Career Prediction** - Predict job roles from skills (rule-based + scoring)
3. **Skill Gap Detection** - Compare user skills with industry role requirements
4. **Learning Recommendation** - Courses, certifications, YouTube, books per skill
5. **Job Recommendation** - Job listings by role (DB dataset; extensible to APIs)
6. **Dashboard** - Skill score, career readiness, progress tracking

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. Install dependencies (Python 3.8.10 compatible)

```bash
pip install -r requirements.txt
```

### 3. Download spaCy model (optional, for better NLP)

```bash
python -m spacy download en_core_web_sm
```

### 4. Database

**Option A: SQLite (default, no setup)**

The project uses SQLite by default. Just run migrations.

**Option B: MySQL**

1. Create a MySQL database:
   ```sql
   CREATE DATABASE career_guidance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Set environment variables:
   ```bash
   set DB_ENGINE=mysql
   set DB_NAME=career_guidance_db
   set DB_USER=root
   set DB_PASSWORD=your_password
   set DB_HOST=localhost
   set DB_PORT=3306
   ```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Load dataset (skills, roles, learning resources, jobs)

```bash
python manage.py load_dataset
```

### 7. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 8. Run server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Usage

1. **Dashboard** - Overview and upload CTA
2. **Upload Resume** - Select PDF or DOC/DOCX, click Upload & Analyze
3. **Analysis Result** - View skill score, career readiness, predicted roles, skill gaps, learning recommendations, jobs

## Project Structure

```
├── career_guidance/       # Django project settings
├── career_app/            # Main app
│   ├── models.py          # Skill, CareerRole, LearningResource, JobListing, Resume
│   ├── views.py           # Dashboard, Upload, Analyze, Result, Jobs
│   ├── services/          # AI modules
│   │   ├── resume_analyzer.py
│   │   ├── career_predictor.py
│   │   ├── skill_gap.py
│   │   ├── learning_recommender.py
│   │   └── job_recommender.py
│   └── management/commands/load_dataset.py
├── templates/             # HTML + Bootstrap
├── static/
├── uploads/               # Uploaded resumes
└── requirements.txt
```

## Extending

- **Job API**: Integrate Adzuna, JSearch (RapidAPI), or Indeed in `job_recommender.py`
- **ML model**: Replace rule-based career prediction with a trained classifier
- **More roles/skills**: Add via Django admin or `load_dataset` command

## License

MIT
