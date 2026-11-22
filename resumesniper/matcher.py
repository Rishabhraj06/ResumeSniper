"""ATS Keyword matching and skill gap calculation."""

import re
from dataclasses import dataclass
from typing import List, Set, Dict, Tuple
from resumesniper.parser import COMMON_SKILLS, ParsedResume


@dataclass
class ATSReport:
    match_percentage: float
    matching_skills: List[str]
    missing_critical_skills: List[str]
    jd_skill_count: int
    recommendations: List[str]


class ATSMatcher:
    """Computes resume compatibility against Job Descriptions."""

    @staticmethod
    def extract_jd_skills(jd_text: str) -> List[str]:
        lower_jd = jd_text.lower()
        found = []
        for skill in COMMON_SKILLS:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, lower_jd):
                found.append(skill)
        return found

    @classmethod
    def evaluate(cls, resume: ParsedResume, jd_text: str) -> ATSReport:
        jd_skills = cls.extract_jd_skills(jd_text)
        if not jd_skills:
            return ATSReport(
                match_percentage=100.0,
                matching_skills=resume.skills,
                missing_critical_skills=[],
                jd_skill_count=0,
                recommendations=["Job description did not contain standardized technical keywords."]
            )

        resume_skill_set = set(resume.skills)
        jd_skill_set = set(jd_skills)

        matching = sorted(list(resume_skill_set.intersection(jd_skill_set)))
        missing = sorted(list(jd_skill_set - resume_skill_set))

        match_pct = round((len(matching) / len(jd_skill_set)) * 100, 1)

        recs = []
        if missing:
            recs.append(f"Add critical missing skills to your projects/skills section: {', '.join(missing[:5])}.")
        if match_pct < 60:
            recs.append("Low ATS match score (<60%). Tailor your experience bullets to reflect the required tech stack.")
        else:
            recs.append("Strong ATS baseline match. Proceed to personalized outreach.")

        return ATSReport(
            match_percentage=match_pct,
            matching_skills=matching,
            missing_critical_skills=missing,
            jd_skill_count=len(jd_skills),
            recommendations=recs
        )
