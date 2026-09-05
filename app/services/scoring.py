"""
Scoring services for V1 and V2 lead scoring models.
"""

from pathlib import Path

import joblib
import pandas as pd

from src.lead_priority import (
    get_priority,
    get_recommended_action,
)
from app.services.database import get_initial_lead_features

from app.services.database import (
    get_initial_lead_features,
    get_dynamic_lead_features,
    get_dynamic_lead_history,
)

# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INITIAL_MODEL_PATH = (
    BASE_DIR
    / "models"
    / "initial"
    / "initial_lead_scoring_model.pkl"
)

DYNAMIC_MODEL_PATH = (
    BASE_DIR
    / "models"
    / "dynamic"
    / "dynamic_lead_scoring_model.pkl"
)


# ============================================================
# LOAD MODELS
# ============================================================

initial_model = joblib.load(INITIAL_MODEL_PATH)
dynamic_model = joblib.load(DYNAMIC_MODEL_PATH)


# ============================================================
# INITIAL LEAD SCORING
# ============================================================

def score_initial_lead(data: dict) -> dict:
    """
    Generate a conversion probability using Model 1.
    """

    df = pd.DataFrame([data])

    probability = initial_model.predict_proba(df)[0, 1]

    priority = get_priority(probability)

    action = get_recommended_action(priority)

    return {
        "conversion_probability": float(probability),
        "priority": priority,
        "recommended_action": action,
    }


# ============================================================
# DYNAMIC LEAD SCORING
# ============================================================

def score_dynamic_lead(data: dict) -> dict:
    """
    Generate a conversion probability using Model 2.
    """

    df = pd.DataFrame([data])

    probability = dynamic_model.predict_proba(df)[0, 1]

    priority = get_priority(probability)

    action = get_recommended_action(priority)

    return {
        "conversion_probability": float(probability),
        "priority": priority,
        "recommended_action": action,
    }

# ============================================================
# DATABASE-BACKED INITIAL SCORING
# ============================================================

def score_initial_lead_by_id(lead_id: int):
    """
    Retrieve a lead from PostgreSQL and generate
    an initial conversion score.
    """

    lead = get_initial_lead_features(lead_id)

    if lead is None:
        return None

    result = score_initial_lead(lead)

    result["lead_id"] = lead_id

    return result


# ============================================================
# DATABASE-BACKED DYNAMIC SCORING
# ============================================================

def score_dynamic_lead_by_id(
    lead_id: int,
    snapshot_day: int
):
    """
    Retrieve a lead's dynamic snapshot from PostgreSQL
    and generate a dynamic conversion score.
    """

    lead = get_dynamic_lead_features(
        lead_id,
        snapshot_day
    )

    if lead is None:
        return None

    result = score_dynamic_lead(lead)

    result["lead_id"] = lead_id

    return result


def score_dynamic_lead_history(lead_id: int):
    """
    Generate dynamic scores for all available
    snapshots of a lead.
    """

    df = get_dynamic_lead_history(lead_id)

    if df is None:
        return None

    scores = []

    for _, row in df.iterrows():

        snapshot_day = int(row["snapshot_day"])

        features = row.to_dict()

        # Remove fields that are not model inputs.
        features.pop("lead_id", None)
        features.pop("snapshot_day", None)
        features.pop("converted", None)

        result = score_dynamic_lead(features)

        scores.append({
            "snapshot_day": snapshot_day,
            "conversion_probability": result[
                "conversion_probability"
            ],
            "priority": result["priority"],
            "recommended_action": result[
                "recommended_action"
            ],
        })

    return {
        "lead_id": lead_id,
        "scores": scores,
    }