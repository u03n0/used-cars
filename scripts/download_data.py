import logging
from pathlib import Path
import subprocess
import zipfile
import pandas as pd

# Set up logging
log_path = Path.cwd() / "logs"
log_path.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=log_path / 'kaggle_dataset_log_file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

logging.info("Started downloading Kaggle dataset.")

# Define paths
custom_path = Path.cwd() / "data" / "raw"
custom_path.mkdir(parents=True, exist_ok=True)

try:
    # Define the URL and the output zip file location
    url = "https://www.kaggle.com/api/v1/datasets/download/ander289386/cars-germany"
    zip_file_path = custom_path / "cars-germany.zip"

    # Run cURL to download the dataset
    curl_command = [
        "curl", 
        "-L",  # Follow redirects
        "-o", str(zip_file_path),  # Output file
        url  # Dataset URL
    ]
    
    # Run the cURL command
    subprocess.run(curl_command, check=True)
    logging.info(f"Dataset downloaded successfully to {zip_file_path}.")
    
    # Assuming the downloaded file is a zip, extract it
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # List files in the zip (optional)
        zip_ref.printdir()
        
        # Extract all files to the custom path
        zip_ref.extractall(custom_path)
        
        # Find the CSV file (assuming it's the only CSV in the zip)
        csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
        
        if csv_files:
            extracted_csv_path = custom_path / csv_files[0]
            logging.info(f"CSV file extracted: {extracted_csv_path}")
        else:
            logging.error("No CSV file found in the zip.")
            raise FileNotFoundError("No CSV file found in the zip.")
    
    # Now delete the zip file after extraction
    zip_file_path.unlink()  # Remove the zip file
    logging.info(f"Zip file {zip_file_path} removed.")
    
    # Call your custom clean function (once it's implemented)
    clean_path = Path("data/clean")
    clean_path.mkdir(parents=True, exist_ok=True)
    
    # Process and clean the data
    try:
        df = pd.read_csv(extracted_csv_path)  # Load the CSV file
        df = df.dropna()  # Drop any rows with N/A (missing) data
        df = df[df['offerType'] == 'Used']  # Filter only by those that are 'Used'
        cols = ['make', 'model', 'gear', 'fuel']
        for col in cols:
            df[col] = df[col].str.lower()  # Lowercase text columns
        df['hp'] = df['hp'].apply(lambda x: int(x))  # Cast hp to int
        df = df.drop(columns=['offerType'])  # Drop the 'offerType' column
        df.to_csv(str(clean_path / extracted_csv_path.stem) + '.csv' , index=False)  # Save the cleaned data
        logging.info(f"Dataset cleaned successfully to {clean_path}.")
    except Exception as clean_exception:
        logging.error(f"Failed to clean dataset: {clean_exception}")
    
except Exception as e:
    logging.error(f"Failed to download or process dataset: {e}")
