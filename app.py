from flask import Flask, jsonify, request, Response
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("inflation_data.csv")

@app.route("/")
def home():
    return "<p>Welcome to the Inflation Data API</p>"

@app.route("/sum", methods=["GET"])
def sum():
    """Return the sum of two numbers."""
    a = request.args.get("a")
    b = request.args.get("b")
    return jsonify({"sum": int(a) + int(b)})

if __name__ == "__main__":
    app.run(debug=True)
