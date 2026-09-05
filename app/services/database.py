"""
Database access functions for the lead scoring API.
"""

import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


load_dotenv()


def get_database_engine():
    """
    Create a SQLAlchemy engine using environment variables.
    """

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )

    return create_engine(database_url)


def get_initial_lead_features(lead_id: int):
    """
    Retrieve the initial scoring features for one lead.
    """

    engine = get_database_engine()

    query = """
        SELECT *
        FROM ml_lead_features_initial
        WHERE lead_id = %(lead_id)s;
    """

    df = pd.read_sql(
        query,
        engine,
        params={"lead_id": lead_id},
    )

    engine.dispose()

    if df.empty:
        return None

    lead = df.iloc[0].to_dict()

# Never expose the target variable to the prediction model.
    lead.pop("converted", None)

    return lead


def get_dynamic_lead_features(
    lead_id: int,
    snapshot_day: int
):
    """
    Retrieve dynamic scoring features for a lead
    at a specific temporal snapshot.
    """

    engine = get_database_engine()

    query = """
        SELECT *
        FROM ml_lead_features_dynamic
        WHERE lead_id = %(lead_id)s
          AND snapshot_day = %(snapshot_day)s;
    """

    df = pd.read_sql(
        query,
        engine,
        params={
            "lead_id": lead_id,
            "snapshot_day": snapshot_day,
        },
    )

    engine.dispose()

    if df.empty:
        return None

    lead = df.iloc[0].to_dict()

    # Remove target and snapshot metadata.
    lead.pop("converted", None)
    lead.pop("snapshot_day", None)
    lead.pop("lead_id", None)

    return lead

def get_dynamic_lead_history(lead_id: int):
    """
    Retrieve all available dynamic snapshots for a lead.
    """

    engine = get_database_engine()

    query = """
        SELECT *
        FROM ml_lead_features_dynamic
        WHERE lead_id = %(lead_id)s
        ORDER BY snapshot_day;
    """

    df = pd.read_sql(
        query,
        engine,
        params={"lead_id": lead_id},
    )

    engine.dispose()

    if df.empty:
        return None

    return df