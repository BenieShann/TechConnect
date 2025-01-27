import sqlite3

db_path = './instance/tech_connect.db'

conn = sqlite3.connect(db_path)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Example: Fetch all rows from a table (replace 'users' with your actual table name)
cursor.execute("SELECT * FROM users")

# Fetch all results
rows = cursor.fetchall()

# Display the rows
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
