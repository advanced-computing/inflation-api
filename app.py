from flask import Flask, jsonify, request, Response
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("inflation_data.csv")
df["Date"] = pd.to_datetime(df["Date"], errors='coerce') #having errors extracting month

@app.route("/")
def home():
    return "<p>Welcome to the 2025 Fed Inflation Newscast Data API. Go ahead and filter the inflation data by month, day, or type (CPI,PCE).</p>"

@app.route("/sum", methods=["GET"])
def sum():
    """Return the sum of two numbers."""
    a = request.args.get("a")
    b = request.args.get("b")
    return jsonify({"sum": int(a) + int(b)})

@app.route("/filter", methods=["GET"])
def filter_data():
    """Filter data by month."""
    month = request.args.get("month", type=int)
    if month is None or month < 1 or month > 2: #my data only has january and feb available
        return jsonify({"error": "Invalid month. Please enter a value between 1 and 2 (until the next month's data becomes available)."}), 400
    
    filtered_df = df[df["Date"].dt.month == month]
    return jsonify(filtered_df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
