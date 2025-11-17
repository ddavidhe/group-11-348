import os
import statistics
import time

import mysql.connector
import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def reset_database(cursor, conn):
    """Reset database to clean state and reload production data"""
    cursor.execute("DROP DATABASE IF EXISTS racing_db;")
    cursor.execute("CREATE DATABASE racing_db;")
    cursor.execute("USE racing_db;")

    schema_path = os.path.join(SCRIPT_DIR, "../../../schema.sql")
    with open(schema_path, "r") as schema_file:
        schema_statements = schema_file.read().split(";")
        for statement in schema_statements:
            if statement.strip():
                cursor.execute(statement)

    PATH = os.path.join(SCRIPT_DIR, "../../../production_data/output_csv/")

    driver_string = """
        INSERT INTO drivers (dID, firstName, lastName, driverTag, nationality, age)
            VALUES (%s, %s, %s, %s, %s, %s)
    """
    driver_df = pd.read_csv(PATH + "drivers.csv").replace({np.nan: None})
    driver_df = driver_df.drop_duplicates(subset=['dID'], keep='first')
    driver_data = driver_df.to_dict(orient="records")
    driver_values = [list(driver.values()) for driver in driver_data]

    constructor_string = "INSERT INTO constructors (cID, name) VALUES"
    constructor_df = pd.read_csv(PATH + "constructor.csv")
    constructor_data = constructor_df.to_dict(orient="records")
    for constructor in constructor_data:
        constructor_string += f" ({constructor['cID']}, '{constructor['name']}'),"
    constructor_string = constructor_string[:-1] + ";"

    race_string = (
        "INSERT INTO races (rID, trackName, trackCountry, round, season) VALUES"
    )
    race_df = pd.read_csv(PATH + "race.csv")
    race_data = race_df.to_dict(orient="records")
    for race in race_data:
        race_string += f" ({race['cID']}, '{race['name']}', '{race['country']}', {race['round']}, {race['season']}),"
    race_string = race_string[:-1] + ";"

    result_string = "INSERT INTO results (dID, cID, rID, startPos, finishPos) VALUES"
    result_df = pd.read_csv(PATH + "result.csv")
    result_data = result_df.to_dict(orient="records")
    for result in result_data:
        result_string += f" ({result['dID']}, {result['cID']}, {result['rID']}, {result['startPos']}, {result['finishPos']}),"
    result_string = result_string[:-1] + ";"

    point_string = "INSERT INTO points (season, position, number) VALUES"
    point_df = pd.read_csv(PATH + "points.csv")
    point_data = point_df.to_dict(orient="records")
    for point in point_data:
        point_string += f" ({point['season']}, {point['position']}, {point['points']}),"
    point_string = point_string[:-1] + ";"

    weather_df = pd.read_csv(PATH + "weather.csv")
    formatted_weather = ",\n".join(
        f"({row['rID']}, {row['Time']}, {row['Rainfall']}, {row['WindSpeed']}, {row['TrackTemp']}, {row['AirTemp']})"
        for _, row in weather_df.iterrows()
    )
    weather_string = (
        "INSERT INTO weather (rID, time, rainFall, windSpeed, trackTemperature, airTemperature) VALUES "
        + formatted_weather
    )

    laps_df = pd.read_csv(PATH + "laps.csv")
    laps_df = laps_df.fillna("NULL")
    formatted_laps = ",\n".join(
        f"({row['dID']},{row['rID']}, {row['LapNumber']}, {row['Speed']}, {row['Time']}, {row['Position']}, {row['PitInTime']}, {row['PitOutTime']})"
        for _, row in laps_df.iterrows()
    )
    laps_string = (
        "INSERT INTO laps (dId, rID, lapNumber, time, finishTime, standing, enterPitTime, exitPitTime) VALUES "
        + formatted_laps
    )

    cursor.executemany(driver_string, driver_values)
    cursor.execute(constructor_string)
    cursor.execute(race_string)
    cursor.execute(result_string)
    cursor.execute(point_string)
    cursor.execute(weather_string)
    cursor.execute(laps_string)
    conn.commit()


def apply_optimization(cursor, conn, opt_num):
    """Apply optimization indexes"""
    if opt_num == 0:
        return

    opt_file = os.path.join(SCRIPT_DIR, f"optimizations/optimization{opt_num}.sql")
    with open(opt_file, "r") as f:
        opt_sql = f.read()
        for statement in opt_sql.split(";"):
            if statement.strip() and not statement.strip().startswith("--"):
                cursor.execute(statement)
    conn.commit()


def run_disqualify_query(cursor, conn, rID, dID, cID):
    """Run the disqualify transaction and return execution time"""
    query_template = """
START TRANSACTION;

UPDATE results
SET finishPos = finishPos - 1
WHERE rID = {rID}
AND finishPos > (
    SELECT finishPos FROM (
        SELECT finishPos
        FROM results
        WHERE dID = {dID} AND cID = {cID} AND rID = {rID}
    ) AS dqpos
);

UPDATE results
SET finishPos = (
    SELECT COUNT(*) FROM (SELECT * FROM results) AS tmp WHERE rID = {rID}
)
WHERE dID = {dID} AND cID = {cID} AND rID = {rID};

COMMIT;
"""
    query = query_template.format(rID=rID, dID=dID, cID=cID)

    start_time = time.time()
    for statement in query.split(";"):
        if statement.strip():
            cursor.execute(statement)
    conn.commit()
    end_time = time.time()

    return end_time - start_time


def main():
    conn = mysql.connector.connect(host="localhost", user="root", password="ultraboost")
    cursor = conn.cursor()

    test_params = {"rID": 1116, "dID": 844, "cID": 131}

    iterations = 100
    results = {}

    print("Feature-5 Production Testing")
    print("=" * 50)
    print(
        f"Test parameters: rID={test_params['rID']}, dID={test_params['dID']}, cID={test_params['cID']}"
    )
    print(f"Iterations per optimization: {iterations}")
    print("=" * 50)

    for opt_num in range(6):
        print(f"\nTesting Optimization {opt_num}...")
        timings = []

        for i in range(iterations):
            reset_database(cursor, conn)

            apply_optimization(cursor, conn, opt_num)

            exec_time = run_disqualify_query(cursor, conn, **test_params)
            timings.append(exec_time)

            if (i + 1) % 10 == 0:
                print(f"  Completed {i + 1}/{iterations} iterations")

        median = statistics.median(timings)
        percentile_99 = statistics.quantiles(timings, n=100)[98]

        results[opt_num] = {"median": median, "p99": percentile_99, "timings": timings}

        print(f"  Median latency: {median:.6f}s")
        print(f"  99th percentile latency: {percentile_99:.6f}s")

    results_path = os.path.join(SCRIPT_DIR, "results/timing_results.txt")
    with open(results_path, "w") as f:
        f.write("Feature-5 Timing Results\n")
        f.write("=" * 50 + "\n")
        f.write(
            f"Test parameters: rID={test_params['rID']}, dID={test_params['dID']}, cID={test_params['cID']}\n"
        )
        f.write(f"Iterations: {iterations}\n\n")

        for opt_num in range(6):
            f.write(f"Optimization {opt_num}:\n")
            f.write(f"  Median latency: {results[opt_num]['median']:.6f}s\n")
            f.write(f"  99th percentile latency: {results[opt_num]['p99']:.6f}s\n\n")

    print("\n" + "=" * 50)
    print("Testing complete! Results saved to results/timing_results.txt")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
