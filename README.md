# Airflow ETL - Multi-Source Data Lake

A personal Data Engineering project: an **Apache Airflow** pipeline that
collects data from three different source types, cleans it, and loads it
into **PostgreSQL** - the classic "centralise heterogeneous sources" problem,
automated and scheduled instead of run by hand.

## Architecture

```
API (JSON) -------+
CSV / JSON files --+--> Airflow DAG (extract -> transform -> load) -> PostgreSQL
Relational DB -----+        retries + failure callback on every task
```

## Contents

| Path | What it does |
|---|---|
| `dags/etl_multi_source_dag.py` | Daily DAG: 3 parallel extracts -> transform -> load, retries = 2, failure callback |
| `src/extract.py` | API extract (requests), file sources, relational extract (SQLite demo / PostgreSQL in production) |
| `src/transform.py` | Cleaning: deduplication, null handling, type standardisation |
| `src/load.py` | Load cleaned tables into PostgreSQL via SQLAlchemy (`DATABASE_URL`) |
| `docker-compose.yml` | Airflow (webserver + scheduler + init) and PostgreSQL 15 |
| `data/sample/` | Small sample inputs (orders CSV, products JSON) |

## Run it

```bash
docker compose up airflow-init
docker compose up -d
# Airflow UI: http://localhost:8080  ->  enable the `etl_multi_source` DAG
```

Without Docker, the ETL steps also run standalone:

```bash
pip install pandas requests sqlalchemy psycopg2-binary
python src/extract.py && python src/transform.py
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/db python src/load.py
```

## Stack

Apache Airflow - Python - PostgreSQL - Docker - SQL

## Resume (Francais)

Projet personnel d'orchestration ETL avec Apache Airflow : collecte de
donnees heterogenes (API, fichiers CSV/JSON, base relationnelle), nettoyage,
et chargement dans PostgreSQL, avec gestion des erreurs et reprises
d'execution. Le tout conteneurise avec Docker Compose.

---
Omar Khemmi - Data Engineer - Casablanca, Morocco
