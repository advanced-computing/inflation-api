import duckdb

try:
    # Connect to the correct database
    con = duckdb.connect("my_database_temp.duckdb")

    # Execute SQL script to create and load data
    with open("import_data.sql", "r") as f:
        sql_script = f.read()
        con.execute(sql_script)

    print("✅ Data imported successfully!")

    # Check if table exists
    tables = con.execute("SHOW TABLES").fetchall()
    print("Tables in database:", tables)

    # Fetch data if the table exists
    if ("inflation_data",) in tables:
        print(con.execute("SELECT * FROM inflation_data LIMIT 5").fetchall())
    else:
        print("⚠️ Table 'inflation_data' does not exist!")

finally:
    con.close()  # Release the database file