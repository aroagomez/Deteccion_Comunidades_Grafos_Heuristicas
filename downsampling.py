import sqlite3
import os

db_path = "database.sqlite"

# Check if the database file exists
if not os.path.exists(db_path):
    print(f"Database file '{db_path}' not found.")
    exit(1)

# Connect to the original database
try:
    original_conn = sqlite3.connect(db_path)
    original_cursor = original_conn.cursor()
    print(f"Connected to database '{db_path}' successfully.")
except sqlite3.Error as e:
    print(f"Error connecting to database: {e}")
    exit(1)

# Print SQLite version
print("SQLite version:", sqlite3.sqlite_version)

# Fetch entries from sqlite_master
try:
    original_cursor.execute("SELECT name, type FROM sqlite_master;")
    master_entries = original_cursor.fetchall()
    print("Entries in sqlite_master:")
    for entry in master_entries:
        print(f"Name: {entry[0]}, Type: {entry[1]}")
except sqlite3.Error as e:
    print(f"Error querying sqlite_master: {e}")
    exit(1)

# Fetch table names
try:
    original_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in original_cursor.fetchall()]
    print("Tables found:", tables)
except sqlite3.Error as e:
    print(f"Error fetching tables: {e}")
    exit(1)

if not tables:
    print("No tables found in the database. Exiting.")
    exit(1)

# Connect to the original database
original_conn = sqlite3.connect(db_path)
original_cursor = original_conn.cursor()

# Sample percentages and file names
sample_specs = {
    "25": "database_25_sample.sqlite",
    "50": "database_50_sample.sqlite",
    "75": "database_75_sample.sqlite"
}

# Get a list of tables from the original database
original_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [table[0] for table in original_cursor.fetchall()]

for percent, file_name in sample_specs.items():
    # Connect to a new database for each sample
    sample_conn = sqlite3.connect(file_name)
    sample_cursor = sample_conn.cursor()

    print(f"Creating sample database: {file_name} with {percent}% of each table.")


    for table_name in tables:
        # Fetch the table schema from the original database
        original_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        create_table_sql = original_cursor.fetchone()

        if create_table_sql:
            create_table_sql = create_table_sql[0]  # Get the SQL command string
            try:
                # Create the table structure in the sample database
                sample_cursor.execute(create_table_sql)
                sample_conn.commit()  # Commit after table creation
                print(f"Created table {table_name} in {file_name}")
            except Exception as e:
                print(f"Error creating table {table_name}: {e}")


            # Fetch sampled data from the original table
            original_cursor.execute(f"""
                SELECT * FROM {table_name}
                WHERE ABS(RANDOM() % 100) < {percent}
            """)

            rows = original_cursor.fetchall()

            # Insert fetched rows into the new database table
            if rows:  # Check if there are rows to insert
                placeholders = ", ".join(["?"] * len(rows[0]))  # Create placeholders for each column
                try:
                    sample_cursor.executemany(
                        f"INSERT INTO {table_name} VALUES ({placeholders})",
                        rows
                    )
                    sample_conn.commit()  # Commit after inserting data
                    print(f"Inserted {len(rows)} rows into {table_name} in {file_name}")
                except Exception as e:
                    print(f"Error inserting data into {table_name}: {e}")
            else:
                print(f"No rows selected for {table_name} with {percent}% sampling.")

    # Close the sample connection
    sample_conn.close()

# Close the original database connection
original_conn.close()
