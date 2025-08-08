from pathlib import Path
import pandas as pd
import logging

# Get the project root directory
project_root = Path(__file__).parent.parent

# Set up logging
log_path = project_root / "logs"
log_path.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=log_path / 'interim_dataset_log_file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)
logging.info("Started feature engineering the dataset.")

interim_path = project_root / "data" / "interim"
interim_path.mkdir(parents=True, exist_ok=True)
logging.info("Created interim path: data/interim/.")

# Process and clean the data
try:
    df = pd.read_csv(project_root / 'data' / 'clean' / 'cars.csv')  # Load the CSV file with absolute path
    current_year = 2025
    df['age'] = current_year - df['year']

    df['miles_per_year'] = df['mileage'] / df['age']

    # Price per mile
    df['price_per_mile'] = df['price'] / df['mileage']

    # Price per year of age
    df['price_per_year'] = df['price'] / df['age']


    df.to_csv(str(interim_path / 'cars') + '.csv', index=False)  # Save the cleaned data
    logging.info(f"Dataset feature-engineering successfully added to {interim_path}.")
    print("Features Engineered")
except Exception as feature_exception:
    logging.error(f"Failed to engineer features: {feature_exception}")
    
