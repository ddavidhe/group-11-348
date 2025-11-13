import mysql.connector
from seeding_scripts import *

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)
cursor = conn.cursor()

# Setup database
setup_prod(cursor, conn)

# Loop through test_prod2.sql → test_prod5.sql
for i in range(1, 6):
    sql_file = f"prod_tests/test_prod{i}.sql"
    out_file = f"prod_outputs/test_prod{i}.out"

    with open(sql_file, "r") as query_file:
        sql_query = query_file.read()

    cursor.execute(sql_query)
    rows = cursor.fetchall()

    with open(out_file, "w") as f:
        for row in rows:
            f.write(f"{row}\n")
