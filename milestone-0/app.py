import mysql.connector

# Replace 'root' and 'your_password' with your MySQL root username and password
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS racing_db;")
cursor.execute("USE racing_db;")

# Drop existing tables to start fresh
# will be more annoying as we add foreign keys
cursor.execute("SHOW TABLES;")
for (table_name,) in cursor:
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")  # Drop all tables

with open("schema.sql", "r") as schema_file:
    cursor.execute(schema_file.read())

with open("data.sql", "r") as data_file:
    data_statements = data_file.read().split(';')
    for statement in data_statements:
        if statement.strip():
            cursor.execute(statement)

cursor.execute("SELECT * FROM racers;")
for row in cursor.fetchall():
    print(row)

conn.commit() # save changes
cursor.close()
conn.close()