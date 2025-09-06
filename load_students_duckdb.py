import os
import duckdb
import pandas as pd

print("Starting the DuckDB data load script...")

# Step 1: CSV path
csv_path = r"C:\Users\Venu\Pictures\school-bi\data\students.csv"

# Step 2: Check if CSV exists
if not os.path.exists(csv_path):
    print(f"CSV file not found at: {csv_path}")
    exit(1)
else:
    print(f"Found CSV file at: {csv_path}")

# Step 3: Load CSV into pandas
try:
    df = pd.read_csv(csv_path)
    print(f"CSV loaded successfully! Rows: {len(df)}")
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit(1)

# Step 4: Connect to DuckDB
try:
    con = duckdb.connect("school.db")  # creates school.db in this folder
    print("Connected to DuckDB (school.db)")
except Exception as e:
    print(f"Error connecting to DuckDB: {e}")
    exit(1)

# Step 5: Create table
try:
    con.register("students_df", df)
    con.execute("CREATE TABLE IF NOT EXISTS students AS SELECT * FROM students_df")
    print("Table 'students' created/updated successfully in DuckDB")
except Exception as e:
    print(f"Error creating table: {e}")
    exit(1)

# Step 6: Fetch and display data
try:
    result_df = con.execute("SELECT * FROM students").fetchdf()
    print("First few rows of 'students' table:")
    print(result_df)
except Exception as e:
    print(f"Error fetching data: {e}")
    exit(1)

print("Script completed successfully!")
