"""
Main FastAPI application for the AI Lead Scoring system.
"""
from app.schemas import InitialLeadRequest, DynamicLeadRequest, V2ScoreResponse
from app.services.scoring import score_initial_lead, score_dynamic_lead

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


# Create a basic health endpoint to confirm the API is running
@app.get("/")
def health_check():

    # Return a simple status response
    return {
        "status": "API is running"
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


# ============================================================
# V2 — INITIAL LEAD SCORING
# ============================================================

@app.post("/score/initial", response_model=V2ScoreResponse)
def score_initial(request: InitialLeadRequest):

    result = score_initial_lead(
        request.model_dump()
    )

    return result


# ============================================================
# V2 — DYNAMIC LEAD SCORING
# ============================================================

@app.post("/score/dynamic", response_model=V2ScoreResponse)
def score_dynamic(request: DynamicLeadRequest):

    result = score_dynamic_lead(
        request.model_dump()
    )

    return result