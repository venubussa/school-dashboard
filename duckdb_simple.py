import duckdb
import pandas as pd
import os

print("Starting DuckDB test...")

csv_path = r"C:\Users\Venu\Pictures\school-bi\data\students.csv"

if not os.path.exists(csv_path):
    print(f"CSV not found: {csv_path}")
else:
    print(f"CSV found: {csv_path}")

# Load CSV
df = pd.read_csv(csv_path)
print("CSV loaded successfully. Here are first few rows:")
print(df.head())

# Connect to DuckDB
con = duckdb.connect("test_school.db")
print("Connected to DuckDB (test_school.db)")

# Create table
con.register("students_df", df)
con.execute("CREATE TABLE IF NOT EXISTS students AS SELECT * FROM students_df")
print("Table created successfully in DuckDB")

# Fetch and show data
result_df = con.execute("SELECT * FROM students").fetchdf()
print("Fetched data from DuckDB:")
print(result_df)
