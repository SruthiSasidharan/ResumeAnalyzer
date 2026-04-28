"""
Module 4: Learning Recommendation - Suggest courses, certifications, YouTube, books.
"""
from django.apps import apps
from .datasets import LEARNING_RESOURCES


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
        return LEARNING_RESOURCES

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
