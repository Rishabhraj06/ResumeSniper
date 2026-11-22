"""Resume and Job Description parsing engine."""

import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class ParsedResume:
    raw_text: str
    skills: List[str]
    experience_bullets: List[str]
    projects: List[str]
    sections: Dict[str, str]


COMMON_SKILLS = [
    "python", "javascript", "typescript", "c++", "java", "golang", "rust",
    "fastapi", "flask", "django", "react", "next.js", "vue", "angular", "node.js",
    "docker", "kubernetes", "aws", "gcp", "azure", "linux", "git", "ci/cd",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "chromadb", "pinecone",
    "pytorch", "tensorflow", "langchain", "llamaindex", "rag", "mcp", "llm",
    "rest api", "graphql", "grpc", "microservices", "system design", "distributed systems"
]


class DocumentParser:
    """Parses resumes and job descriptions from multiple document formats."""

    @staticmethod
    def extract_text(file_path: Path) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if path.suffix.lower() == ".pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(str(path))
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
                return text.strip()
            except Exception as e:
                raise RuntimeError(f"Error reading PDF: {e}")
        else:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()

    @staticmethod
    def parse_resume(text: str) -> ParsedResume:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        lower_text = text.lower()

        # 1. Identify skills
        detected_skills = []
        for skill in COMMON_SKILLS:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, lower_text):
                detected_skills.append(skill)

        # 2. Extract bullet points
        bullets = []
        for line in lines:
            if line.startswith(("-", "•", "*", "–")) or re.match(r"^\d+\.", line):
                clean_bullet = re.sub(r"^[-•*–\d.]+\s*", "", line).strip()
                if len(clean_bullet) > 15:
                    bullets.append(clean_bullet)

        # 3. Simple section division
        sections: Dict[str, str] = {}
        current_sec = "general"
        sec_lines: List[str] = []

        section_headers = {
            "skills": ["skills", "technical skills", "technologies"],
            "experience": ["experience", "work experience", "employment"],
            "projects": ["projects", "personal projects", "open source"],
            "education": ["education", "academic background"]
        }

        for line in lines:
            header_found = False
            for sec_name, aliases in section_headers.items():
                if line.lower().strip(":# ") in aliases:
                    if sec_lines:
                        sections[current_sec] = "\n".join(sec_lines)
                    current_sec = sec_name
                    sec_lines = []
                    header_found = True
                    break
            if not header_found:
                sec_lines.append(line)

        if sec_lines:
            sections[current_sec] = "\n".join(sec_lines)

        return ParsedResume(
            raw_text=text,
            skills=detected_skills,
            experience_bullets=bullets,
            projects=[],
            sections=sections
        )
