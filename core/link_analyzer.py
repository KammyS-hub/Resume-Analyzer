import re

def extract_links(text):
    pattern = r'https?://[^\s]+'
    return re.findall(pattern, text)


def classify_link(url):
    url = url.lower()

    if "github.com" in url:
        return "github"

    if "linkedin.com" in url:
        return "linkedin"

    if any(x in url for x in ["coursera", "udemy", "edx", "skillshare"]):
        return "certificate"

    if any(x in url for x in ["vercel", "netlify", "github.io", "portfolio"]):
        return "portfolio"

    return "other"


# V3 scoring weights (clean + realistic)
WEIGHTS = {
    "github": 5,
    "certificate": 3,
    "linkedin": 2,
    "portfolio": 4,
    "other": 1
}


def analyze_links(text):
    links = extract_links(text)

    if not links:
        return {
            "score": 0,
            "details": []
        }

    total = 0
    details = []

    for link in links:
        t = classify_link(link)
        score = WEIGHTS.get(t, 1)

        total += score

        details.append({
            "link": link,
            "type": t,
            "score": score
        })

    # normalize
    final_score = min(total * 10, 100)

    return {
        "score": final_score,
        "details": details
    }