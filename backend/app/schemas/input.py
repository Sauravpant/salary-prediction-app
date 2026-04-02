from pydantic import BaseModel, Field
from typing import Literal


class SalaryPredictionInput(BaseModel):
    """Schema for salary prediction input from frontend"""

    age: int = Field(..., ge=18, le=100, description="Age of the employee (18-100)")
    years_of_experience: float = Field(
        ..., ge=0, le=60, description="Years of work experience"
    )
    education_level: Literal["High School", "Bachelor", "Master", "PhD"] = Field(
        ..., description="Education level of the employee"
    )
    gender: Literal["Male", "Female"] = Field(..., description="Gender of the employee")
    job_title: str = Field(..., description="Job title of the employee")


class SalaryPredictionOutput(BaseModel):
    """Schema for salary prediction output"""

    predicted_salary: float = Field(..., description="Predicted salary")
    input_data: SalaryPredictionInput
