"""Clean and validate customer data."""
import pandas as pd
from pathlib import Path


def clean_customers(input_path: str) -> pd.DataFrame:
    """
    Load customer data, remove rows with missing critical fields,
    and validate data integrity.
    
    Args:
        input_path: Path to customers.csv
    
    Returns:
        Cleaned DataFrame with valid customer records
    """
    df = pd.read_csv(input_path)
    
    # Remove rows with missing age or salary
    df_clean = df.dropna(subset=['age', 'salary'])
    
    # Convert age to integer and salary to float
    df_clean['age'] = df_clean['age'].astype(int)
    df_clean['salary'] = df_clean['salary'].astype(float)
    
    # Remove rows where age is not in valid range (18-120)
    df_clean = df_clean[(df_clean['age'] >= 18) & (df_clean['age'] <= 120)]
    
    return df_clean.reset_index(drop=True)


def save_cleaned_data(df: pd.DataFrame, output_path: str) -> None:
    """Save cleaned customer data to CSV."""
    df.to_csv(output_path, index=False)
