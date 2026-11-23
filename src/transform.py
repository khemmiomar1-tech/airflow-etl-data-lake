"""Transform: clean and unify the raw extracts into analysis-ready tables."""

from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
SAMPLE = BASE / "data" / "sample"
CLEAN = BASE / "data" / "clean"


def clean_orders() -> pd.DataFrame:
    df = pd.read_csv(SAMPLE / "orders.csv", parse_dates=["order_date"])
    df = df.drop_duplicates(subset=["order_id"])
    df = df.dropna(subset=["order_id", "customer_id", "amount"])
    df["amount"] = df["amount"].astype(float)
    df["order_date"] = df["order_date"].dt.date
    return df


def clean_users() -> pd.DataFrame:
    df = pd.read_json(RAW / "api_users.json")
    df = df[["id", "name", "email", "username"]].rename(columns={"id": "user_id"})
    df["email"] = df["email"].str.lower().str.strip()
    return df.drop_duplicates(subset=["user_id"])


def clean_customers() -> pd.DataFrame:
    df = pd.read_csv(RAW / "db_customers.csv")
    df["name"] = df["name"].str.strip()
    df["city"] = df["city"].str.strip().str.title()
    return df.drop_duplicates(subset=["customer_id"])


def run_transforms() -> dict:
    CLEAN.mkdir(parents=True, exist_ok=True)
    tables = {
        "orders": clean_orders(),
        "users": clean_users(),
        "customers": clean_customers(),
    }
    for name, df in tables.items():
        df.to_csv(CLEAN / f"{name}.csv", index=False)
    return tables


if __name__ == "__main__":
    for name, df in run_transforms().items():
        print(name, len(df), "rows")
