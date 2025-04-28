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
    