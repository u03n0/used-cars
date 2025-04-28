from pathlib import Path
import pandas as pd
import logging

# Get the project root directory
project_root = Path(__file__).parent.parent

# Set up logging
log_path = project_root / "logs"
log_path.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=log_path / 'cleaning_dataset_log_file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)
logging.info("Started cleaning dataset.")

clean_path = project_root / "data" / "clean"
clean_path.mkdir(parents=True, exist_ok=True)
logging.info("Created cleaning path: data/clean/.")

# Process and clean the data
try:
    df = pd.read_csv(project_root / 'data' / 'raw' / 'cars.csv')  # Load the CSV file with absolute path
    
    # Rest of your cleaning code...
    df = df.dropna()  # Drop any rows with N/A (missing) data
    df = df.drop_duplicates()
    df = df[df['state'] == 'owned']
    to_drop = ["feature_0", "feature_1", "feature_2", "feature_3", "feature_4", "feature_5", "feature_6", "feature_7", "feature_8", "feature_9", "engine_has_gas",
    'number_of_photos', 'duration_listed', 'up_counter', 'location_region', 'is_exchangeable', 'state', 'engine_type']
    df = df.drop(columns=to_drop)
    df = df.rename(columns={"manufacturer_name": "make", "model_name": "model", "odometer_value": "mileage", "year_produced": "year", "engine_fuel": "fuel",
    "price_usd": "price"})
    to_lower = ['make', 'model', 'transmission', 'color', 'fuel', 'body_type', 'drivetrain']
    for col in to_lower:
        df[col] = df[col].str.lower()
    
    df.to_csv(str(clean_path / 'cars') + '.csv', index=False)  # Save the cleaned data
    logging.info(f"Dataset cleaned successfully to {clean_path}.")
    print("Data cleaned")
except Exception as clean_exception:
    logging.error(f"Failed to clean dataset: {clean_exception}")
    