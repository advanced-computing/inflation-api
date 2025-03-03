import pytest
import pandas as pd
from helper import load_data, filter_by_month

@pytest.fixture
def sample_data():
    """Create a sample DataFrame for testing."""
    data = {"Date": ["2025-01-15", "2025-02-20", "2025-03-10"], "Inflation": [2.1, 2.3, 2.4]}
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

def test_load_data():
    """Test if load_data() loads a valid DataFrame."""
    df = load_data("inflation_data.csv")  # Use test file if needed
    assert df is not None
    assert "Date" in df.columns

def test_filter_by_month_valid(sample_data):
    """Test filtering with valid months."""
    jan_data = filter_by_month(sample_data, 1)
    assert len(jan_data) == 1
    assert jan_data[0]["Inflation"] == 2.1  # First row is January

def test_filter_by_month_invalid(sample_data):
    """Test filtering with an invalid month (should return None)."""
    no_data = filter_by_month(sample_data, 5)  # May doesn't exist in sample
    assert no_data is None
