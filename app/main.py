"""
Main FastAPI application for the AI Lead Scoring system.
"""

from fastapi import FastAPI

from app.schemas import LeadInput, PredictionResponse
from app.services.prediction import predict_lead


app = FastAPI(
    title="AI Lead Scoring API",
    description=(
        "API for predicting lead conversion probability "
        "and assigning lead priority."
    ),
    version="1.0.0"
)


@app.get("/health")
def health_check():
    """
    Check whether the API is running.
    """

    return {
        "status": "healthy",
        "message": "AI Lead Scoring API is running"
    }


@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(lead: LeadInput):
    """
    Generate a lead conversion prediction.
    """

    lead_data = lead.model_dump()

    result = predict_lead(lead_data)

    return result