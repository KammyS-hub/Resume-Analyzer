# ATS Scoring Engine v2

def calculate_ats_score(resume_text, skills_list):
    score = 0

    resume_text = resume_text.lower()

    # Weight system (IMPORTANT UPGRADE)
    for skill in skills_list:
        if skill.lower() in resume_text:
            score += 10  # base skill match score

    # Bonus scoring rules
    if "project" in resume_text:
        score += 10

    if "internship" in resume_text:
        score += 15

    if "python" in resume_text:
        score += 10

    # Cap score at 100
    return min(score, 100)