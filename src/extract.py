"""Extract: pull raw data from the three source types into local files.

Sources: a public API (JSON), CSV/JSON files, and a relational database
(SQLite in the demo, PostgreSQL in production via SQLAlchemy).
"""

import json
import sqlite3
from pathlib import Path

import pandas as pd
import requests

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
SAMPLE = BASE / "data" / "sample"


def extract_api(url: str = "https://jsonplaceholder.typicode.com/users") -> Path:
    """Extract a public API endpoint to a raw JSON file."""
    RAW.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    out = RAW / "api_users.json"
    out.write_text(json.dumps(response.json(), indent=2))
    return out


def extract_files() -> list:
    """Register the file-based sources (CSV + JSON) shipped in data/sample."""
    return [SAMPLE / "orders.csv", SAMPLE / "products.json"]


def extract_database(db_path: Path = None) -> Path:
    """Extract a relational table (demo: local SQLite) to a raw CSV file."""
    RAW.mkdir(parents=True, exist_ok=True)
    db_path = db_path or (SAMPLE / "shop.db")
    if not db_path.exists():
        # Build a tiny demo database on first run so the DAG is self-contained
        conn = sqlite3.connect(db_path)
        pd.DataFrame(
            [{"customer_id": i, "name": f"Customer {i}", "city": "Casablanca"}
             for i in range(1, 11)]
        ).to_sql("customers", conn, index=False, if_exists="replace")
        conn.close()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM customers", conn)
    conn.close()
    out = RAW / "db_customers.csv"
    df.to_csv(out, index=False)
    return out


if __name__ == "__main__":
    print(extract_api())
    print(extract_files())
    print(extract_database())
