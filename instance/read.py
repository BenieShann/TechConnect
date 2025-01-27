import sqlite3

db_path = './instance/tech_connect.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
