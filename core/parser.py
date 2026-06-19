import re

SKILL_DB = [
    "python",
    "java",
    "c++",
    "sql",
    "machine learning",
    "data analysis",
    "git",
    "github",
    "flask",
    "django",
    "pandas",
    "numpy",
    "matplotlib",
    "problem solving",
    "dsa"
]


def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)

    if match:
        return match.group().strip()

    return "Not Found"


def extract_phone(text):
    pattern = r"\+?\d[\d\s\-]{8,15}"

    match = re.search(pattern, text)

    if match:
        return match.group().strip()

    return "Not Found"


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILL_DB:

        if skill in text:
            found_skills.append(skill)

    return found_skills


def parse_resume(text):

    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }