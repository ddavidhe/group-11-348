import mysql.connector
from seeding_scripts import *

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)
cursor = conn.cursor()
setup_prod(cursor, conn)

with open("prod_outputs/test_prod6.out", "w") as f:
    with open("prod_tests/test_prod6.sql", "r") as query:
        _ = cursor.execute(query.read())
        for row in cursor.fetchall():
            to_write = f'{row}\n'
            f.write(to_write)
