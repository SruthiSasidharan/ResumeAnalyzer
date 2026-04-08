"""
Module 1: Resume Analyzer - Extract skills, education, experience using NLP.
"""
import re
from pathlib import Path

_PDF_READER = None
_PDF_READER_NAME = None

try:
    import PyPDF2
    _PDF_READER = PyPDF2
    _PDF_READER_NAME = "PyPDF2"
except ImportError:
    pass

if _PDF_READER is None:
    try:
        import pypdf
        _PDF_READER = pypdf
        _PDF_READER_NAME = "pypdf"
    except ImportError:
        pass

if _PDF_READER is None:
    try:
        from pdfminer.high_level import extract_text as pdfminer_extract_text
        _PDF_READER = "pdfminer"
        _PDF_READER_NAME = "pdfminer.six"
    except ImportError:
        pass

try:
    from docx import Document
except ImportError:
    Document = None


class ResumeAnalyzer:
    """NLP-based resume parsing and skill extraction."""

    # Skill keywords for extraction (2024-2025 tech stack)
    SKILL_KEYWORDS = [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "Go", "Rust", "PHP", "Kotlin", "Swift",
        "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask", "Spring Boot", "FastAPI",
        "Machine Learning", "Deep Learning", "ML", "DL", "TensorFlow", "PyTorch", "Keras", "Scikit-learn",
        "NLP", "Natural Language Processing", "Computer Vision", "Data Science",
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "NoSQL",
        "AWS", "Azure", "GCP", "Google Cloud", "Amazon Web Services",
        "Docker", "Kubernetes", "Jenkins", "CI/CD", "DevOps", "Git", "Linux",
        "REST API", "GraphQL", "Microservices", "Agile", "Scrum", "JIRA",
        "Data Structures", "Algorithms", "Statistics", "Data Analysis",
        "Pandas", "NumPy", "Matplotlib", "Tableau", "Power BI", "Excel",
        "Cybersecurity", "Networking", "Testing", "Unit Testing", "Selenium", "Jest",
        "PySpark", "Hadoop", "Spark", "ETL", "Data Engineering"
    ]

    # Education patterns
    EDUCATION_PATTERNS = [
        r'(?i)(?:b\.?tech|b\.?e\.?|b\.?s\.?|b\.?sc|b\.?com|b\.?ca)\s*(?:in|–|-)?\s*([^\n,]+)',
        r'(?i)(?:m\.?tech|m\.?e\.?|m\.?s\.?|m\.?sc|m\.?ba|m\.?ca)\s*(?:in|–|-)?\s*([^\n,]+)',
        r'(?i)(?:bachelor|master|phd|doctoral)\s+(?:degree\s+)?(?:in\s+)?([^\n,]+)',
        r'(?i)(?:diploma|certification)\s+(?:in\s+)?([^\n,]+)',
        r'(?i)(?:graduated?|completed)\s+(?:from\s+)?([^\n,]+)',
    ]

    # Experience patterns
    EXPERIENCE_PATTERNS = [
        r'(?i)(?:worked|experience|intern|developer|engineer)\s+(?:at|@)\s+([^\n,\.]+)',
        r'(?i)(?:company|organization|employer)\s*:?\s*([^\n]+)',
        r'(?i)(?:junior|senior|associate)?\s*(?:software|web|data|ml)\s+(?:engineer|developer|analyst)[^\n]*',
        r'(?i)(?:\d+\s*(?:years?|yrs?|months?))\s+(?:of\s+)?(?:experience|exp)[^\n]*',
    ]

    def __init__(self):
        self._nlp = None
        self._load_nlp()

    def _load_nlp(self):
        """Load spaCy model if available."""
        try:
            import spacy
            try:
                self._nlp = spacy.load("en_core_web_sm")
            except OSError:
                try:
                    spacy.cli.download("en_core_web_sm")
                    self._nlp = spacy.load("en_core_web_sm")
                except Exception:
                    self._nlp = None
        except ImportError:
            self._nlp = None

    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF or DOC/DOCX."""
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == '.pdf':
            return self._extract_from_pdf(file_path)
        elif suffix in ('.doc', '.docx'):
            return self._extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

    def _extract_from_pdf(self, file_path: str) -> str:
        if _PDF_READER is None:
            raise ImportError(
                "PDF parsing requires one of: PyPDF2, pypdf, or pdfminer.six. "
                "Run: pip install PyPDF2"
            )
        if _PDF_READER == "pdfminer":
            return pdfminer_extract_text(file_path) or ""
        text = []
        with open(file_path, 'rb') as f:
            reader = _PDF_READER.PdfReader(f)
            for page in reader.pages:
                text.append(page.extract_text() or "")
        return "\n".join(text)

    def _extract_from_docx(self, file_path: str) -> str:
        if not Document:
            raise ImportError("python-docx is required for DOC parsing. Install: pip install python-docx")
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)

    def extract_skills(self, text: str) -> list:
        """Extract skills from resume text using keyword matching + NLP."""
        text_lower = text.lower()
        found_skills = set()

        # Keyword matching (case-insensitive)
        for skill in self.SKILL_KEYWORDS:
            if skill.lower() in text_lower:
                found_skills.add(skill)
            # Handle aliases
            if skill == "Machine Learning" and ("machine learning" in text_lower or " ml " in text_lower):
                found_skills.add("Machine Learning")
            if skill == "Deep Learning" and ("deep learning" in text_lower or " dl " in text_lower):
                found_skills.add("Deep Learning")
            if skill == "JavaScript" and ("javascript" in text_lower or " js " in text_lower or "js " in text_lower):
                found_skills.add("JavaScript")
            if skill == "TypeScript" and ("typescript" in text_lower or " ts " in text_lower):
                found_skills.add("TypeScript")

        # Regex for common skill phrases
        skill_patterns = [
            r'\b(Python|Java|JavaScript|React|Node\.js|SQL|MongoDB|AWS|Docker|TensorFlow|PyTorch)\b',
            r'\b(Machine Learning|Deep Learning|Data Science|NLP|Computer Vision)\b',
            r'\b(HTML|CSS|REST API|Git|Linux|Agile|Scrum)\b',
        ]
        for pattern in skill_patterns:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                found_skills.add(m.group(1))

        # Use spaCy NER for additional extraction
        if self._nlp and len(text) < 100000:
            doc = self._nlp(text[:50000])
            for ent in doc.ents:
                if ent.label_ in ("ORG", "PRODUCT", "WORK_OF_ART"):
                    for kw in self.SKILL_KEYWORDS:
                        if kw.lower() in ent.text.lower():
                            found_skills.add(kw)
                            break

        return sorted(list(found_skills))

    def extract_education(self, text: str) -> list:
        """Extract education info using regex patterns."""
        education = []
        for pattern in self.EDUCATION_PATTERNS:
            for m in re.finditer(pattern, text):
                edu = m.group(1).strip() if m.lastindex else m.group(0).strip()
                if edu and len(edu) > 2 and edu not in [e.get('degree', e) for e in education]:
                    education.append({"degree": edu[:200], "source": "pattern"})
        return education[:10]  # Limit to 10

    def extract_experience(self, text: str) -> list:
        """Extract experience/employment info."""
        experience = []
        for pattern in self.EXPERIENCE_PATTERNS:
            for m in re.finditer(pattern, text):
                exp = m.group(1).strip() if m.lastindex else m.group(0).strip()
                if exp and len(exp) > 2:
                    exp_clean = exp[:200]
                    if not any(exp_clean in str(e) for e in experience):
                        experience.append({"title_or_company": exp_clean})
        return experience[:10]

    def analyze(self, file_path: str) -> dict:
        """Full resume analysis pipeline."""
        text = self.extract_text(file_path)
        skills = self.extract_skills(text)
        education = self.extract_education(text)
        experience = self.extract_experience(text)
        return {
            "raw_text": text[:50000],  # Limit stored text
            "skills": skills,
            "education": education,
            "experience": experience,
        }
