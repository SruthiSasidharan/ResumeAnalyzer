"""
Module 3: Skill Gap Detection - Compare user skills with industry skill sets.
"""
from .career_predictor import CareerPredictor


class SkillGapDetector:
    """Identify missing skills for target roles."""

    def __init__(self):
        self.predictor = CareerPredictor()

    def detect(self, user_skills: list, target_role: str = None) -> dict:
        """
        Detect skill gaps.
        If target_role given, return gaps for that role; else use top predicted role.
        """
        predictions = self.predictor.predict(user_skills)
        if not predictions:
            return {"gaps": [], "target_role": None, "skill_score": 0, "career_readiness": "Beginner"}

        top = predictions[0]
        if target_role:
            for p in predictions:
                if p["slug"] == target_role or p["role"].lower() == target_role.lower():
                    top = p
                    break

        missing = top.get("missing_required", [])
        gaps = [{"skill": s, "importance": "high", "role": top["role"]} for s in missing]

        # Add missing optional skills that would boost score
        for role in self.predictor.roles:
            if role.get("slug") == top["slug"] or role.get("name") == top["role"]:
                opt = set(role.get("optional_skills", [])) - set(user_skills)
                for s in list(opt)[:5]:
                    gaps.append({"skill": s, "importance": "medium", "role": top["role"]})
                break

        skill_score = top["score"] * 100
        if skill_score >= 80:
            readiness = "Advanced"
        elif skill_score >= 60:
            readiness = "Intermediate"
        elif skill_score >= 40:
            readiness = "Beginner-Intermediate"
        else:
            readiness = "Beginner"

        return {
            "gaps": gaps[:15],
            "target_role": top["role"],
            "skill_score": round(skill_score, 1),
            "career_readiness": readiness,
        }
