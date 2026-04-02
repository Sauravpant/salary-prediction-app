JOB_CATEGORIES = {
    "Software Engineering": [
        "software",
        "developer",
        "frontend",
        "backend",
        "full stack",
        "engineer",
        "software engineer",
    ],
    "Data Science & Analytics": ["data scientist", "data analyst", "analytics", "data"],
    "Management": ["manager", "director", "lead", "head", "vp"],
    "Sales": ["sales", "operation", "logistics", "admin"],
    "Marketing": ["marketing"],
    "HR": ["hr", "recruiter", "talent"],
    "Finance": ["finance", "account", "bank", "audit"],
    "Healthcare": ["doctor", "nurse", "medical"],
    "Education": ["teacher", "professor", "educat"],
}

EDUCATION_MAPPING = {"high school": 0, "bachelor": 1, "master": 2, "phd": 3}

EXPECTED_JOB_COLUMNS = [
    "Job Title_Data Science & Analytics",
    "Job Title_Education",
    "Job Title_Finance",
    "Job Title_Healthcare",
    "Job Title_HR",
    "Job Title_Management",
    "Job Title_Marketing",
    "Job Title_Other",
    "Job Title_Sales",
    "Job Title_Software Engineering",
]

FEATURE_ORDER = [
    "Age",
    "Years of Experience",
    "Education Level",
    "Gender_Female",
    "Gender_Male",
    "Job Title_Data Science & Analytics",
    "Job Title_Education",
    "Job Title_Finance",
    "Job Title_Healthcare",
    "Job Title_HR",
    "Job Title_Management",
    "Job Title_Marketing",
    "Job Title_Other",
    "Job Title_Sales",
    "Job Title_Software Engineering",
]
