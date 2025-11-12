import mysql.connector

# Replace 'root' and 'your_password' with your MySQL root username and password
conn = mysql.connector.connect(host="localhost", user="root", password="password")

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
seed("sample_data/sample_results_data.sql", cursor)
seed("sample_data/sample_laps_data.sql", cursor)
seed("sample_data/sample_weather_data.sql", cursor)

with open("queries/feature-1/driver_form.sql", "r") as driver_form:
    driver_form_template = driver_form.read()
    driver_form_template = driver_form_template.format(1, 22, 2021)
    _ = cursor.execute(driver_form_template)
    for row in cursor.fetchall():
        print(row)

with open("queries/feature-2/average_lap.sql", "r") as average_lap:
    average_lap_template = average_lap.read()
    average_lap_template = average_lap_template.format(20, 14)
    _ = cursor.execute(average_lap_template)
    for row in cursor.fetchall():
        print(row)

with open("queries/feature-3/pit_delta.sql", "r") as pit_delta:
    pit_delta_template = pit_delta.read()
    pit_delta_template = pit_delta_template.format(1, 44)
    _ = cursor.execute(pit_delta_template)
    for row in cursor.fetchall():
        print(row)

with open("queries/feature-4/lap_info.sql", "r") as lap_info:
    lap_info_template = lap_info.read()
    lap_info_template = lap_info_template.format(rID=2, lapNumber=63)
    _ = cursor.execute(lap_info_template)
    for row in cursor.fetchall():
        print(row)

_ = conn.commit()  # save changes
_ = cursor.close()
conn.close()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="racing_db",
    use_pure=True,  # required for multi=True
)

cur = conn.cursor(buffered=True)

with open("queries/feature-5/disqualify.sql", "r") as f:
    dq_dID, dq_cID, dq_rID = 44, 8, 1
    sql = f.read().format(dID=dq_dID, cID=dq_cID, rID=dq_rID)

for statement in sql.split(";"):
    stmt = statement.strip()
    if stmt:
        _ = cur.execute(stmt)

# Print updated standings for the race
_ = cur.execute(
    "SELECT dID, cID, rID, finishPos FROM results WHERE rID = %s ORDER BY finishPos ASC",
    (dq_rID,),
)
for row in cur.fetchall():
    print(row)

conn.commit()
cur.close()
conn.close()
