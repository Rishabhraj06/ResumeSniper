"""ResumeSniper Interactive Web Dashboard powered by Streamlit."""

import streamlit as st
from pathlib import Path
from resumesniper.parser import DocumentParser
from resumesniper.matcher import ATSMatcher
from resumesniper.tailorer import ResumeTailorer
from resumesniper.reachout import OutreachGenerator

st.set_page_config(page_title="ResumeSniper | ATS Copilot", page_icon="🎯", layout="wide")

st.title("🎯 ResumeSniper — ATS Matcher & Recruiter Outreach Copilot")
st.caption("Maximize interview call-backs by eliminating keyword gaps and generating tailored outreach.")

with st.sidebar:
    st.header("📄 Your Master Profile")
    candidate_name = st.text_input("Candidate Name", value="Rishabh Raj")
    target_role = st.text_input("Target Role", value="AI & Systems Engineer")
    target_company = st.text_input("Target Company", value="Tech Innovations")

    uploaded_resume = st.file_uploader("Upload Resume (PDF, TXT, MD)", type=["pdf", "txt", "md"])

    sample_resume = st.button("Load Sample Senior AI Resume")

resume_text = ""
if uploaded_resume:
    if uploaded_resume.name.endswith(".pdf"):
        import pypdf
        reader = pypdf.PdfReader(uploaded_resume)
        resume_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        resume_text = uploaded_resume.read().decode("utf-8", errors="ignore")
elif sample_resume:
    resume_text = """
    Rishabh Raj — AI & Systems Engineer
    Skills: Python, FastAPI, Docker, PyTorch, LangChain, RAG, MCP, PostgreSQL, Linux, Git
    Experience:
    • Architected high-throughput Multi-Agent frameworks using Python and FastAPI, reducing execution latency by 45%.
    • Engineered hybrid search RAG engines with BM25 and vector embeddings, serving sub-20ms queries.
    • Automated pre-flight security screening with custom AST scanners.
    """

jd_input = st.text_area(
    "Paste Target Job Description (JD):",
    height=160,
    placeholder="e.g. Seeking an AI Engineer experienced in Python, FastAPI, Docker, Kubernetes, AWS, and Hybrid RAG..."
)

if st.button("🚀 Analyze ATS Match & Tailor", type="primary") and (resume_text or sample_resume) and jd_input:
    parsed = DocumentParser.parse_resume(resume_text)
    report = ATSMatcher.evaluate(parsed, jd_input)

    c1, c2, c3 = st.columns(3)
    c1.metric("ATS Match Score", f"{report.match_percentage}%")
    c2.metric("Matching Required Skills", len(report.matching_skills))
    c3.metric("Critical Missing Skills", len(report.missing_critical_skills))

    st.progress(int(report.match_percentage))

    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("✅ Matching Required Skills")
        if report.matching_skills:
            st.success(", ".join(report.matching_skills))
        else:
            st.warning("No direct keyword match.")

    with col_r:
        st.subheader("🚨 Critical Missing Skills")
        if report.missing_critical_skills:
            st.error(", ".join(report.missing_critical_skills))
        else:
            st.success("All required technical skills matched!")

    st.markdown("---")
    st.subheader("✨ Tailored Bullet Suggestions (Google XYZ Formula)")
    if parsed.experience_bullets:
        tailored = ResumeTailorer.tailor_bullets(parsed.experience_bullets[:3], report.missing_critical_skills)
        for t in tailored:
            st.markdown(f"**Original:** {t['original']}")
            st.info(f"👉 **Tailored:** {t['enhanced']}")
            st.caption(f"Aligned with missing skill: `{t['targeted_skill']}`")

    st.markdown("---")
    st.subheader("📬 1-Click High-Converting Recruiter Reachout")
    msgs = OutreachGenerator.generate_outreach(candidate_name, target_role, target_company, report)

    tab1, tab2, tab3 = st.tabs(["LinkedIn Note (<300 chars)", "Hiring Manager Cold Email", "Twitter/Quick DM"])
    with tab1:
        st.text_area("Copy-Paste LinkedIn Connection Message:", msgs["linkedin_note"], height=100)
    with tab2:
        st.text_area("Personalized Cold Email:", msgs["cold_email"], height=200)
    with tab3:
        st.text_area("Twitter / X Direct Message:", msgs["quick_dm"], height=100)
