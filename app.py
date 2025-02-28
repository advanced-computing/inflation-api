#Isaura reformats & refactors the API with helper and pytest files 
from flask import Flask, jsonify, request, abort
from helper import load_data, filter_by_month 

app = Flask(__name__)

# Loading the dataset
df = load_data()
if df is None:
    raise SystemExit("Failed to load data. Check your CSV file.")

@app.route("/")
def home():
    return "<p>Welcome to the 2025 Fed Inflation Newscast Data API. Go ahead and filter the inflation data by month (01 or 02, e.g., filter?month=1). Soon I will update with more filters.</p>"

@app.route("/sum", methods=["GET"])
def add():
    """Return the sum of two numbers."""
    a = request.args.get("a", type=int)
    b = request.args.get("b", type=int)
    
    if a is None or b is None:
        abort(400, "Please provide two numbers (e.g., /add?a=5&b=10).")
    
    return jsonify({"sum": a + b})

@app.route("/filter", methods=["GET"])
def filter_data():
    """API filters data by month."""
    month = request.args.get("month", type=int)
    filtered_records = filter_by_month(df, month)

    if filtered_records is None:
        abort(404, "No data available for the selected month.")

    return jsonify(filtered_records)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
