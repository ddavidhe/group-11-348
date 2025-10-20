import mysql.connector

# Replace 'root' and 'your_password' with your MySQL root username and password
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)

cursor = conn.cursor()

_ = cursor.execute("DROP DATABASE racing_db;")
_ = cursor.execute("CREATE DATABASE racing_db;")
_ = cursor.execute("USE racing_db;")

# Create the tables
with open("schema.sql", "r") as schema_file:
    schema_statements = schema_file.read().split(";")
    for statement in schema_statements:
        if statement.strip():
            _ = cursor.execute(statement)


# Seed data
def seed(n, c):
    with open(n, "r") as data_file:
        data_statements = data_file.read().split(";")
        for ds in data_statements:
            if ds.strip():
                c.execute(ds)


seed("sample_data/sample_driver_data.sql", cursor)
seed("sample_data/sample_points_data.sql", cursor)
seed("sample_data/sample_constructors_data.sql", cursor)
seed("sample_data/sample_races_data.sql", cursor)
seed("sample_data/sample_results.sql", cursor)
seed("sample_data/sample_lap_telemetries.sql", cursor)
seed("sample_data/sample_driver_telemetries.sql", cursor)
seed("sample_data/sample_lap.sql", cursor)

with open("queries/feature-1/driver_form.sql", "r") as driver_form:
    driver_form_template = driver_form.read()
    driver_form_template = driver_form_template.format(1, 22, 2021)
    _ = cursor.execute(driver_form_template)
    for row in cursor.fetchall():
        print(row)

with open("queries/feature-2/average_lap.sql", "r") as average_lap:
    average_lap_template = average_lap.read()
    average_lap_template = average_lap_template.format(1, 2)
    _ = cursor.execute(average_lap_template)
    for row in cursor.fetchall():
        print(row)

_ = conn.commit()  # save changes
_ = cursor.close()
conn.close()
