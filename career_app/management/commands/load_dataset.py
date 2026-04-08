"""
Load latest dataset into database - Skills, Roles, Learning Resources, Jobs.
Run: python manage.py load_dataset
"""
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Load skills, roles, learning resources, and job listings into database'

    def handle(self, *args, **options):
        base = Path(__file__).resolve().parent.parent.parent
        data_dir = base / 'career_app' / 'data'

        # Skills
        Skill = apps.get_model('career_app', 'Skill')
        skills_data = [
            {"name": "Python", "category": "Programming", "aliases": ["Py"]},
            {"name": "Java", "category": "Programming", "aliases": []},
            {"name": "JavaScript", "category": "Programming", "aliases": ["JS"]},
            {"name": "TypeScript", "category": "Programming", "aliases": ["TS"]},
            {"name": "React", "category": "Frontend", "aliases": []},
            {"name": "Machine Learning", "category": "AI/ML", "aliases": ["ML"]},
            {"name": "SQL", "category": "Database", "aliases": []},
            {"name": "Docker", "category": "DevOps", "aliases": []},
            {"name": "AWS", "category": "Cloud", "aliases": []},
            {"name": "TensorFlow", "category": "AI/ML", "aliases": []},
            {"name": "PyTorch", "category": "AI/ML", "aliases": []},
            {"name": "HTML", "category": "Frontend", "aliases": []},
            {"name": "CSS", "category": "Frontend", "aliases": []},
            {"name": "Node.js", "category": "Backend", "aliases": ["Node"]},
            {"name": "Django", "category": "Backend", "aliases": []},
            {"name": "Flask", "category": "Backend", "aliases": []},
            {"name": "Data Analysis", "category": "Data", "aliases": []},
            {"name": "Statistics", "category": "Data", "aliases": []},
        ]
        for s in skills_data:
            Skill.objects.update_or_create(name=s["name"], defaults=s)
        self.stdout.write(f'Loaded {len(skills_data)} skills')

        # Career Roles
        CareerRole = apps.get_model('career_app', 'CareerRole')
        roles_data = [
            {"name": "Data Scientist", "slug": "data-scientist", "description": "",
             "required_skills": ["Python", "Machine Learning", "SQL", "Statistics", "Data Analysis"],
             "optional_skills": ["TensorFlow", "PyTorch", "NLP", "Pandas"]},
            {"name": "Frontend Developer", "slug": "frontend-developer", "description": "",
             "required_skills": ["HTML", "CSS", "JavaScript"],
             "optional_skills": ["React", "TypeScript", "Vue.js"]},
            {"name": "Backend Developer", "slug": "backend-developer", "description": "",
             "required_skills": ["Python", "SQL", "REST API"],
             "optional_skills": ["Node.js", "Django", "Flask", "MongoDB", "Docker"]},
            {"name": "Full Stack Developer", "slug": "fullstack-developer", "description": "",
             "required_skills": ["JavaScript", "HTML", "CSS", "SQL"],
             "optional_skills": ["React", "Node.js", "Django"]},
            {"name": "ML Engineer", "slug": "ml-engineer", "description": "",
             "required_skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch"],
             "optional_skills": ["Docker", "Kubernetes"]},
            {"name": "DevOps Engineer", "slug": "devops-engineer", "description": "",
             "required_skills": ["Linux", "Docker", "CI/CD", "AWS"],
             "optional_skills": ["Kubernetes", "Jenkins"]},
            {"name": "Data Analyst", "slug": "data-analyst", "description": "",
             "required_skills": ["SQL", "Excel", "Data Analysis", "Statistics"],
             "optional_skills": ["Python", "Tableau", "Power BI"]},
            {"name": "Software Engineer", "slug": "software-engineer", "description": "",
             "required_skills": ["Python", "Data Structures", "Algorithms", "Git"],
             "optional_skills": ["Java", "SQL", "Docker"]},
        ]
        for r in roles_data:
            CareerRole.objects.update_or_create(slug=r["slug"], defaults=r)
        self.stdout.write(f'Loaded {len(roles_data)} roles')

        # Learning Resources
        LearningResource = apps.get_model('career_app', 'LearningResource')
        learning_data = [
            ("Python", "course", "Python for Everybody (Coursera)", "https://coursera.org", "Coursera"),
            ("Python", "certification", "PCEP - Certified Entry-Level Python Programmer", "", "Python Institute"),
            ("Python", "youtube", "Corey Schafer - Python Tutorial", "https://youtube.com", "YouTube"),
            ("Python", "book", "Python Crash Course - Eric Matthes", "", "No Starch Press"),
            ("Machine Learning", "course", "Machine Learning - Andrew Ng (Coursera)", "https://coursera.org", "Coursera"),
            ("Machine Learning", "certification", "Google Professional ML Engineer", "", "Google"),
            ("Machine Learning", "youtube", "StatQuest - Machine Learning", "https://youtube.com", "YouTube"),
            ("JavaScript", "course", "JavaScript Complete Guide (Udemy)", "https://udemy.com", "Udemy"),
            ("JavaScript", "youtube", "freeCodeCamp - JavaScript Full Course", "https://youtube.com", "YouTube"),
            ("React", "course", "React - The Complete Guide (Udemy)", "https://udemy.com", "Udemy"),
            ("React", "certification", "Meta React Certificate", "", "Meta"),
            ("SQL", "course", "SQL for Data Science (Coursera)", "https://coursera.org", "Coursera"),
            ("SQL", "youtube", "Alex The Analyst - SQL", "https://youtube.com", "YouTube"),
            ("Docker", "course", "Docker Mastery (Udemy)", "https://udemy.com", "Udemy"),
            ("Docker", "certification", "Docker Certified Associate", "", "Docker"),
            ("AWS", "course", "AWS Solutions Architect (Udemy)", "https://udemy.com", "Udemy"),
            ("AWS", "certification", "AWS Solutions Architect Associate", "", "AWS"),
        ]
        for skill_name, rtype, title, url, source in learning_data:
            LearningResource.objects.get_or_create(
                skill_name=skill_name, resource_type=rtype, title=title,
                defaults={"url": url, "source": source}
            )
        self.stdout.write(f'Loaded {len(learning_data)} learning resources')

        # Job Listings (sample)
        JobListing = apps.get_model('career_app', 'JobListing')
        jobs_data = [
            ("Data Scientist", "TechCorp", "Remote", "data-scientist", ["Python", "ML", "SQL"], "https://example.com/1"),
            ("Senior Data Scientist", "DataInc", "Bangalore", "data-scientist", ["Python", "TensorFlow", "NLP"], "https://example.com/2"),
            ("Frontend Developer", "WebWorks", "Hyderabad", "frontend-developer", ["React", "JavaScript", "CSS"], "https://example.com/3"),
            ("Full Stack Developer", "StartupX", "Remote", "fullstack-developer", ["Node.js", "React", "MongoDB"], "https://example.com/4"),
            ("Backend Engineer", "APILabs", "Chennai", "backend-developer", ["Python", "Django", "PostgreSQL"], "https://example.com/5"),
            ("ML Engineer", "AIM Labs", "Mumbai", "ml-engineer", ["PyTorch", "TensorFlow", "Python"], "https://example.com/6"),
            ("DevOps Engineer", "CloudTech", "Pune", "devops-engineer", ["AWS", "Docker", "Kubernetes"], "https://example.com/7"),
            ("Data Analyst", "AnalyticsPro", "Delhi", "data-analyst", ["SQL", "Python", "Tableau"], "https://example.com/8"),
        ]
        for title, company, location, role_slug, skills, url in jobs_data:
            obj, _ = JobListing.objects.get_or_create(
                title=title, company=company,
                defaults={"location": location, "role_slug": role_slug, "skills_required": skills, "url": url}
            )
        self.stdout.write(self.style.SUCCESS(f'Loaded {len(jobs_data)} job listings'))
