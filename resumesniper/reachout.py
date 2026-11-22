"""Cold outreach message generator for recruiters and engineering leaders."""

from typing import Dict
from resumesniper.matcher import ATSReport


class OutreachGenerator:
    """Synthesizes high-converting, non-templated cold messages."""

    @staticmethod
    def generate_outreach(candidate_name: str, target_role: str, company_name: str, report: ATSReport) -> Dict[str, str]:
        top_skills = ", ".join(report.matching_skills[:3]) if report.matching_skills else "Python, System Architecture"

        # 1. LinkedIn Connection Note (Strict <= 300 chars limit)
        linkedin_note = (
            f"Hi! Noticed {company_name}'s work in {target_role}. "
            f"I specialize in {top_skills} with production agentic and backend experience. "
            f"Would love to connect and follow your engineering journey!"
        )[:300]

        # 2. Hiring Manager Cold Email
        cold_email = (
            f"Subject: {target_role} @ {company_name} — Engineering Background ({top_skills})\n\n"
            f"Hi team,\n\n"
            f"I came across the {target_role} opening at {company_name} and was particularly drawn to your stack.\n\n"
            f"Recently, I built and productionized high-throughput systems focusing on {top_skills}, "
            f"delivering low-latency pipelines and modular architectures. Based on your requirements, "
            f"my background directly addresses your active technical challenges.\n\n"
            f"I've attached my tailored resume and GitHub profile (github.com/Rishabhraj06). "
            f"Are you open to a brief 10-minute sync this week?\n\n"
            f"Best regards,\n{candidate_name}"
        )

        # 3. Twitter / Quick DM
        quick_dm = (
            f"Hey! Saw you are scaling engineering for {company_name}. "
            f"I'm an AI & Systems Engineer working on {top_skills}. "
            f"Would love to drop my GitHub and see if there's a strong fit for {target_role}!"
        )

        return {
            "linkedin_note": linkedin_note,
            "cold_email": cold_email,
            "quick_dm": quick_dm
        }
