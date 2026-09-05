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


class InitialLeadRequest(BaseModel):
    """
    Schema for the V2 initial lead scoring model.
    """

    # Categorical features
    lead_source: str
    campaign: str
    lead_type: str
    decision_maker_type: str
    preferred_contact_method: str
    learner_student_level: str
    city: str
    country: str
    course_name: str
    course_student_level: str
    subject: str
    delivery_mode: str

    # Numerical features
    budget: float
    age_at_lead: int
    duration_weeks: int
    price: float
    budget_price_ratio: float
    budget_gap: float


class DynamicLeadRequest(InitialLeadRequest):
    """
    Schema for the V2 dynamic lead scoring model.

    Extends the initial lead information with
    behavioral and sales activity features.
    """

    # Behavioral features
    total_interactions: int
    website_visits: int
    course_page_views: int
    pricing_page_views: int
    trial_class_requests: int
    email_inquiries: int

    # Sales activity features
    total_sales_actions: int
    phone_calls: int
    whatsapp_followups: int
    email_followups: int
    trial_class_invitations: int
    free_consultations: int
    course_information_sent: int

    # Sales action status
    completed_sales_actions: int
    pending_sales_actions: int

    # Sales action priority
    high_priority_actions: int
    medium_priority_actions: int
    low_priority_actions: int

    # Recency features
    days_since_last_interaction: float | None = None
    days_since_last_sales_action: float | None = None


class V2ScoreResponse(BaseModel):
    """
    Schema representing the prediction returned
    by the V2 lead scoring system.
    """

    lead_id: int | None = None
    conversion_probability: float
    priority: str
    recommended_action: str