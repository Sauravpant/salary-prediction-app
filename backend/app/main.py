from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.input import SalaryPredictionInput, SalaryPredictionOutput
from app.utils.model_loader import SalaryPredictionModel
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Salary Prediction API",
    description="API for predicting employee salary based on various features",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None


@app.on_event("startup")
async def startup_event():
    """Load model when application starts"""
    global model
    try:
        model = SalaryPredictionModel()
        logger.info("Model loaded successfully on startup")
    except Exception as e:
        logger.error(f"Failed to load model on startup: {str(e)}")
        raise



@app.post("/predict", response_model=SalaryPredictionOutput)
async def predict_salary(input_data: SalaryPredictionInput) -> SalaryPredictionOutput:
  
    if model is None:
        logger.error("Model is not loaded")
        raise HTTPException(
            status_code=500, detail="Model is not loaded. Please try again later."
        )

    try:
        predicted_salary = model.predict(
            age=input_data.age,
            years_of_experience=input_data.years_of_experience,
            education_level=input_data.education_level,
            gender=input_data.gender,
            job_title=input_data.job_title,
        )

        logger.info(
            f"Prediction made for {input_data.job_title} with {input_data.years_of_experience} years experience: {predicted_salary}"
        )

        return SalaryPredictionOutput(
            predicted_salary=round(predicted_salary, 2), input_data=input_data
        )

    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error during prediction: {str(e)}"
        )


@app.get("/")
async def root():

    return {
        "message": "Welcome to Salary Prediction API",
        "endpoints": {"health": "/health", "predict": "/predict", "docs": "/docs"},
    }
