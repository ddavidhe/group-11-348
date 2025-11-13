import os

import mysql.connector

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

conn = mysql.connector.connect(
    host="localhost", user="root", password="ultraboost", database="racing_db"
)
cursor = conn.cursor()

test_files = ["test_prod1.sql", "test_prod2.sql"]

for test_file in test_files:
    print(f"Processing {test_file}...")

    test_path = os.path.join(SCRIPT_DIR, "tests", test_file)
    with open(test_path, "r") as f:
        test_sql = f.read()

    cursor.execute(test_sql)
    results = cursor.fetchall()

    output_file = test_file.replace(".sql", ".out")
    output_path = os.path.join(SCRIPT_DIR, "outputs", output_file)
    with open(output_path, "w") as f:
        for row in results:
            f.write(f"{row}\n")

    print(f"  Created {output_file}")

cursor.close()
conn.close()

print("\nDone! All production test outputs generated.")
