import mysql.connector

# Replace 'root' and 'your_password' with your MySQL root username and password
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)

cursor = conn.cursor()

cursor.execute("DROP DATABASE racing_db;")
cursor.execute("CREATE DATABASE racing_db;")
cursor.execute("USE racing_db;")

# Create the tables
with open("schema.sql", "r") as schema_file:
    schema_statements = schema_file.read().split(';')
    for statement in schema_statements:
        if statement.strip():
            cursor.execute(statement)

# Seed data
def seed(n, c):
    with open(n, "r") as data_file:
        data_statements = data_file.read().split(';')
        for ds in data_statements:
            if ds.strip():
                c.execute(ds)

seed("sample_data/sample_driver_data.sql", cursor)
seed("sample_data/sample_points_data.sql", cursor)
seed("sample_data/sample_constructors_data.sql", cursor)
seed("sample_data/sample_races_data.sql", cursor)
seed("sample_data/sample_results.sql", cursor)

with open("queries/feature-1/driver_form.sql", "r") as driver_form:
    driver_form_template = driver_form.read()
    driver_form_template = driver_form_template.format(1, 22, 2021)
    cursor.execute(driver_form_template)
    for row in cursor.fetchall():
        print(row)

conn.commit() # save changes
cursor.close()
conn.close()