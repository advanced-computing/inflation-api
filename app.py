from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("inflation_data.csv")

@app.route("/")
def home():
    return "<p>Welcome to the Inflation Data API</p>"

# Endpoint to get all data
@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(df.to_dict(orient="records"))

# Endpoint to filter by a column value
@app.route("/filter", methods=["GET"])
def filter_data():
    column = request.args.get("column")
    value = request.args.get("value")
    
    if column not in df.columns:
        return jsonify({"error": "Invalid column name"}), 400
    
    filtered_df = df[df[column] == value]
    return jsonify(filtered_df.to_dict(orient="records"))

# Endpoint to get summary statistics
@app.route("/summary", methods=["GET"])
def summary():
    return jsonify(df.describe().to_dict())

if __name__ == "__main__":
    app.run(debug=True)
