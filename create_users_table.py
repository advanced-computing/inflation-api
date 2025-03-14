import duckdb

con = duckdb.connect("my_database.duckdb")

# Create the 'users' table 
con.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        age INTEGER,
        country TEXT
    );
""")

print("'Users' table created successfully!")

con.close()
