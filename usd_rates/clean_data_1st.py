import pandas as pd
import os

def clean_usd_brl_data(input_file: str, output_file: str):
    """
    Cleans the USD_BRL Historical Data CSV file.
    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to save the cleaned CSV file.
    """
    # Check if the file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return
    
    try:
        # Load the data
        print("Loading data...")
        df = pd.read_csv(input_file)
        print(f"Original dataset shape: {df.shape}")
        
        # Step 1: Remove unnecessary columns (e.g., 'Unnamed' columns)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # Step 2: Standardize column names
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
        print(f"Columns after cleaning: {df.columns.tolist()}")
        
        # Step 3: Convert 'date' column to datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Step 4: Clean numeric data in the 'price' column
        numeric_columns = ['price', 'open', 'high', 'low', 'change_%']
        for col in numeric_columns:
            if col in df.columns:
                # Remove commas and convert to numeric
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.replace('%', ''), errors='coerce')
        
        # Step 5: Drop rows with missing 'date' or 'price'
        df = df.dropna(subset=['date', 'price'])
        
        # Step 6: Remove duplicate rows
        df = df.drop_duplicates()
        
        # Step 7: Sort by date in ascending order
        df = df.sort_values(by='date').reset_index(drop=True)
        
        print(f"Cleaned dataset shape: {df.shape}")
        
        # Save cleaned data to a new file
        df.to_csv(output_file, index=False)
        print(f"Cleaned data saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_csv = "USD_BRL Historical Data.csv"
    output_csv = "USD_BRL_Historical_Data_Cleaned.csv"
    clean_usd_brl_data(input_csv, output_csv)
