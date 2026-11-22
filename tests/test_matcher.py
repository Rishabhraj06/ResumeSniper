"""Tests for ResumeSniper parser and ATS matcher."""

from resumesniper.parser import DocumentParser
from resumesniper.matcher import ATSMatcher
from resumesniper.reachout import OutreachGenerator


def test_resume_parser_detects_skills_and_bullets():
    raw = """
    Rishabh Raj
    Skills: Python, FastAPI, Docker, Kubernetes
    Experience:
    • Built autonomous multi-agent pipelines serving 10k users.
    • Scaled database queries with Redis caching.
    """
    parsed = DocumentParser.parse_resume(raw)
    assert "python" in parsed.skills
    assert "fastapi" in parsed.skills
    assert len(parsed.experience_bullets) == 2


def test_ats_matcher_calculates_gap():
    raw_resume = "Skills: Python, Docker, FastAPI"
    raw_jd = "Looking for engineer skilled in Python, Docker, Kubernetes, AWS"

    parsed = DocumentParser.parse_resume(raw_resume)
    report = ATSMatcher.evaluate(parsed, raw_jd)

    assert report.match_percentage == 50.0
    assert "python" in report.matching_skills
    assert "kubernetes" in report.missing_critical_skills


def test_outreach_generator_respects_linkedin_char_limit():
    parsed = DocumentParser.parse_resume("Python FastAPI")
    report = ATSMatcher.evaluate(parsed, "Python FastAPI")
    msgs = OutreachGenerator.generate_outreach("Rishabh Raj", "AI Engineer", "Anthropic", report)

    assert len(msgs["linkedin_note"]) <= 300
    assert "Anthropic" in msgs["cold_email"]
