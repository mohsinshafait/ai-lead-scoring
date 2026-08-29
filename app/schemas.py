"""
Pydantic schemas for validating API request and response data.
"""
from pydantic import BaseModel

class LeadInput(BaseModel):
    """
    Schema representing the raw lead information required
    by the lead scoring model.
    """

    # Categorical features
    lead_origin: str
    lead_source: str
    country: str
    specialization: str
    heard_about_x_education: str
    current_occupation: str
    course_selection_factor: str
    lead_profile: str
    city: str

    # Binary features
    do_not_email: str
    free_mastering_interview_copy: str

    # Numerical features
    total_visits: float
    total_time_spent_on_website: float
    page_views_per_visit: float

class PredictionResponse(BaseModel):
    """
    Schema representing the prediction returned by the API.
    """

    prediction: str
    conversion_probability: float
    lead_priority: str