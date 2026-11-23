"""Load: write the cleaned tables into PostgreSQL.

Connection comes from the DATABASE_URL environment variable
(default: the docker-compose PostgreSQL service).
"""

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

BASE = Path(__file__).resolve().parent.parent
CLEAN = BASE / "data" / "clean"
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg2://airflow:airflow@localhost:5432/airflow"
)


def load_table(name: str, engine) -> int:
    df = pd.read_csv(CLEAN / f"{name}.csv")
    df.to_sql(name, engine, if_exists="replace", index=False)
    return len(df)


def run_loads() -> dict:
    engine = create_engine(DATABASE_URL)
    return {name: load_table(name, engine) for name in ("orders", "users", "customers")}


if __name__ == "__main__":
    print(run_loads())
