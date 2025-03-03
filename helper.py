import pandas as pd
from ydata_profiling import ProfileReport

def load_data(filename="inflation_data.csv"):
    """Load dataset and handle errors."""
    try:
        df = pd.read_csv(filename)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None  # Handle missing or corrupt file

def filter_by_month(df, month):
    """Filter dataset by a given month."""
    if month is None or month not in [1, 2]:  # Only January and February available
        return None

    filtered_df = df[df["Date"].dt.month == month]
    return filtered_df.to_dict(orient="records") if not filtered_df.empty else None

#For use within app.py
def generate_profile(df, output_file="profiling_report.html"):
    """Generate and save a profiling report."""
    profile = ProfileReport(df, title="Inflation Data Profiling Report", explorative=True)
    profile.to_file(output_file)
    return output_file  
