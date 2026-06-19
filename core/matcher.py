ROLE_SKILLS = {
    "Data Analyst": [
        "python",
        "sql",
        "pandas",
        "numpy",
        "data analysis"
    ],

    "Python Developer": [
        "python",
        "flask",
        "django",
        "git",
        "github"
    ],

    "AI Engineer": [
        "python",
        "machine learning",
        "numpy",
        "pandas",
        "git"
    ]
}


def match_role(resume_skills, role):

    required_skills = ROLE_SKILLS.get(role, [])

    matched = []

    missing = []

    for skill in required_skills:

        if skill in resume_skills:
            matched.append(skill)

        else:
            missing.append(skill)

    if len(required_skills) > 0:

        score = round(
            (len(matched) / len(required_skills)) * 100,
            2
        )

    else:
        score = 0

    return {
        "role": role,
        "score": score,
        "matched": matched,
        "missing": missing
    }