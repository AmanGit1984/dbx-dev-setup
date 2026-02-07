"""Tests for transaction aggregation transformation."""
import pytest
import pandas as pd
import tempfile
import os
from src.aggregate_transactions import aggregate_transactions, save_aggregated_data


@pytest.fixture
def sample_transactions_csv():
    """Create a temporary transactions CSV file for testing."""
    content = """transaction_id,customer_id,amount,transaction_date
101,1,150.00,2024-01-15
102,2,75.50,2024-01-16
103,1,200.00,2024-01-17
104,3,125.00,2024-01-18
105,2,50.25,2024-01-19
106,4,300.00,2024-01-20
107,1,95.00,2024-01-21
108,5,85.50,2024-01-22
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    os.unlink(temp_path)


def test_aggregate_transactions_correct_totals(sample_transactions_csv):
    """Test that transaction amounts are correctly summed per customer."""
    df = aggregate_transactions(sample_transactions_csv)
    
    # Customer 1 should have 3 transactions totaling 445.00
    customer_1 = df[df['customer_id'] == 1].iloc[0]
    assert customer_1['total_amount'] == 445.00
    assert customer_1['transaction_count'] == 3


def test_aggregate_transactions_averages(sample_transactions_csv):
    """Test that average transaction amount is calculated correctly."""
    df = aggregate_transactions(sample_transactions_csv)
    
    # Customer 2 should have avg 62.88 (125.75 / 2)
    customer_2 = df[df['customer_id'] == 2].iloc[0]
    assert customer_2['avg_amount'] == pytest.approx(62.88, abs=0.01)


def test_aggregate_transactions_single_transaction(sample_transactions_csv):
    """Test customers with single transaction."""
    df = aggregate_transactions(sample_transactions_csv)
    
    # Customer 3 has only 1 transaction
    customer_3 = df[df['customer_id'] == 3].iloc[0]
    assert customer_3['transaction_count'] == 1
    assert customer_3['total_amount'] == customer_3['avg_amount']
    assert customer_3['total_amount'] == 125.00


def test_aggregate_transactions_sorting(sample_transactions_csv):
    """Test that results are sorted by customer_id."""
    df = aggregate_transactions(sample_transactions_csv)
    
    customer_ids = list(df['customer_id'])
    assert customer_ids == sorted(customer_ids)


def test_aggregate_transactions_all_customers_included(sample_transactions_csv):
    """Test that all unique customers are included."""
    df = aggregate_transactions(sample_transactions_csv)
    
    # Should have 5 unique customers
    assert len(df) == 5
    assert set(df['customer_id']) == {1, 2, 3, 4, 5}


def test_aggregate_transactions_decimal_precision(sample_transactions_csv):
    """Test that monetary values are rounded to 2 decimals."""
    df = aggregate_transactions(sample_transactions_csv)
    
    # All monetary columns should have max 2 decimal places
    for col in ['total_amount', 'avg_amount']:
        for val in df[col]:
            # Check decimal places
            decimal_str = str(val).split('.')[-1] if '.' in str(val) else '0'
            assert len(decimal_str) <= 2


def test_save_aggregated_data():
    """Test that aggregated data can be saved to CSV."""
    df = pd.DataFrame({
        'customer_id': [1, 2],
        'total_amount': [445.00, 125.75],
        'transaction_count': [3, 2],
        'avg_amount': [148.33, 62.88]
    })
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        temp_path = f.name
    
    try:
        save_aggregated_data(df, temp_path)
        
        # Verify file exists and has correct content
        assert os.path.exists(temp_path)
        df_loaded = pd.read_csv(temp_path)
        assert len(df_loaded) == 2
        assert list(df_loaded['customer_id']) == [1, 2]
    finally:
        os.unlink(temp_path)
