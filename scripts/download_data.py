import kagglehub
import logging
from pathlib import Path


log_path = Path.cwd() / "logs"
log_path.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=log_path / 'kaggle_dataset_log_file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

logging.info("Started downloading Kaggle dataset.")

custom_path = Path.cwd() / "data"
custom_path.mkdir(parents=True, exist_ok=True)

try:
    path = kagglehub.dataset_download("u03n01t/car-sales", path=custom_path)
    # If successful, log the success
    logging.info(f"Dataset downloaded successfully to {path}.")
    
except Exception as e:
    logging.error(f"Failed to download dataset: {e}")
