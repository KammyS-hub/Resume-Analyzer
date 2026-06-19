from flask import Flask, render_template, request
import os
import pdfplumber

from core.parser import parse_resume
from core.scorer import calculate_ats_score
from core.link_analyzer import analyze_links

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

SKILL_DB = [
    "python", "java", "c++", "sql",
    "machine learning", "data analysis",
    "git", "github", "flask", "django",
    "pandas", "numpy", "matplotlib",
    "problem solving", "dsa"
]

SECTION_DB = {
    "Education": "education",
    "Projects": "projects",
    "Experience": "experience",
    "Technical Skills": "technical skills",
    "Achievements": "achievements",
    "GitHub": "github",
    "LinkedIn": "linkedin",
    "Certifications": "certification"
}


@app.route("/", methods=["GET", "POST"])
def home():

    score = None
    matched_skills = []
    missing_skills = []
    found_sections = []
    missing_sections = []

    extracted_email = ""
    extracted_phone = ""

    link_score = 0
    link_details = []

    if request.method == "POST":

        file = request.files["resume"]
        job_desc = request.form.get("job_desc", "")

        if file.filename != "":

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            text = ""

            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text

            text_lower = text.lower()

            # ---------- PARSER ----------
            parsed = parse_resume(text)

            extracted_email = parsed["email"]
            extracted_phone = parsed["phone"]
            resume_skills = parsed["skills"]

            # ---------- SECTION CHECK ----------
            for display_name, keyword in SECTION_DB.items():
                if keyword in text_lower:
                    found_sections.append(display_name)
                else:
                    missing_sections.append(display_name)

            # ---------- JOB DESCRIPTION SKILLS ----------
            jd_lower = job_desc.lower()
            jd_skills = [skill for skill in SKILL_DB if skill in jd_lower]

            for skill in jd_skills:
                if skill in resume_skills:
                    matched_skills.append(skill)
                else:
                    missing_skills.append(skill)

            # ---------- ATS SCORE ----------
            score = calculate_ats_score(text, SKILL_DB)

            # ---------- LINK INTELLIGENCE (V3 FEATURE) ----------
            link_result = analyze_links(text)
            link_score = link_result["score"]
            link_details = link_result["details"]

    return render_template(
        "index.html",
        score=score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        found_sections=found_sections,
        missing_sections=missing_sections,
        extracted_email=extracted_email,
        extracted_phone=extracted_phone,
        link_score=link_score,
        link_details=link_details
    )


if __name__ == "__main__":
    app.run(debug=True)