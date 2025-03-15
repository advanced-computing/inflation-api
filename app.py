#Isaura adds DuckDB codes
from flask import Flask, request, jsonify, abort
from helper import load_data_from_duckdb, filter_by_month
import duckdb 

app = Flask(__name__)

# Loading the dataset - now using duckdb
def get_db_connection():
    return duckdb.connect("my_database.duckdb")

@app.route("/")
def home():
    return "<p>Welcome to the 2025 Fed Inflation Newscast Data API. Go ahead and filter the inflation data by month (01 or 02, e.g., filter?month=1). Soon I will update with more filters.</p>"

@app.route("/sum", methods=["GET"]) #useless - should delete
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
    if month is None:
        abort(400, "Please provide a valid month (e.g., /filter?month=1).")

    # Fetch fresh data from DuckDB
    df = load_data_from_duckdb()
    
    # Use the filter function
    filtered_records = filter_by_month(df, month)

    if filtered_records is None or len(filtered_records) == 0:
        abort(404, "No data available for the selected month.")

    return jsonify(filtered_records)

# Adding POST - Add a User**
@app.route("/users", methods=["POST"])
def add_user():
    """Add a new user to the database."""
    data = request.get_json()

    # Validate request data
    if not data or "username" not in data or "age" not in data or "country" not in data:
        abort(400, "Missing required fields: username, age, and country")

    username = data["username"]
    age = data["age"]
    country = data["country"]

    try:
        con = get_db_connection()
        con.execute("INSERT INTO users VALUES (?, ?, ?);", (username, age, country))
        con.close()
        return jsonify({"message": "✅ User added successfully!", "user": data}), 201
    except Exception as e:
        abort(400, f"Error inserting user: {str(e)}")

# Adding GET - Retrieve All Users**
@app.route("/users", methods=["GET"])
def get_users():
    """Retrieve all users from the database."""
    con = get_db_connection()
    users = con.execute("SELECT * FROM users;").fetchdf()
    con.close()
    return jsonify(users.to_dict(orient="records"))

# Adding GET /users/stats - Get User Statistics
@app.route("/users/stats", methods=["GET"])
def get_user_stats():
    """Return total users, average age, and top 3 countries."""
    con = get_db_connection()
    
    # Query: Get total users, average age, and top 3 countries
    stats = con.execute("""
        WITH country_counts AS (
            SELECT country, COUNT(*) as count FROM users GROUP BY country ORDER BY count DESC LIMIT 3
        )
        SELECT 
            (SELECT COUNT(*) FROM users) AS total_users,
            (SELECT AVG(age) FROM users) AS average_age,
            (SELECT LIST(country) FROM country_counts) AS top_countries;
    """).fetchone()
    
    con.close()

    if stats:
        return jsonify({
            "total_users": stats[0],
            "average_age": round(stats[1], 2) if stats[1] is not None else None,
            "top_countries": stats[2] if stats[2] else []
        })
    else:
        abort(404, "No users found.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
