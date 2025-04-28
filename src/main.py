from pathlib import Path
import importlib.util
import sys
import logging
import subprocess
import glob


log_path = Path.cwd() / "logs"  # root folder + 'logs' folder
log_path.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=log_path /'main_pipeline_log_file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)


logging.info("Starting main pipeline execution")

project_root = Path(__file__).parent.parent
raw_data_path = project_root / "data" / "raw" / "cars.csv"
clean_data_path = project_root / "data" / "clean" / "cars.csv"
models_dir = project_root / "models"

#  Check if raw data exists, if not download it
if not raw_data_path.exists():
    logging.info("Raw data not found. Running download script.")
    subprocess.run(["python", str(Path.cwd() / "scripts" / "download_data.py")], check=True)
else:
    logging.info(f"Raw data already exists at {raw_data_path}")

# Check if clean data exists, if not clean the data
if not clean_data_path.exists():
    logging.info("Clean data not found. Running cleaning script.")
    subprocess.run(["python", str(Path.cwd() / "src" / "cleaning.py")], check=True)
else:
    logging.info(f"Clean data already exists at {clean_data_path}")

# Check if model files exist, if not train models
pkl_files = list(models_dir.glob("*.pkl"))
if not pkl_files:
    logging.info("No model files found. Running sklearn pipeline script.")
    models_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(["python", str(Path.cwd() / "src" / "sklearn_pipeline.py")], check=True)
else:
    logging.info(f"Model files already exist in {models_dir}")

logging.info("Pipeline completed successfully")

