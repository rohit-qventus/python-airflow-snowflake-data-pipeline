import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from plugins.data_ingestion import download_kaggle_dataset, extract_zip_files

# --- Dynamic Path Calculation ---
# Get the absolute path of the current DAG file
DAG_FILE_PATH = os.path.abspath(__file__)

# Assuming the structure: your_repo_root/airflow/dags/your_dag_file.py
# Go up two levels from the DAG file to reach the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DAG_FILE_PATH)))

# Construct the absolute path to your raw data directory
LOCAL_RAW_DATA_BASE_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw')
# --- End Dynamic Path Calculation ---

# Define your Kaggle dataset slugs
KAGGLE_ECOMMERCE_SLUG = 'olistbr/brazilian-ecommerce'
KAGGLE_MARKETING_SLUG = 'olistbr/marketing-funnel-olist'

with DAG(
    dag_id='olist_ecommerce_data_ingestion',
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['ecommerce', 'ingestion'],
) as dag:

    # Task 1: Download the main E-commerce dataset ZIP
    download_ecommerce_zip = PythonOperator(
        task_id='download_ecommerce_dataset_zip',
        python_callable=download_kaggle_dataset,
        op_kwargs={
            'dataset_slug': KAGGLE_ECOMMERCE_SLUG,
            # Create a temporary directory for zips inside the raw data path
            'output_zip_dir': os.path.join(LOCAL_RAW_DATA_BASE_PATH, 'zipped_downloads')
        },
    )

    # Task 2: Download the Marketing Funnel dataset ZIP
    download_marketing_funnel_zip = PythonOperator(
        task_id='download_marketing_funnel_dataset_zip',
        python_callable=download_kaggle_dataset,
        op_kwargs={
            'dataset_slug': KAGGLE_MARKETING_SLUG,
            # Create a temporary directory for zips inside the raw data path
            'output_zip_dir': os.path.join(LOCAL_RAW_DATA_BASE_PATH, 'zipped_downloads')
        },
    )

    # Task 3: Extract all downloaded ZIPs to the raw data directory
    extract_all_cs_files = PythonOperator(
        task_id='extract_all_csv_files',
        python_callable=extract_zip_files,
        op_kwargs={
            # XCom pull the paths of the downloaded zips from previous tasks
            'zip_file_paths': [
                "{{ ti.xcom_pull(task_ids='download_ecommerce_dataset_zip') }}",
                "{{ ti.xcom_pull(task_ids='download_marketing_funnel_dataset_zip') }}"
            ],
            'extract_to_dir': LOCAL_RAW_DATA_BASE_PATH # Extract directly into data/raw
        },
    )

    # Define task dependencies
    [download_ecommerce_zip, download_marketing_funnel_zip] >> extract_all_cs_files

    # Future tasks will go here:
    # extract_all_cs_files >> load_raw_to_staging >> ...