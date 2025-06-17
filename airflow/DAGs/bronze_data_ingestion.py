from __future__ import annotations

import os
from datetime import datetime
import json
from pathlib import Path  # Import the Path object

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.operators.bash import BashOperator

KAGGLE_CONN_ID = "kaggle_default"

# --- DYNAMIC PATH LOGIC ---
# Get the path to the directory containing this DAG file (e.g., .../airflow/dags)
DAGS_FOLDER = Path(__file__).parent

# Navigate up to the project root directory and then down to the data/raw folder
# Path(__file__).parent                    -> .../dags
# Path(__file__).parent.parent             -> .../airflow
# Path(__file__).parent.parent.parent      -> .../python-airflow-snowflake-data-pipeline/
PROJECT_ROOT = DAGS_FOLDER.parent.parent
LOCAL_RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"
# -------------------------


@dag(
    dag_id="kaggle_download_dynamic_path",
    start_date=datetime(2025, 6, 17),
    schedule_interval=None,
    catchup=False,
    tags=['kaggle', 'dynamic-path'],
    doc_md="""
    ### Kaggle Download DAG with a Dynamic Path
    This DAG calculates the download path relative to the DAG file's location,
    making the project more portable.
    """
)
def kaggle_download_dynamic_path_dag():

    create_download_directory = BashOperator(
        task_id="create_local_raw_data_directory",
        # The LOCAL_RAW_DATA_PATH variable is automatically converted to a string
        bash_command=f"mkdir -p {LOCAL_RAW_DATA_PATH}",
    )

    @task
    def setup_kaggle_credentials():
        """Sets up Kaggle API credentials from Airflow connection."""
        conn = BaseHook.get_connection(KAGGLE_CONN_ID)
        kaggle_dir = os.path.expanduser("~/.kaggle")
        os.makedirs(kaggle_dir, exist_ok=True)
        kaggle_json_path = os.path.join(kaggle_dir, "kaggle.json")
        with open(kaggle_json_path, "w") as f:
            json.dump({"username": conn.login, "key": conn.password}, f)
        os.chmod(kaggle_json_path, 0o600)

    download_dataset = BashOperator(
        task_id="download_and_unzip_dataset",
        bash_command=f"kaggle datasets download ankitbansal06/retail-orders -p {LOCAL_RAW_DATA_PATH} --unzip",
    )

    setup_kaggle_credentials() >> create_download_directory >> download_dataset

# Instantiate the DAG
kaggle_download_dynamic_path_dag()