"""Aggregate transaction data by customer."""
import pandas as pd


def aggregate_transactions(input_path: str) -> pd.DataFrame:
    """
    Load transaction data and aggregate by customer.
    
    Args:
        input_path: Path to transactions.csv
    
    Returns:
        DataFrame with customer_id, total_amount, transaction_count, avg_amount
    """
    df = pd.read_csv(input_path)
    
    # Convert amount to float
    df['amount'] = df['amount'].astype(float)
    
    # Aggregate by customer_id
    agg_data = df.groupby('customer_id').agg(
        total_amount=('amount', 'sum'),
        transaction_count=('amount', 'count'),
        avg_amount=('amount', 'mean')
    ).reset_index()
    
    # Round monetary values to 2 decimals
    agg_data['total_amount'] = agg_data['total_amount'].round(2)
    agg_data['avg_amount'] = agg_data['avg_amount'].round(2)
    
    return agg_data.sort_values('customer_id')


def save_aggregated_data(df: pd.DataFrame, output_path: str) -> None:
    """Save aggregated transaction data to CSV."""
    df.to_csv(output_path, index=False)
