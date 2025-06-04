# python-airflow-snowflake-data-pipeline
A Python-based data pipeline that scrapes web data and loads it into Snowflake using Apache Airflow, with structured staging and curated layers for efficient data modeling.


This is a monorepo project managed by a fully automated CICD pipeline using github 

### Data
Data part of this project is kept in the following directories
- airflow
- lambda-function
- lambda-layer
- snowflake
- snowflake-admin
- snowflake-deployment

### Infra
- github
- infra
- modules
- scripts

# DEV_RY_PYTHON_PIPELINE - Python Airflow & Snowflake Data Pipeline

This project sets up an Apache Airflow environment to orchestrate data pipelines interacting with Snowflake and Azure Cloud services.

## Project Structure

(You might want to add a brief overview of your key directories here, e.g.:)

* `airflow/`: Contains Airflow-related files, including:
    * `dags/`: Your Airflow DAG definitions.
    * `logs/`: Airflow task logs (generated at runtime).
    * `plugins/`: (Optional) Custom Airflow plugins.
    * `airflow.cfg`: Airflow configuration file (generated on `db init`).
* `venv/`: Your Python virtual environment (ignored by Git).
* `requirements.txt`: Project dependencies.
* `README.md`: This file.
* (Add any other relevant project directories, e.g., `dbt/`, `notebooks/`, `scripts/`)

## Getting Started

Follow these steps to set up and run the Airflow environment locally.

### 1. Navigate to the Project Root

Open your terminal or command prompt and go to the main project directory:

```bash
cd /path/to/your/project/python-airflow-snowflake-data-pipeline