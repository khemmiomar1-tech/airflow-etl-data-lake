"""Airflow DAG - multi-source ETL into PostgreSQL.

Pipeline: extract (API + files + relational DB) -> transform (clean) ->
load (PostgreSQL). Scheduled daily, with retries and failure callbacks so a
failed source is visible instead of silently skipped.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src import extract, load, transform  # noqa: E402


def _alert(context):
    print(f"Task failed: {context['task_instance'].task_id} - {context.get('exception')}")


default_args = {
    "owner": "omar-khemmi",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": _alert,
}

with DAG(
    dag_id="etl_multi_source",
    description="Multi-source ETL: API + CSV/JSON + DB -> clean -> PostgreSQL",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["etl", "portfolio"],
) as dag:

    extract_api = PythonOperator(task_id="extract_api", python_callable=extract.extract_api)
    extract_files = PythonOperator(task_id="extract_files", python_callable=extract.extract_files)
    extract_db = PythonOperator(task_id="extract_database", python_callable=extract.extract_database)
    transform_all = PythonOperator(task_id="transform", python_callable=transform.run_transforms)
    load_all = PythonOperator(task_id="load_postgres", python_callable=load.run_loads)

    [extract_api, extract_files, extract_db] >> transform_all >> load_all
