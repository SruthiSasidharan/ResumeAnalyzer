"""
Module 2: Career Prediction - Predict job role based on skills.
Uses rule-based scoring + optional ML model.
"""
from django.apps import apps


class CareerPredictor:
    """Predict suitable career roles from user skills."""

    def __init__(self):
        self.roles = self._load_roles()

    def _load_roles(self) -> list:
        """Load roles from DB or fallback to default."""
        try:
            CareerRole = apps.get_model('career_app', 'CareerRole')
            roles = list(CareerRole.objects.all().values('name', 'slug', 'required_skills', 'optional_skills'))
            if roles:
                return roles
        except Exception:
            pass
        return self._default_roles()

    def _default_roles(self) -> list:
        return [
            {"name": "Data Scientist", "slug": "data-scientist",
             "required_skills": ["Python", "Machine Learning", "SQL", "Statistics", "Data Analysis"],
             "optional_skills": ["TensorFlow", "PyTorch", "Deep Learning", "NLP", "Pandas", "NumPy"]},
            {"name": "Frontend Developer", "slug": "frontend-developer",
             "required_skills": ["HTML", "CSS", "JavaScript"],
             "optional_skills": ["React", "Angular", "Vue.js", "TypeScript", "REST API"]},
            {"name": "Backend Developer", "slug": "backend-developer",
             "required_skills": ["Python", "SQL", "REST API"],
             "optional_skills": ["Node.js", "Django", "Flask", "Spring Boot", "MongoDB", "Docker", "Redis"]},
            {"name": "Full Stack Developer", "slug": "fullstack-developer",
             "required_skills": ["JavaScript", "HTML", "CSS", "SQL", "REST API"],
             "optional_skills": ["React", "Node.js", "Python", "MongoDB", "Docker"]},
            {"name": "ML Engineer", "slug": "ml-engineer",
             "required_skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch"],
             "optional_skills": ["Deep Learning", "NLP", "Computer Vision", "Kubernetes", "Docker"]},
            {"name": "DevOps Engineer", "slug": "devops-engineer",
             "required_skills": ["Linux", "Docker", "CI/CD", "AWS"],
             "optional_skills": ["Kubernetes", "Jenkins", "Azure", "GCP", "Networking"]},
            {"name": "Data Analyst", "slug": "data-analyst",
             "required_skills": ["SQL", "Excel", "Data Analysis", "Statistics"],
             "optional_skills": ["Python", "Tableau", "Power BI", "Pandas"]},
            {"name": "Software Engineer", "slug": "software-engineer",
             "required_skills": ["Python", "Data Structures", "Algorithms", "Git"],
             "optional_skills": ["Java", "C++", "SQL", "REST API", "Docker"]},
        ]

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
