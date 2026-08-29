"""
Service responsible for loading the trained model
and generating lead conversion predictions.
"""

from pathlib import Path

import joblib
import pandas as pd

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Define the path to the exported ML model
MODEL_PATH = PROJECT_ROOT / "models" / "lead_scoring_model.pkl"


# Load the trained ML pipeline once when the application starts
model = joblib.load(MODEL_PATH)


def assign_lead_priority(probability: float) -> str:
    """
    Assign a business priority based on conversion probability.
    """

    if probability >= 0.70:
        return "High"
    elif probability >= 0.40:
        return "Medium"
    else:
        return "Low"


def predict_lead(lead_data: dict) -> dict:
    """
    Generate a conversion prediction for a single lead.
    """

    # Convert API field names to the original feature names
    # expected by the trained ML pipeline
    model_input = {
        "Lead Origin": lead_data["lead_origin"],
        "Lead Source": lead_data["lead_source"],
        "Country": lead_data["country"],
        "Specialization": lead_data["specialization"],
        "How did you hear about X Education":
            lead_data["heard_about_x_education"],
        "What is your current occupation":
            lead_data["current_occupation"],
        "What matters most to you in choosing a course":
            lead_data["course_selection_factor"],
        "Lead Profile": lead_data["lead_profile"],
        "City": lead_data["city"],
        "Do Not Email": lead_data["do_not_email"],
        "A free copy of Mastering The Interview":
            lead_data["free_mastering_interview_copy"],
        "TotalVisits": lead_data["total_visits"],
        "Total Time Spent on Website":
            lead_data["total_time_spent_on_website"],
        "Page Views Per Visit":
            lead_data["page_views_per_visit"]
    }

    # Convert the single lead into a DataFrame
    input_df = pd.DataFrame([model_input])

    # Generate the model prediction
    prediction = model.predict(input_df)[0]

    # Get the probability of conversion (class 1)
    conversion_probability = model.predict_proba(
        input_df
    )[0, 1]

    # Assign business priority
    lead_priority = assign_lead_priority(
        conversion_probability
    )

    # Create a deployment-friendly response
    return {
        "prediction": (
            "Likely to Convert"
            if prediction == 1
            else "Unlikely to Convert"
        ),
        "conversion_probability": round(
            float(conversion_probability), 4
        ),
        "lead_priority": lead_priority
    }