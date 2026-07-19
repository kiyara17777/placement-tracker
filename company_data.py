SUGGESTED_WEIGHTS = {
    "google": {
        "sector": "Product/Tech",
        "weights": {"DP": 0.35, "Trees & Graphs": 0.30, "System Design": 0.35}
    },
    "adobe": {
        "sector": "Product/Tech",
        "weights": {"DP": 0.30, "OOP Concepts": 0.30, "Arrays & Strings": 0.20, "CS Fundamentals": 0.20}
    },
    "microsoft": {
        "sector": "Product/Tech",
        "weights": {"DP": 0.35, "Trees & Graphs": 0.25, "CS Fundamentals": 0.20, "OOP Concepts": 0.20}
    },
    "amazon": {
        "sector": "E-commerce/Tech",
        "weights": {"DP": 0.30, "OOP Concepts": 0.20, "System Design": 0.30, "Arrays & Strings": 0.20}
    },
    "apple": {
        "sector": "Product/Tech",
        "weights": {"DP": 0.25, "System Design": 0.30, "OOP Concepts": 0.25, "CS Fundamentals": 0.20}
    },
    "uber": {
        "sector": "Product/Tech",
        "weights": {"System Design": 0.35, "DP": 0.25, "SQL": 0.20, "Trees & Graphs": 0.20}
    },
    "jp morgan": {
        "sector": "Finance",
        "weights": {"DP": 0.30, "SQL": 0.35, "Aptitude": 0.35}
    },
    "netflix": {
        "sector": "Product/Tech",
        "weights": {"System Design": 0.40, "DP": 0.25, "Trees & Graphs": 0.20, "OOP Concepts": 0.15}
    },
    "cisco": {
        "sector": "Networking/Tech",
        "weights": {"CS Fundamentals": 0.35, "DP": 0.25, "OOP Concepts": 0.25, "Arrays & Strings": 0.15}
    },
    "morgan stanley": {
        "sector": "Finance",
        "weights": {"DP": 0.35, "SQL": 0.35, "Aptitude": 0.30}
    },
    "linkedin": {
        "sector": "Product/Tech",
        "weights": {"System Design": 0.35, "DP": 0.30, "Trees & Graphs": 0.20, "SQL": 0.15}
    },
    "jane street": {
        "sector": "Finance/Quant",
        "weights": {"DP": 0.30, "Aptitude": 0.40, "CS Fundamentals": 0.30}
    },
}


def get_suggestion(company_name):
    return SUGGESTED_WEIGHTS.get(company_name.strip().lower())


def get_all_curated_companies():
    """Returns list of (name, sector) for auto-seeding."""
    display_names = {
        "google": "Google", "adobe": "Adobe", "microsoft": "Microsoft",
        "amazon": "Amazon", "apple": "Apple", "uber": "Uber",
        "jp morgan": "JP Morgan", "netflix": "Netflix", "cisco": "Cisco",
        "morgan stanley": "Morgan Stanley", "linkedin": "LinkedIn",
        "jane street": "Jane Street"
    }
    return [(display_names[key], data['sector']) for key, data in SUGGESTED_WEIGHTS.items()]