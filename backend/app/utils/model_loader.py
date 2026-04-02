import joblib
import pandas as pd
from pathlib import Path
from app.utils.constants import (
    JOB_CATEGORIES,
    EDUCATION_MAPPING,
)

MODEL_DIR = Path(__file__).parent.parent / "model"
MODEL_PATH = MODEL_DIR / "salary_prediction_model.pkl"


class SalaryPredictionModel:
    """Model loader and preprocessor for salary prediction"""

    def __init__(self):
        self.model = None
        self.expected_features = []
        self.load_model()

    def load_model(self):
        """Load the trained model from pickle file"""
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

        self.model = joblib.load(MODEL_PATH)
        self.expected_features = list(getattr(self.model, "feature_names_in_", []))
        print(f"Model loaded successfully from {MODEL_PATH}")

    def categorize_job_title(self, job_title: str) -> str:
        """Categorize job title into broader categories"""
        job_title_lower = job_title.lower().strip()

        for category, keywords in JOB_CATEGORIES.items():
            if any(keyword in job_title_lower for keyword in keywords):
                return category

        return "Other"

    def preprocess_input(
        self,
        age: int,
        years_of_experience: float,
        education_level: str,
        gender: str,
        job_title: str,
    ) -> pd.DataFrame:
        """Preprocess input data to match training data format"""
        data = {
            "Age": int(age),
            "Years of Experience": float(years_of_experience),
            "Education Level": EDUCATION_MAPPING.get(education_level.lower(), 0),
            "Gender": gender.capitalize(),
            "Job Title": self.categorize_job_title(job_title),
        }

        df = pd.DataFrame([data])

        gender_dummies = pd.get_dummies(df["Gender"], prefix="Gender")
        df = pd.concat([df, gender_dummies], axis=1)
        df.drop("Gender", axis=1, inplace=True)

        for gender_col in ["Gender_Female", "Gender_Male"]:
            if gender_col not in df.columns:
                df[gender_col] = 0

        job_dummies = pd.get_dummies(df["Job Title"], prefix="Job Title")
        df = pd.concat([df, job_dummies], axis=1)
        df.drop("Job Title", axis=1, inplace=True)

        if not self.expected_features:
            raise ValueError(
                "Loaded model does not expose feature_names_in_. Retrain with pandas DataFrame input."
            )

        for col in self.expected_features:
            if col not in df.columns:
                df[col] = 0

        df = df[[col for col in df.columns if col in self.expected_features]]

        df = df[self.expected_features]

        return df

    def predict(
        self,
        age: int,
        years_of_experience: float,
        education_level: str,
        gender: str,
        job_title: str,
    ) -> float:
        """Predict salary based on input features"""
        X = self.preprocess_input(
            age, years_of_experience, education_level, gender, job_title
        )
        predicted_salary = self.model.predict(X)[0]
        return float(predicted_salary)
