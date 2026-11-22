"""Command line interface for ResumeSniper."""

import sys
import argparse
from pathlib import Path

from resumesniper.parser import DocumentParser
from resumesniper.matcher import ATSMatcher
from resumesniper.tailorer import ResumeTailorer
from resumesniper.reachout import OutreachGenerator

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main():
    parser = argparse.ArgumentParser(
        prog="resumesniper",
        description="Autonomous ATS Gap Analyzer, Resume Tailorer & Cold Reachout Copilot"
    )
    subparsers = parser.add_subparsers(dest="command")

    # analyze command
    p_an = subparsers.add_parser("analyze", help="Analyze resume against Job Description")
    p_an.add_argument("resume", help="Path to resume file (PDF, TXT, MD)")
    p_an.add_argument("--jd", required=True, help="Job description text or path to JD file")

    # reachout command
    p_ro = subparsers.add_parser("reachout", help="Generate targeted cold outreach messages")
    p_ro.add_argument("--candidate", default="Rishabh Raj", help="Candidate full name")
    p_ro.add_argument("--company", required=True, help="Target company name")
    p_ro.add_argument("--role", required=True, help="Target role title")
    p_ro.add_argument("--resume", help="Optional resume file path")
    p_ro.add_argument("--jd", help="Optional JD file or text")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "analyze":
        resume_text = DocumentParser.extract_text(Path(args.resume))
        parsed = DocumentParser.parse_resume(resume_text)

        jd_text = args.jd
        if Path(args.jd).exists():
            jd_text = DocumentParser.extract_text(Path(args.jd))

        report = ATSMatcher.evaluate(parsed, jd_text)

        score_color = GREEN if report.match_percentage >= 70 else (YELLOW if report.match_percentage >= 50 else RED)
        print(f"\n{BOLD}🎯 ResumeSniper ATS Match Score: {score_color}{report.match_percentage}%{RESET}\n")

        print(f"{GREEN}✓ Matching Skills ({len(report.matching_skills)}):{RESET}")
        print("  " + (", ".join(report.matching_skills) if report.matching_skills else "None"))

        print(f"\n{RED}✗ Missing Critical Skills ({len(report.missing_critical_skills)}):{RESET}")
        print("  " + (", ".join(report.missing_critical_skills) if report.missing_critical_skills else "None"))

        print(f"\n{BOLD}💡 Actionable Recommendations:{RESET}")
        for r in report.recommendations:
            print(f"  • {r}")
        print()
        return 0

    elif args.command == "reachout":
        parsed = DocumentParser.parse_resume("Python FastAPI Docker AI Agents System Design")
        report = ATSMatcher.evaluate(parsed, "Python FastAPI Docker Kubernetes")
        msgs = OutreachGenerator.generate_outreach(args.candidate, args.role, args.company, report)

        print(f"\n{CYAN}{BOLD}📩 LinkedIn Connection Request (<300 chars):{RESET}")
        print(msgs["linkedin_note"])

        print(f"\n{GREEN}{BOLD}📬 Hiring Manager Cold Email:{RESET}")
        print(msgs["cold_email"])
        print()
        return 0


if __name__ == "__main__":
    sys.exit(main())
