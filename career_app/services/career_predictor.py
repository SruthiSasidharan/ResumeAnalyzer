"""
Module 2: Career Prediction - Predict job role based on skills.
Uses rule-based scoring + optional ML model.
"""
from django.apps import apps
from .datasets import CAREER_ROLES


class CareerPredictor:
    """Predict suitable career roles from user skills."""

    def __init__(self):
        self.roles = self._load_roles()

    def _load_roles(self) -> list:
        """Load roles from DB or fallback to configured roles."""
        try:
            CareerRole = apps.get_model('career_app', 'CareerRole')
            roles = list(CareerRole.objects.all().values('name', 'slug', 'required_skills', 'optional_skills'))
            if roles:
                return roles
        except Exception:
            pass
        return CAREER_ROLES

    def _default_roles(self) -> list:
        """Legacy method - now uses CAREER_ROLES from datasets."""
        return self._load_roles()

    def predict(self, skills: list) -> list:
        """
        Predict career roles with scores.
        Returns list of {"role": str, "slug": str, "score": float, "match_skills": list, "missing_required": list}
        """
        user_skills = {s.strip() for s in skills if s}
        results = []
        for role in self.roles:
            req = set(s.strip() for s in role.get("required_skills", []))
            opt = set(s.strip() for s in role.get("optional_skills", []))
            match_req = user_skills & req
            match_opt = user_skills & opt
            missing_req = list(req - user_skills)
            # Score: 60% required + 40% optional
            req_score = len(match_req) / len(req) if req else 1
            opt_score = len(match_opt) / len(opt) if opt else 1
            score = 0.6 * req_score + 0.4 * opt_score
            results.append({
                "role": role["name"],
                "slug": role.get("slug", role["name"].lower().replace(" ", "-")),
                "score": round(score, 2),
                "match_skills": list(match_req | match_opt),
                "missing_required": missing_req[:5],
            })
        results.sort(key=lambda x: -x["score"])
        return results[:5]
