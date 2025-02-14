from flask import Flask, jsonify, request, Response
import pandas as pd

app = Flask(__name__)

# Load the CSV data
df = pd.read_csv("inflation_data.csv")

@app.route("/")
def home():
    return "<p>Welcome to the Inflation Data API</p>"

# Endpoint to get all data with optional format, limit, and offset
@app.route("/data", methods=["GET"])
def get_data():
    output_format = request.args.get("format", "json").lower()
    limit = request.args.get("limit", type=int, default=len(df))
    offset = request.args.get("offset", type=int, default=0)
    
    filtered_df = df.iloc[offset:offset+limit]
    
    if output_format == "csv":
        return Response(filtered_df.to_csv(index=False), mimetype="text/csv")
    return jsonify(filtered_df.to_dict(orient="records"))

# Endpoint to filter by a column value
@app.route("/filter", methods=["GET"])
def filter_data():
    column = request.args.get("column")
    value = request.args.get("value")
    output_format = request.args.get("format", "json").lower()
    
    if column not in df.columns:
        return jsonify({"error": "Invalid column name"}), 400
    
    filtered_df = df[df[column] == value]
    
    if output_format == "csv":
        return Response(filtered_df.to_csv(index=False), mimetype="text/csv")
    return jsonify(filtered_df.to_dict(orient="records"))

# Endpoint to retrieve a single record by identifier
@app.route("/record", methods=["GET"])
def get_record():
    identifier_column = request.args.get("id_column")
    identifier_value = request.args.get("id_value")
    output_format = request.args.get("format", "json").lower()
    
    if identifier_column not in df.columns:
        return jsonify({"error": "Invalid identifier column"}), 400
    
    record = df[df[identifier_column] == identifier_value]
    
    if record.empty:
        return jsonify({"error": "Record not found"}), 404
    
    if output_format == "csv":
        return Response(record.to_csv(index=False), mimetype="text/csv")
    return jsonify(record.to_dict(orient="records"))

# Endpoint to get summary statistics
@app.route("/summary", methods=["GET"])
def summary():
    return jsonify(df.describe().to_dict())

if __name__ == "__main__":
    app.run(debug=True)
