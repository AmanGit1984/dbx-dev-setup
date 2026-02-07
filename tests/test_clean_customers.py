"""Tests for customer data cleaning transformation."""
import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
from src.clean_customers import clean_customers, save_cleaned_data


@pytest.fixture
def sample_customers_csv():
    """Create a temporary customers CSV file for testing."""
    content = """customer_id,name,age,salary,email
1,Alice Johnson,32,75000,alice@example.com
2,Bob Smith,28,65000,bob@example.com
3,Carol White,,72000,carol@example.com
4,David Brown,45,95000,david@example.com
5,Eve Davis,29,,eve@example.com
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    os.unlink(temp_path)


def test_clean_customers_removes_missing_fields(sample_customers_csv):
    """Test that rows with missing age or salary are removed."""
    df = clean_customers(sample_customers_csv)
    
    # Should have 3 valid records (rows 3, 4, 5 removed due to missing age/salary)
    assert len(df) == 3
    assert list(df['customer_id']) == [1, 2, 4]


def test_clean_customers_data_types(sample_customers_csv):
    """Test that age is int and salary is float."""
    df = clean_customers(sample_customers_csv)
    
    assert df['age'].dtype == 'int64'
    assert df['salary'].dtype == 'float64'


def test_clean_customers_age_validation(sample_customers_csv):
    """Test that age values are within valid range."""
    df = clean_customers(sample_customers_csv)
    
    assert (df['age'] >= 18).all()
    assert (df['age'] <= 120).all()


def test_clean_customers_preserves_good_data(sample_customers_csv):
    """Test that valid records are preserved correctly."""
    df = clean_customers(sample_customers_csv)
    
    # Check that known good records exist
    alice = df[df['customer_id'] == 1].iloc[0]
    assert alice['name'] == 'Alice Johnson'
    assert alice['age'] == 32
    assert alice['salary'] == 75000.0


def test_save_cleaned_data():
    """Test that cleaned data can be saved to CSV."""
    df = pd.DataFrame({
        'customer_id': [1, 2],
        'name': ['Alice', 'Bob'],
        'age': [32, 28],
        'salary': [75000.0, 65000.0]
    })
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        temp_path = f.name
    
    try:
        save_cleaned_data(df, temp_path)
        
        # Verify file exists and has correct content
        assert os.path.exists(temp_path)
        df_loaded = pd.read_csv(temp_path)
        assert len(df_loaded) == 2
        assert list(df_loaded['customer_id']) == [1, 2]
    finally:
        os.unlink(temp_path)
