# Curated from public interview experiences (GfG, LinkedIn posts, TUF, senior inputs)
# Weights are researched approximations, not live-scraped data.

SUGGESTED_WEIGHTS = {
    "goldman sachs": {
        "sector": "Finance",
        "weights": {"DP": 0.35, "SQL": 0.35, "Aptitude": 0.30}
    },
    "google": {
        "sector": "Product/Tech",
        "weights": {"DP": 0.40, "Trees & Graphs": 0.30, "System Design": 0.30}
    },
    "amazon": {
        "sector": "E-commerce/Tech",
        "weights": {"DP": 0.30, "OOP Concepts": 0.20, "System Design": 0.30, "Arrays & Strings": 0.20}
    },
    "microsoft": {
        "sector": "Product/Tech",
        "weights": {"DP": 0.35, "Trees & Graphs": 0.25, "CS Fundamentals": 0.20, "OOP Concepts": 0.20}
    },
    "morgan stanley": {
        "sector": "Finance",
        "weights": {"DP": 0.35, "SQL": 0.35, "Aptitude": 0.30}
    },
    "flipkart": {
        "sector": "E-commerce/Tech",
        "weights": {"DP": 0.30, "System Design": 0.30, "Arrays & Strings": 0.20, "SQL": 0.20}
    },
    "tcs digital": {
        "sector": "IT Services",
        "weights": {"Aptitude": 0.40, "CS Fundamentals": 0.30, "Arrays & Strings": 0.30}
    },
    "uber": {
        "sector": "Product/Tech",
        "weights": {"System Design": 0.35, "DP": 0.25, "SQL": 0.20, "Trees & Graphs": 0.20}
    },
}


def get_suggestion(company_name):
    """Case-insensitive lookup. Returns None if company isn't in our curated list."""
    return SUGGESTED_WEIGHTS.get(company_name.strip().lower())