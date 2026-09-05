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