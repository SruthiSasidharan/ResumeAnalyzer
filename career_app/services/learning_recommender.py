"""
Module 4: Learning Recommendation - Suggest courses, certifications, YouTube, books.
"""
from django.apps import apps


class LearningRecommender:
    """Recommend learning resources for missing skills."""

    def __init__(self):
        self.resources = self._load_resources()

    def _load_resources(self) -> dict:
        """Load from DB or default JSON."""
        try:
            LearningResource = apps.get_model('career_app', 'LearningResource')
            resources = {}
            for r in LearningResource.objects.all():
                skill = r.skill_name
                if skill not in resources:
                    resources[skill] = {"courses": [], "certifications": [], "youtube": [], "books": []}
                rtype = r.resource_type
                if rtype in resources[skill]:
                    resources[skill][rtype].append({"title": r.title, "url": r.url or "", "source": r.source or ""})
            if resources:
                return resources
        except Exception:
            pass
        return self._default_resources()

    def _default_resources(self) -> dict:
        return {
            "Python": {
                "courses": ["Python for Everybody (Coursera)", "Automate the Boring Stuff"],
                "certifications": ["PCEP", "PCAP"],
                "youtube": ["Corey Schafer - Python", "freeCodeCamp Python Full Course"],
                "books": ["Python Crash Course - Eric Matthes", "Fluent Python"],
            },
            "Machine Learning": {
                "courses": ["Machine Learning - Andrew Ng (Coursera)", "Deep Learning Specialization"],
                "certifications": ["AWS ML Specialty", "Google ML Engineer"],
                "youtube": ["StatQuest ML", "3Blue1Brown Neural Networks", "Krish Naik ML"],
                "books": ["Hands-On ML - Aurélien Géron"],
            },
            "JavaScript": {
                "courses": ["JavaScript Complete Guide (Udemy)", "Full Stack Open"],
                "certifications": ["Meta Front-End Developer"],
                "youtube": ["freeCodeCamp JavaScript", "Web Dev Simplified"],
                "books": ["You Don't Know JS - Kyle Simpson"],
            },
            "React": {
                "courses": ["React Complete Guide (Udemy)", "Epic React"],
                "certifications": ["Meta React Certificate"],
                "youtube": ["freeCodeCamp React", "Web Dev Simplified React"],
                "books": ["Learning React - Alex Banks"],
            },
            "SQL": {
                "courses": ["SQL for Data Science (Coursera)", "Complete SQL Bootcamp"],
                "certifications": ["Oracle SQL Certified"],
                "youtube": ["freeCodeCamp SQL", "Alex The Analyst SQL"],
                "books": ["SQL Cookbook", "Learning SQL"],
            },
            "HTML": {
                "courses": ["Web Development Bootcamp (Udemy)"],
                "certifications": [],
                "youtube": ["freeCodeCamp HTML", "Traversy Media HTML"],
                "books": ["HTML and CSS - Jon Duckett"],
            },
            "CSS": {
                "courses": ["Advanced CSS and Sass (Udemy)"],
                "certifications": [],
                "youtube": ["Kevin Powell CSS", "Web Dev Simplified CSS"],
                "books": ["CSS in Depth"],
            },
            "Node.js": {
                "courses": ["Complete Node.js Developer (Udemy)"],
                "certifications": ["OpenJS Node.js Certification"],
                "youtube": ["freeCodeCamp Node.js", "Traversy Media Node.js"],
                "books": ["Node.js Design Patterns"],
            },
            "TensorFlow": {
                "courses": ["TensorFlow in Practice (Coursera)"],
                "certifications": ["TensorFlow Developer Certificate"],
                "youtube": ["deeplizard TensorFlow"],
                "books": [],
            },
            "PyTorch": {
                "courses": ["Deep Learning with PyTorch (Udacity)"],
                "certifications": [],
                "youtube": ["Daniel Bourke PyTorch", "Aladdin Persson PyTorch"],
                "books": ["Deep Learning with PyTorch"],
            },
            "Docker": {
                "courses": ["Docker Mastery (Udemy)"],
                "certifications": ["Docker Certified Associate"],
                "youtube": ["TechWorld with Nana Docker", "Fireship Docker"],
                "books": ["Docker Deep Dive"],
            },
            "AWS": {
                "courses": ["AWS Solutions Architect (Udemy)"],
                "certifications": ["AWS Solutions Architect Associate"],
                "youtube": ["freeCodeCamp AWS"],
                "books": ["AWS Certified Solutions Architect"],
            },
            "Data Analysis": {
                "courses": ["Google Data Analytics Certificate"],
                "certifications": ["Google Data Analytics Professional"],
                "youtube": ["Alex The Analyst", "Luke Barousse"],
                "books": ["Storytelling with Data"],
            },
            "Statistics": {
                "courses": ["Statistics with Python (Coursera)"],
                "certifications": [],
                "youtube": ["StatQuest Statistics", "Khan Academy Statistics"],
                "books": ["Practical Statistics for Data Scientists"],
            },
        }

    def recommend(self, skill_names: list) -> list:
        """Return learning resources for each skill."""
        results = []
        for skill in skill_names:
            skill_clean = skill.strip()
            if skill_clean in self.resources:
                r = self.resources[skill_clean]
                results.append({
                    "skill": skill_clean,
                    "courses": r.get("courses", [])[:3],
                    "certifications": r.get("certifications", [])[:2],
                    "youtube": r.get("youtube", [])[:3],
                    "books": r.get("books", [])[:2],
                })
            else:
                results.append({
                    "skill": skill_clean,
                    "courses": ["Search Coursera/Udemy for this skill"],
                    "certifications": [],
                    "youtube": ["Search YouTube for tutorials"],
                    "books": [],
                })
        return results
