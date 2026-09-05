import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


load_dotenv()


def load_initial_dataset():

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )

    engine = create_engine(database_url)

    query = """
        SELECT *
        FROM ml_lead_features_initial;
    """

    df = pd.read_sql(query, engine)

    engine.dispose()

    return df


def load_dynamic_dataset():

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )

    engine = create_engine(database_url)

    query = """
        SELECT *
        FROM ml_lead_features_dynamic
        ORDER BY lead_id, snapshot_day;
    """

    df = pd.read_sql(query, engine)

    engine.dispose()

    return df