import numpy as np
import pandas as pd

def setup_prod(cursor, conn):
    cursor.execute("DROP DATABASE racing_db;")
    cursor.execute("CREATE DATABASE racing_db;")
    cursor.execute("USE racing_db;")

    with open("../../../schema.sql", "r") as schema_file:
        schema_statements = schema_file.read().split(';')
        for statement in schema_statements:
            if statement.strip():
                cursor.execute(statement)

    PATH = '../../../production_data/output_csv/'

    # Drivers
    driver_string = """
                INSERT INTO drivers (dID, firstName, lastName, driverTag, nationality, age) 
                    VALUES (%s, %s, %s, %s, %s, %s)
            """
    driver_df = pd.read_csv(PATH + 'drivers.csv').replace({np.nan: None})
    driver_data = driver_df.to_dict(orient='records')
    driver_values = [list(driver.values()) for driver in driver_data]

    # Constructors
    constructor_string = "INSERT INTO constructors (cID, name) VALUES"
    constructor_df = pd.read_csv(PATH + 'constructor.csv')
    constructor_data = constructor_df.to_dict(orient='records')
    for constructor in constructor_data:
        constructor_string += f" ({constructor['cID']}, \'{constructor['name']}\'),"
    constructor_string = constructor_string[:-1] + ";"

    # Races
    race_string = "INSERT INTO races (rID, trackName, trackCountry, round, season) VALUES"
    race_df = pd.read_csv(PATH + 'race.csv')
    race_data = race_df.to_dict(orient='records')
    for race in race_data:
        race_string += f" ({race['cID']}, \'{race['name']}\', \'{race['country']}\', {race['round']}, {race['season']}),"
    race_string = race_string[:-1] + ";"

    # Results
    result_string = "INSERT INTO results (dID, cID, rID, startPos, finishPos) VALUES"
    result_df = pd.read_csv(PATH + 'result.csv')
    result_data = result_df.to_dict(orient='records')
    for result in result_data:
        result_string += f" ({result['dID']}, {result['cID']}, {result['rID']}, {result['startPos']}, {result['finishPos']}),"
    result_string = result_string[:-1] + ";"

    # Points
    point_string = "INSERT INTO points (season, position, number) VALUES"
    point_df = pd.read_csv(PATH + 'points.csv')
    point_data = point_df.to_dict(orient='records')
    for point in point_data:
        point_string += f" ({point['season']}, {point['position']}, {point['points']}),"
    point_string = point_string[:-1] + ";"

    cursor.executemany(driver_string, driver_values)
    cursor.execute(constructor_string)
    cursor.execute(race_string)
    cursor.execute(result_string)
    cursor.execute(point_string)
    conn.commit()

def setup_prod_opt(cursor, conn, opt):
    cursor.execute("DROP DATABASE racing_db;")
    cursor.execute("CREATE DATABASE racing_db;")
    cursor.execute("USE racing_db;")

    with open("../../../schema.sql", "r") as schema_file:
        schema_statements = schema_file.read().split(';')
        for statement in schema_statements:
            if statement.strip():
                cursor.execute(statement)

    with open("optimizations/" + opt, "r") as schema_file:
        schema_statements = schema_file.read().split(';')
        for statement in schema_statements:
            if statement.strip():
                cursor.execute(statement)

    PATH = '../../../production_data/output_csv/'

    # Drivers
    driver_string = """
                INSERT INTO drivers (dID, firstName, lastName, driverTag, nationality, age) 
                    VALUES (%s, %s, %s, %s, %s, %s)
            """
    driver_df = pd.read_csv(PATH + 'drivers.csv').replace({np.nan: None})
    driver_data = driver_df.to_dict(orient='records')
    driver_values = [list(driver.values()) for driver in driver_data]

    # Constructors
    constructor_string = "INSERT INTO constructors (cID, name) VALUES"
    constructor_df = pd.read_csv(PATH + 'constructor.csv')
    constructor_data = constructor_df.to_dict(orient='records')
    for constructor in constructor_data:
        constructor_string += f" ({constructor['cID']}, \'{constructor['name']}\'),"
    constructor_string = constructor_string[:-1] + ";"

    # Races
    race_string = "INSERT INTO races (rID, trackName, trackCountry, round, season) VALUES"
    race_df = pd.read_csv(PATH + 'race.csv')
    race_data = race_df.to_dict(orient='records')
    for race in race_data:
        race_string += f" ({race['cID']}, \'{race['name']}\', \'{race['country']}\', {race['round']}, {race['season']}),"
    race_string = race_string[:-1] + ";"

    # Results
    result_string = "INSERT INTO results (dID, cID, rID, startPos, finishPos) VALUES"
    result_df = pd.read_csv(PATH + 'result.csv')
    result_data = result_df.to_dict(orient='records')
    for result in result_data:
        result_string += f" ({result['dID']}, {result['cID']}, {result['rID']}, {result['startPos']}, {result['finishPos']}),"
    result_string = result_string[:-1] + ";"

    # Points
    point_string = "INSERT INTO points (season, position, number) VALUES"
    point_df = pd.read_csv(PATH + 'points.csv')
    point_data = point_df.to_dict(orient='records')
    for point in point_data:
        point_string += f" ({point['season']}, {point['position']}, {point['points']}),"
    point_string = point_string[:-1] + ";"

    cursor.executemany(driver_string, driver_values)
    cursor.execute(constructor_string)
    cursor.execute(race_string)
    cursor.execute(result_string)
    cursor.execute(point_string)
    conn.commit()