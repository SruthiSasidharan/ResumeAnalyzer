"""
Centralized Dataset Configuration
All datasets for resume analysis, career prediction, and job recommendations
can be easily updated here without modifying service files.
"""

# ============================================================================
# RESUME ANALYZER DATASETS
# ============================================================================

SKILL_KEYWORDS = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "Go", "Rust", "PHP", "Kotlin", "Swift",
    # Frontend
    "HTML", "CSS", "React", "Angular", "Vue.js",
    # Backend & APIs
    "Node.js", "Express", "Django", "Flask", "Spring Boot", "FastAPI",
    # AI/ML
    "Machine Learning", "Deep Learning", "ML", "DL", "TensorFlow", "PyTorch", "Keras", "Scikit-learn",
    "NLP", "Natural Language Processing", "Computer Vision", "Data Science",
    # Databases
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "NoSQL",
    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Google Cloud", "Amazon Web Services",
    "Docker", "Kubernetes", "Jenkins", "CI/CD", "DevOps", "Git", "Linux",
    # Architecture & Design
    "REST API", "GraphQL", "Microservices", "Agile", "Scrum", "JIRA",
    # Data & Analytics
    "Data Structures", "Algorithms", "Statistics", "Data Analysis",
    "Pandas", "NumPy", "Matplotlib", "Tableau", "Power BI", "Excel",
    # Security & Testing
    "Cybersecurity", "Networking", "Testing", "Unit Testing", "Selenium", "Jest",
    # Big Data
    "PySpark", "Hadoop", "Spark", "ETL", "Data Engineering"
]

EDUCATION_PATTERNS = [
    # Match degree with optional (CODE) like "Master of Computer Application (MCA)"
    r'(?i)((?:master|bachelor|phd|diploma|degree|b\.?(?:tech|e|s|sc|com|ca)|m\.?(?:tech|e|s|sc|ca|ba))\s+(?:of\s+)?[a-zA-Z\s&\-]+(?:\s*\([A-Z]{2,}\))?)',
    # Match "X | Y | Z" format common in resumes (education separated by pipes)
    r'^([^\n|]{10,100})\s*\|\s*([^\n|]{5,100})',
]

EXPERIENCE_PATTERNS = [
    # Senior/Junior Software Engineer at Company
    r'(?i)((?:senior|junior|lead|principal|associate)?\s+(?:software|web|mobile|data|ml|devops|cloud|systems)\s+(?:engineer|developer|architect|analyst|specialist))\s+(?:at|in)\s+([a-zA-Z0-9\s&\-\.()]{3,100}?)(?=\n|,|;|$)',
    # Role at Company format
    r'(?i)([a-zA-Z\s&\-\.()]{5,80})\s+(?:at|@|in)\s+([a-zA-Z0-9\s&\-\.()]{3,100}?)(?=\n|,|;|$)',
    # Company/Organization: XYZ format
    r'(?i)(?:company|organization|employer|worked\s+at)?\s*:?\s*([a-zA-Z0-9\s&\-\.()]{5,100}?)(?=\n|,|;|$)',
    # Job title with years
    r'(?i)((?:junior|senior|associate|lead)?\s*(?:software|web|data|ml)\s+(?:engineer|developer|analyst))\s*\|?\s*([0-9]+\s*(?:years?|yrs?))?(?=\n|,|;|$)',
    # Experience duration patterns (e.g., "5 years of experience")
    r'(?i)([0-9]+(?:\.[0-9])?\s*(?:years?|yrs?|months?|mos?|y))\s+(?:of\s+)?(?:professional\s+)?(?:work|experience|exp)(?=\n|,|;|$)',
    # Internship/Apprenticeship format
    r'(?i)(?:internship|apprenticeship|trainee|intern|co-op)\s+(?:at|in|with)?\s*([a-zA-Z0-9\s&\-\.()]{3,100}?)(?=\n|,|;|$)',
]

# ============================================================================
# CAREER PREDICTION DATASETS - Roles and Skill Mappings
# ============================================================================

CAREER_ROLES = [
    {
        "name": "Data Scientist",
        "slug": "data-scientist",
        "required_skills": ["Python", "Machine Learning", "SQL", "Statistics", "Data Analysis"],
        "optional_skills": ["TensorFlow", "PyTorch", "Deep Learning", "NLP", "Pandas", "NumPy"]
    },
    {
        "name": "Frontend Developer",
        "slug": "frontend-developer",
        "required_skills": ["HTML", "CSS", "JavaScript"],
        "optional_skills": ["React", "Angular", "Vue.js", "TypeScript", "REST API"]
    },
    {
        "name": "Backend Developer",
        "slug": "backend-developer",
        "required_skills": ["Python", "SQL", "REST API"],
        "optional_skills": ["Node.js", "Django", "Flask", "Spring Boot", "MongoDB", "Docker", "Redis"]
    },
    {
        "name": "Full Stack Developer",
        "slug": "fullstack-developer",
        "required_skills": ["JavaScript", "HTML", "CSS", "SQL", "REST API"],
        "optional_skills": ["React", "Node.js", "Python", "MongoDB", "Docker"]
    },
    {
        "name": "ML Engineer",
        "slug": "ml-engineer",
        "required_skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch"],
        "optional_skills": ["Deep Learning", "NLP", "Computer Vision", "Kubernetes", "Docker"]
    },
    {
        "name": "DevOps Engineer",
        "slug": "devops-engineer",
        "required_skills": ["Linux", "Docker", "CI/CD", "AWS"],
        "optional_skills": ["Kubernetes", "Jenkins", "Azure", "GCP", "Networking"]
    },
    {
        "name": "Data Analyst",
        "slug": "data-analyst",
        "required_skills": ["SQL", "Excel", "Data Analysis", "Statistics"],
        "optional_skills": ["Python", "Tableau", "Power BI", "Pandas"]
    },
    {
        "name": "Software Engineer",
        "slug": "software-engineer",
        "required_skills": ["Python", "Data Structures", "Algorithms", "Git"],
        "optional_skills": ["Java", "C++", "SQL", "REST API", "Docker"]
    },
]

# ============================================================================
# JOB RECOMMENDATION DATASETS - Fallback Job Listings
# ============================================================================

FALLBACK_JOBS = [
    {
        "title": "Data Scientist",
        "company": "TechCorp",
        "location": "Remote",
        "url": "https://example.com/job1",
        "skills": ["Python", "ML", "SQL"]
    },
    {
        "title": "Senior Data Scientist",
        "company": "DataInc",
        "location": "Bangalore, India",
        "url": "https://example.com/job2",
        "skills": ["Python", "TensorFlow", "NLP"]
    },
    {
        "title": "Frontend Developer",
        "company": "WebWorks",
        "location": "Hyderabad",
        "url": "https://example.com/job3",
        "skills": ["React", "JavaScript", "CSS"]
    },
    {
        "title": "Full Stack Developer",
        "company": "StartupX",
        "location": "Remote",
        "url": "https://example.com/job4",
        "skills": ["Node.js", "React", "MongoDB"]
    },
    {
        "title": "Backend Engineer",
        "company": "APILabs",
        "location": "Chennai",
        "url": "https://example.com/job5",
        "skills": ["Python", "Django", "PostgreSQL"]
    },
    {
        "title": "ML Engineer",
        "company": "AIM Labs",
        "location": "Mumbai",
        "url": "https://example.com/job6",
        "skills": ["PyTorch", "TensorFlow", "Python"]
    },
    {
        "title": "DevOps Engineer",
        "company": "CloudTech",
        "location": "Pune",
        "url": "https://example.com/job7",
        "skills": ["AWS", "Docker", "Kubernetes"]
    },
    {
        "title": "Data Analyst",
        "company": "AnalyticsPro",
        "location": "Delhi",
        "url": "https://example.com/job8",
        "skills": ["SQL", "Python", "Tableau"]
    },
]

# ============================================================================
# LEARNING RECOMMENDATIONS DATASETS
# ============================================================================

LEARNING_PATHS = {
    "data-scientist": [
        {"course": "Python Fundamentals", "duration": "2 weeks", "priority": "high"},
        {"course": "Statistics & Probability", "duration": "3 weeks", "priority": "high"},
        {"course": "Machine Learning Basics", "duration": "4 weeks", "priority": "high"},
        {"course": "SQL for Data Science", "duration": "2 weeks", "priority": "high"},
        {"course": "TensorFlow & Deep Learning", "duration": "3 weeks", "priority": "medium"},
    ],
    "frontend-developer": [
        {"course": "HTML & CSS Mastery", "duration": "2 weeks", "priority": "high"},
        {"course": "JavaScript Advanced", "duration": "3 weeks", "priority": "high"},
        {"course": "React.js", "duration": "4 weeks", "priority": "high"},
        {"course": "Web Design Principles", "duration": "2 weeks", "priority": "medium"},
        {"course": "TypeScript", "duration": "2 weeks", "priority": "medium"},
    ],
    "backend-developer": [
        {"course": "Python for Backend", "duration": "2 weeks", "priority": "high"},
        {"course": "SQL & Databases", "duration": "3 weeks", "priority": "high"},
        {"course": "REST API Design", "duration": "2 weeks", "priority": "high"},
        {"course": "Django Framework", "duration": "3 weeks", "priority": "high"},
        {"course": "Docker & Deployment", "duration": "2 weeks", "priority": "medium"},
    ],
    "devops-engineer": [
        {"course": "Linux Fundamentals", "duration": "2 weeks", "priority": "high"},
        {"course": "Docker & Containerization", "duration": "3 weeks", "priority": "high"},
        {"course": "AWS Essentials", "duration": "3 weeks", "priority": "high"},
        {"course": "CI/CD Pipelines", "duration": "2 weeks", "priority": "high"},
        {"course": "Kubernetes", "duration": "3 weeks", "priority": "medium"},
    ],
}

LEARNING_RESOURCES = {
    "Python": {
        "courses": ["Python for Everybody (Coursera)", "Automate the Boring Stuff"],
        "certifications": ["PCEP", "PCAP"],
        "youtube": ["Corey Schafer - Python", "freeCodeCamp Python Full Course"],
        "books": ["Python Crash Course - Eric Matthes", "Fluent Python"],
    },
    "Machine Learning": {
        "courses": ["Machine Learning - Andrew Ng (Coursera)", "Deep Learning Specialization"],
        "certifications": ["AWS ML Specialty", "Google ML Engineer"],
        "youtube": ["StatQuest ML", "3Blue1Brown Neural Networks", "Krish Naik ML"],
        "books": ["Hands-On ML - Aurélien Géron"],
    },
    "JavaScript": {
        "courses": ["JavaScript Complete Guide (Udemy)", "Full Stack Open"],
        "certifications": ["Meta Front-End Developer"],
        "youtube": ["freeCodeCamp JavaScript", "Web Dev Simplified"],
        "books": ["You Don't Know JS - Kyle Simpson"],
    },
    "React": {
        "courses": ["React Complete Guide (Udemy)", "Epic React"],
        "certifications": ["Meta React Certificate"],
        "youtube": ["freeCodeCamp React", "Web Dev Simplified React"],
        "books": ["Learning React - Alex Banks"],
    },
    "SQL": {
        "courses": ["SQL for Data Science (Coursera)", "Complete SQL Bootcamp"],
        "certifications": ["Oracle SQL Certified"],
        "youtube": ["freeCodeCamp SQL", "Alex The Analyst SQL"],
        "books": ["SQL Cookbook", "Learning SQL"],
    },
    "HTML": {
        "courses": ["Web Development Bootcamp (Udemy)"],
        "certifications": [],
        "youtube": ["freeCodeCamp HTML", "Traversy Media HTML"],
        "books": ["HTML and CSS - Jon Duckett"],
    },
    "CSS": {
        "courses": ["Advanced CSS and Sass (Udemy)"],
        "certifications": [],
        "youtube": ["Kevin Powell CSS", "Web Dev Simplified CSS"],
        "books": ["CSS in Depth"],
    },
    "Node.js": {
        "courses": ["Complete Node.js Developer (Udemy)"],
        "certifications": ["OpenJS Node.js Certification"],
        "youtube": ["freeCodeCamp Node.js", "Traversy Media Node.js"],
        "books": ["Node.js Design Patterns"],
    },
    "TensorFlow": {
        "courses": ["TensorFlow in Practice (Coursera)"],
        "certifications": ["TensorFlow Developer Certificate"],
        "youtube": ["deeplizard TensorFlow"],
        "books": [],
    },
    "PyTorch": {
        "courses": ["Deep Learning with PyTorch (Udacity)"],
        "certifications": [],
        "youtube": ["Daniel Bourke PyTorch", "Aladdin Persson PyTorch"],
        "books": ["Deep Learning with PyTorch"],
    },
    "Docker": {
        "courses": ["Docker Mastery (Udemy)"],
        "certifications": ["Docker Certified Associate"],
        "youtube": ["TechWorld with Nana Docker", "Fireship Docker"],
        "books": ["Docker Deep Dive"],
    },
    "AWS": {
        "courses": ["AWS Solutions Architect (Udemy)"],
        "certifications": ["AWS Solutions Architect Associate"],
        "youtube": ["freeCodeCamp AWS"],
        "books": ["AWS Certified Solutions Architect"],
    },
    "Data Analysis": {
        "courses": ["Google Data Analytics Certificate"],
        "certifications": ["Google Data Analytics Professional"],
        "youtube": ["Alex The Analyst", "Luke Barousse"],
        "books": ["Storytelling with Data"],
    },
    "Statistics": {
        "courses": ["Statistics with Python (Coursera)"],
        "certifications": [],
        "youtube": ["StatQuest Statistics", "Khan Academy Statistics"],
        "books": ["Practical Statistics for Data Scientists"],
    },
}
