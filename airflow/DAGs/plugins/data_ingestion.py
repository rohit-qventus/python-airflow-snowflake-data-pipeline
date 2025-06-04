import os
import zipfile
from datetime import datetime


def download_kaggle_dataset(dataset_slug, output_zip_dir):
    """
    Downloads a Kaggle dataset using the Kaggle API command-line tool.
    Returns the absolute path to the downloaded ZIP file.
    """
    os.makedirs(output_zip_dir, exist_ok=True)

    command = f"kaggle datasets download -d {dataset_slug} -p {output_zip_dir} --force"

    print(f"Executing Kaggle download command: {command}")
    return_code = os.system(command)

    if return_code != 0:
        raise Exception(f"Kaggle download failed for dataset: {dataset_slug}. Return code: {return_code}")

    zip_filename = dataset_slug.split('/')[-1] + '.zip'
    downloaded_zip_path = os.path.join(output_zip_dir, zip_filename)

    if not os.path.exists(downloaded_zip_path):
        raise Exception(f"Downloaded ZIP file not found at expected path: {downloaded_zip_path}. Please check Kaggle CLI output.")

    print(f"Successfully downloaded {dataset_slug} to {downloaded_zip_path}")
    return downloaded_zip_path


def extract_zip_files(zip_file_paths, extract_to_dir):
    """
    Extracts content from a list of ZIP files to a specified directory.
    """
    os.makedirs(extract_to_dir, exist_ok=True)
    extracted_csv_paths = []

    for zip_path in zip_file_paths:
        if not os.path.exists(zip_path):
            print(f"Warning: ZIP file not found, skipping extraction: {zip_path}")
            continue

        print(f"Extracting {zip_path} to {extract_to_dir}")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_dir)
                for member in zip_ref.namelist():
                    if member.endswith('.csv'):
                        extracted_csv_paths.append(os.path.join(extract_to_dir, member))
            
            os.remove(zip_path) # Clean up the downloaded ZIP file
            print(f"Cleaned up {zip_path}")

        except zipfile.BadZipFile:
            print(f"Error: {zip_path} is not a valid ZIP file.")
            raise
        except Exception as e:
            print(f"Error extracting {zip_path}: {e}")
            raise

    print(f"Successfully extracted {len(extracted_csv_paths)} CSVs from {len(zip_file_paths)} archives.")
    return extracted_csv_paths