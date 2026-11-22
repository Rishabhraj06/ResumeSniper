"""Bullet tailoring and resume alignment engine."""

import os
from typing import List, Dict, Optional
from resumesniper.parser import ParsedResume
from resumesniper.matcher import ATSReport

ACTION_VERBS = [
    "Architected", "Engineered", "Spearheaded", "Optimized", "Scaled",
    "Streamlined", "Deployed", "Formulated", "Automated", "Orchestrated"
]


class ResumeTailorer:
    """Tailors resume experience bullets according to target job requirements."""

    @classmethod
    def tailor_bullets(cls, bullets: List[str], missing_skills: List[str]) -> List[Dict[str, str]]:
        tailored = []
        for idx, bullet in enumerate(bullets):
            target_skill = missing_skills[idx % len(missing_skills)] if missing_skills else ""
            enhanced = cls._enhance_bullet(bullet, target_skill)
            tailored.append({
                "original": bullet,
                "enhanced": enhanced,
                "targeted_skill": target_skill
            })
        return tailored

    @staticmethod
    def _enhance_bullet(bullet: str, skill: str) -> str:
        # Check if Google XYZ pattern exists (metric/result)
        has_metric = any(char in bullet for char in ["%", "x", "ms", "$", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
        first_word = bullet.split()[0] if bullet.split() else ""

        prefix = "Architected and optimized" if first_word.lower() in ("built", "created", "worked", "did") else first_word
        core_text = " ".join(bullet.split()[1:]) if bullet.split() else bullet

        if skill and skill not in bullet.lower():
            if has_metric:
                return f"{prefix} {core_text}, incorporating {skill} to improve modularity and execution throughput."
            else:
                return f"{prefix} {core_text} utilizing {skill}, achieving a 35% reduction in latency."
        return bullet
