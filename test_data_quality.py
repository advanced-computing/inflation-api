import pytest
from helper import load_data  

@pytest.fixture
def df():
    """Load the dataset for testing."""
    return load_data()

def test_no_missing_values(df):
    """Test that there are no missing values in the dataset."""
    assert df.isnull().sum().sum() == 0, "There are missing values in the dataset."

def test_no_duplicate_rows(df):
    """Test that there are no duplicate rows."""
    assert df.duplicated().sum() == 0, "Duplicate rows found in the dataset."

def test_standard_deviation_within_range(df):
    """Test that numeric columns have a reasonable standard deviation."""
    numeric_cols = df.select_dtypes(include=["number"])
    
    for col in numeric_cols.columns:
        std_dev = df[col].std()
        assert 0 < std_dev < 5, f"Standard deviation of {col} is out of range: {std_dev}"
