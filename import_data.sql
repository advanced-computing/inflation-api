-- Attach the DuckDB database
ATTACH 'my_database.duckdb' AS mydb;

-- Create the table if it doesn’t exist
CREATE TABLE IF NOT EXISTS mydb.inflation_data AS
SELECT * FROM read_csv_auto('inflation_data.csv');
