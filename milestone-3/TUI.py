import mysql.connector
import numpy as np
import pandas as pd
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Center, Container, VerticalScroll
from textual.widgets import Button, ContentSwitcher, DataTable, Input, RichLog, Static


class F1App(App):
    BINDINGS = [
        Binding("q", "quit", "Quit", show=False, priority=True),
        Binding("escape", "back", "Back", show=False),
    ]
    LOGO = r"""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⢀⣀⣀⣀⠀⠀⠀⠀⢀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⢸⣿⣿⡿⢀⣠⣴⣾⣿⣿⣿⣿⣇⡀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⢸⣿⣿⠟⢋⡙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⡿⠓⡐⠒⢶⣤⣄⡀⠀⠀
    ⠀⠸⠿⠇⢰⣿⣿⡆⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⡷⠈⣿⣿⣉⠁⠀
    ⠀⠀⠀⠀⠀⠈⠉⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠈⠉⠁⠀⠈⠉⠉⠀⠀
    """
    CSS = """
        Screen {
            border: double red;
            margin: 10;
            layout: vertical;
            align-horizontal: center;
        }

        #view {
            border: red;
            height: auto;
            margin: 3 5 1 5;
            layout: vertical;
            align-horizontal: center;
        }

        #logo {
            text-align: center;
            color: red;
        }

        #helper-text {
            text-align: center;
            color: white;
        }

        #seedsample {
            padding: 1;
            align: center middle;
            height: auto;
        }

        #seedprod {
            padding: 1;
            align: center middle;
            height: auto;
        }

        .feature-scroll {
            padding: 1;
            align: center middle;
            content-align: center middle;
            height: auto;
        }

        .feature-input Static {
            text-align: center;
        }

        .feature-input {
            padding: 1;
            align: center middle;
            content-align: center middle;
            height: auto;
        }

        .feature-input Input {
            width: 50%;
            text-align: center;
        }

        .feature-input Button {
            width: auto;
        }

        .feature-output-table {
            width: auto;
            margin-top: 1;
            margin-bottom: 1;
        }

        .status-message {
            width: auto;
        }

        #unseeded-error {
            padding: 1;
            align: center middle;
            height: auto;
        }
    """

    def __init__(self):
        super().__init__()
        self.conn = None
        self.cursor = None
        self.seeded = False

    def _db_add_modifications(self):
        with open("additional_modifications.sql", "r") as schema_file:
            schema_statements = schema_file.read().split(";")
            for statement in schema_statements:
                if statement.strip():
                    self.cursor.execute(statement)
        self.conn.commit()

    def _db_seed_sample(self):
        def seed(n, c):
            with open(n, "r") as data_file:
                data_statements = data_file.read().split(";")
                for ds in data_statements:
                    if ds.strip():
                        c.execute(ds)

        # self.query_one(RichLog).write("Seeding sample database.")
        try:
            self.cursor.execute("DROP DATABASE IF EXISTS racing_db;")
            self.cursor.execute("CREATE DATABASE racing_db;")
            self.cursor.execute("USE racing_db;")

            with open("schema.sql", "r") as schema_file:
                schema_statements = schema_file.read().split(";")
                for statement in schema_statements:
                    if statement.strip():
                        self.cursor.execute(statement)

            seed("sample_data/sample_driver_data.sql", self.cursor)
            seed("sample_data/sample_points_data.sql", self.cursor)
            seed("sample_data/sample_constructors_data.sql", self.cursor)
            seed("sample_data/sample_races_data.sql", self.cursor)
            seed("sample_data/sample_results_data.sql", self.cursor)
            seed("sample_data/sample_laps_data.sql", self.cursor)
            seed("sample_data/sample_weather_data.sql", self.cursor)
            self.conn.commit()
            self.seeded = True
            self.notify("Successfully seeded sample data!")
        except Exception as e:
            self.notify(f"Error: {str(e)}")

    def _db_seed_prod(self):
            # self.query_one(RichLog).write("Seeding production database.")
        try:
            self.cursor.execute("DROP DATABASE IF EXISTS racing_db;")
            self.cursor.execute("CREATE DATABASE racing_db;")
            self.cursor.execute("USE racing_db;")

            with open("schema.sql", "r") as schema_file:
                schema_statements = schema_file.read().split(";")
                for statement in schema_statements:
                    if statement.strip():
                        self.cursor.execute(statement)

            PATH = "production_data/output_csv/"

            # Drivers
            driver_string = """
                INSERT INTO drivers (dID, firstName, lastName, driverTag, nationality, age)
                    VALUES (%s, %s, %s, %s, %s, %s)
            """
            driver_df = pd.read_csv(PATH + "drivers.csv").replace({np.nan: None})
            driver_data = driver_df.to_dict(orient="records")
            driver_values = [list(driver.values()) for driver in driver_data]

            # Constructors
            constructor_string = "INSERT INTO constructors (cID, name) VALUES"
            constructor_df = pd.read_csv(PATH + "constructor.csv")
            constructor_data = constructor_df.to_dict(orient="records")
            for constructor in constructor_data:
                constructor_string += f" ({constructor['cID']}, '{constructor['name']}'),"
            constructor_string = constructor_string[:-1] + ";"

            # Races
            race_string = (
                "INSERT INTO races (rID, trackName, trackCountry, round, season) VALUES"
            )
            race_df = pd.read_csv(PATH + "race.csv")
            race_data = race_df.to_dict(orient="records")
            for race in race_data:
                race_string += f" ({race['cID']}, '{race['name']}', '{race['country']}', {race['round']}, {race['season']}),"
            race_string = race_string[:-1] + ";"

            # Results
            result_string = (
                "INSERT INTO results (dID, cID, rID, startPos, finishPos) VALUES"
            )
            result_df = pd.read_csv(PATH + "result.csv")
            result_data = result_df.to_dict(orient="records")
            for result in result_data:
                result_string += f" ({result['dID']}, {result['cID']}, {result['rID']}, {result['startPos']}, {result['finishPos']}),"
            result_string = result_string[:-1] + ";"

            # Points
            point_string = "INSERT INTO points (season, position, number) VALUES"
            point_df = pd.read_csv(PATH + "points.csv")
            point_data = point_df.to_dict(orient="records")
            for point in point_data:
                point_string += (
                    f" ({point['season']}, {point['position']}, {point['points']}),"
                )
            point_string = point_string[:-1] + ";"

            # Weather
            weather_df = pd.read_csv(PATH + "weather.csv")
            formatted_weather = ",\n".join(
                f"({row['rID']}, {row['Time']}, {row['Rainfall']}, {row['WindSpeed']}, {row['TrackTemp']}, {row['AirTemp']})"
                for _, row in weather_df.iterrows()
            )
            print(formatted_weather)
            weather_string = (
                "INSERT INTO weather (rID, time, rainFall, windSpeed, trackTemperature, airTemperature) VALUES "
                + formatted_weather
            )

            # Laps
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

            self.cursor.executemany(driver_string, driver_values)
            self.cursor.execute(constructor_string)
            self.cursor.execute(race_string)
            self.cursor.execute(result_string)
            self.cursor.execute(point_string)
            self.cursor.execute(weather_string)
            self.cursor.execute(laps_string)
            self.conn.commit()
            self.seeded = True
            self.notify("Successfully seeded production data!")
        except Exception as e:
            self.notify(f"Error: {str(e)}")

    def _db_login(self, username, password):
        try:
            self.conn = mysql.connector.connect(
                host="localhost", user=username, password=password
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute("SHOW DATABASES LIKE 'racing_db';")
            rows = self.cursor.fetchall()
            if not rows:
                self.notify(f"The database is not seeded!")
                return True
            else:
                self.cursor.execute("USE racing_db;")
                self.seeded = True
                return True
        except Exception as e:
            self.notify(f"Error: {str(e)}")
            return False

    def _count_rounds(self, season):
        self.cursor.execute(f"SELECT COUNT(*) FROM races WHERE season = {season}")
        return self.cursor.fetchone()[0]
    
    def _driverInRace(self, rID, dID):
        self.cursor.execute(
            f"SELECT EXISTS(SELECT 1 FROM laps WHERE rID = {rID} AND dID = {dID})")
        return bool(self.cursor.fetchone()[0])

    def _db_query_feature1(self, s, e, season):
        with open("queries/feature-1/driver_form.sql", "r") as driver_form:
            driver_form_template = driver_form.read()
            driver_form_template = driver_form_template.format(s, e, season)
            self.cursor.execute(driver_form_template)
            table = self.query_one("#feature1-table", DataTable)
            table.add_columns("First Name", "Last Name", "CODE", "Points")
            table.add_rows(self.cursor.fetchall())
            table.cursor_type = "row"
            table.zebra_stripes = True

    def _reset_feature1(self):
        self.query_one(
            "#feature1-switcher", ContentSwitcher
        ).current = "feature1-interface"
        table = self.query_one("#feature1-table", DataTable)
        self.query_one("#feature1-season", Input).value = ""
        self.query_one("#feature1-start", Input).value = ""
        self.query_one("#feature1-end", Input).value = ""
        table.clear(columns=True)

    def _db_query_feature2(self, rID, dID):
        with open("queries/feature-2/average_lap.sql", "r") as average_lap:
            average_lap_template = average_lap.read()
            average_lap_template = average_lap_template.format(rID, dID)
            self.cursor.execute(average_lap_template)
            table = self.query_one("#feature2-table", DataTable)
            table.add_columns("Average Lap Speed")
            table.add_rows(self.cursor.fetchall())
            table.cursor_type = "row"
            table.zebra_stripes = True

    def _reset_feature2(self):
        self.query_one(
            "#feature2-switcher", ContentSwitcher
        ).current = "feature2-interface"
        table = self.query_one("#feature2-table", DataTable)
        self.query_one("#feature2-raceid", Input).value = ""
        self.query_one("#feature2-driverid", Input).value = ""
        table.clear(columns=True)

    def _db_query_feature3(self, rID, dID):
        with open("queries/feature-3/pit_delta.sql", "r") as pit_delta:
            pit_delta_template = pit_delta.read()
            pit_delta_template = pit_delta_template.format(raceID=rID, driverID=dID)
            self.cursor.execute(pit_delta_template)
            table = self.query_one("#feature3-table", DataTable)
            table.add_columns("Lap Number", "First Lap Time", "Pit Time", "Pit Delta")
            table.add_rows(self.cursor.fetchall())
            table.cursor_type = "row"
            table.zebra_stripes = True
    
    def _reset_feature3(self):
        self.query_one(
            "#feature3-switcher", ContentSwitcher
        ).current = "feature3-interface"
        table = self.query_one("#feature3-table", DataTable)
        self.query_one("#feature3-raceid", Input).value = ""
        self.query_one("#feature3-driverid", Input).value = ""
        table.clear(columns=True)

    def _db_query_feature4(self, rID, lap_number):
        with open("queries/feature-4/lap_info.sql", "r") as lap_info:
            lap_info_template = lap_info.read()
            lap_info_template = lap_info_template.format(rID=rID, lapNumber=lap_number)
            self.cursor.execute(lap_info_template)
            table = self.query_one("#feature4-table", DataTable)
            table.add_columns("First Name", "Last Name", "CODE", "Time", "Start Position", "Finish Position")
            table.add_rows(self.cursor.fetchall())
            table.cursor_type = "row"
            table.zebra_stripes = True
    
    def _reset_feature4(self):
        self.query_one(
            "#feature4-switcher", ContentSwitcher
        ).current = "feature4-interface"
        table = self.query_one("#feature4-table", DataTable)
        self.query_one("#feature4-raceid", Input).value = ""
        self.query_one("#feature4-lap-number", Input).value = ""
        table.clear(columns=True)

    def _db_query_feature5(self, rID, dID, cID):
        try:
            with open("queries/feature-5/disqualify.sql", "r") as disqualify:
                disqualify_template = disqualify.read()
                disqualify_template = disqualify_template.format(rID=rID, dID=dID, cID=cID)
                # Execute the transaction
                for statement in disqualify_template.split(";"):
                    if statement.strip():
                        self.cursor.execute(statement)
                self.conn.commit()
                self.notify("Successfully disqualified the driver!")
                return True
        except Exception as e:
            self.notify(f"Error: {str(e)}")
            return False

    def _reset_feature5(self):
        self.query_one(
            "#feature5-switcher", ContentSwitcher
        ).current = "feature5-interface"
        self.query_one("#feature5-raceid", Input).value = ""
        self.query_one("#feature5-driverid", Input).value = ""
        self.query_one("#feature5-constructorid", Input).value = ""

    def _db_query_advanced_feature1(self, dname, rname):
        with open("advanced/feature-1/driver_track_history.sql", "r") as driver_track_history:
            driver_track_history_template = driver_track_history.read()
            driver_track_history_template = driver_track_history_template.format(dname, rname)
            self.cursor.execute(driver_track_history_template)
            table = self.query_one("#advancedfeature1-table", DataTable)
            table.add_columns("First Name", "Last Name", "Track Name", "Track Country", "Race Count", "Average Qualifying", "Average Finish")
            rows = self.cursor.fetchall()
            if not rows:
                self.notify("No results found.")
            table.add_rows(rows)
            table.cursor_type = "row"
            table.zebra_stripes = True

    def _reset_advanced_feature1(self):
        self.query_one(
            "#advancedfeature1-switcher", ContentSwitcher
        ).current = "advancedfeature1-interface"
        table = self.query_one("#advancedfeature1-table", DataTable)
        self.query_one("#advancedfeature1-dname", Input).value = ""
        self.query_one("#advancedfeature1-rname", Input).value = ""
        table.clear(columns=True)

    def _db_advanced_feature2a(self, username, password):
        create_user_template = "CREATE USER '{}'@'localhost' IDENTIFIED BY '{}';"
        grant_user_template = "GRANT SELECT ON racing_db.* TO '{}'@'localhost';"
        create_user_template = create_user_template.format(username, password)
        grant_user_template = grant_user_template.format(username)
        try:
            self.cursor.execute(create_user_template)
            self.cursor.execute(grant_user_template)
            self.conn.commit()
            self.notify("User has been created.")
        except Exception as e:
            self.notify(f"Error: {str(e)}")

    def _reset_advanced_feature2a(self):
        self.query_one("#advancedfeature2a-username", Input).value = ""
        self.query_one("#advancedfeature2a-password", Input).value = ""

    def _db_advanced_feature2b(self, username):
        grant_user_template = "GRANT ALL ON racing_db.* TO '{}'@'localhost';"
        grant_user_template = grant_user_template.format(username)
        try:
            self.cursor.execute(grant_user_template)
            self.conn.commit()
            self.notify("User has been granted all permissions.")
        except Exception as e:
            self.notify(f"Error: {str(e)}")

    def _reset_advanced_feature2b(self):
        self.query_one("#advancedfeature2b-username", Input).value = ""

    def compose(self) -> ComposeResult:
        yield Static(self.LOGO, id="logo")

        with ContentSwitcher(id="view", initial="login"):
            with Container(id="login", classes="feature-input"):
                yield Static(
                    "Please Login."
                )
                with Center():
                    yield Input(
                        placeholder="Username",
                        id="username",
                        type="text",
                    )
                with Center():
                    yield Input(
                        placeholder="Password",
                        id="password",
                        type="text",
                    )
                with Center():
                    yield Button("Go", id="login")

            yield DataTable(id="feature-table", classes="feature-output-table")

            with VerticalScroll(id="seedsample"):
                yield Button(
                    "Seed the database with sample data.", id="seed-sample-btn"
                )

            with VerticalScroll(id="seedprod"):
                yield Button(
                    "Seed the database with production data.", id="seed-prod-btn"
                )

            with Container(id="unseeded-error"):
                yield Static("Please seed the database first.")

            with VerticalScroll(id="feature1", classes="feature-scroll"):
                with ContentSwitcher(
                    id="feature1-switcher", initial="feature1-interface"
                ):
                    with Container(id="feature1-interface", classes="feature-input"):
                        yield Static(
                            "Please input a season, starting round, and an ending round."
                        )
                        with Center():
                            yield Input(
                                placeholder="Season...",
                                id="feature1-season",
                                type="integer",
                            )
                        with Center():
                            yield Input(
                                placeholder="Start...",
                                id="feature1-start",
                                type="integer",
                            )
                        with Center():
                            yield Input(
                                placeholder="End...", id="feature1-end", type="integer"
                            )
                        with Center():
                            yield Button("Go", id="feature1-go")
                    with Center(id="feature1-table-container"):
                        yield DataTable(id="feature1-table", classes="feature-output-table")

            with VerticalScroll(id="feature2", classes="feature-scroll"):
                with ContentSwitcher(
                    id="feature2-switcher", initial="feature2-interface"
                ):
                    with Container(id="feature2-interface", classes="feature-input"):
                        with Center():
                            yield Static("Please input a raceID and a driverID")
                        with Center():
                            yield Input(placeholder="Race ID...", id="feature2-raceid", type="integer")
                        with Center():
                            yield Input(placeholder="Driver ID...", id="feature2-driverid", type="integer")
                        with Center():
                            yield Button("Go", id="feature2-go")
                    with Center(id="feature2-table-container"):
                        yield DataTable(id="feature2-table", classes="feature-output-table")

            with VerticalScroll(id="feature3", classes="feature-scroll"):
                with ContentSwitcher(
                    id="feature3-switcher", initial="feature3-interface"
                ):
                    with Container(id="feature3-interface", classes="feature-input"):
                        with Center():
                            yield Static("Please input a raceID and a driverID")
                        with Center():
                            yield Input(placeholder="Race ID...", id="feature3-raceid", type="integer")
                        with Center():
                            yield Input(placeholder="Driver ID...", id="feature3-driverid", type="integer")
                        with Center():
                            yield Button("Go", id="feature3-go")
                    with Center(id="feature3-table-container"):
                        yield DataTable(id="feature3-table", classes="feature-output-table")
            
            with VerticalScroll(id="feature4", classes="feature-scroll"):
                with ContentSwitcher(
                    id="feature4-switcher", initial="feature4-interface"
                ):
                    with Container(id="feature4-interface", classes="feature-input"):
                        with Center():
                            yield Static("Please input a race ID and a lap number.")
                        with Center():
                            yield Input(
                                placeholder="Race ID...",
                                id="feature4-raceid",
                                type="integer",
                            )
                        with Center():
                            yield Input(
                                placeholder="Lap number...",
                                id="feature4-lap-number",
                                type="integer",
                            )
                        with Center():
                            yield Button("Go", id="feature4-go")
                    with Center(id="feature4-table-container"):
                        yield DataTable(id="feature4-table", classes="feature-output-table")

            with VerticalScroll(id="feature5", classes="feature-scroll"):
                with ContentSwitcher(
                    id="feature5-switcher", initial="feature5-interface"
                ):
                    with Container(id="feature5-interface", classes="feature-input"):
                        with Center():
                            yield Static(
                                "Please input a race ID, driver ID, and constructor ID to disqualify a driver."
                            )
                        with Center():
                            yield Input(
                                placeholder="Race ID...",
                                id="feature5-raceid",
                                type="integer",
                            )
                        with Center():
                            yield Input(
                                placeholder="Driver ID...",
                                id="feature5-driverid",
                                type="integer",
                            )
                        with Center():
                            yield Input(
                                placeholder="Constructor ID...",
                                id="feature5-constructorid",
                                type="integer",
                            )
                        with Center():
                            yield Button("Disqualify", id="feature5-go")
                    with Center(id="feature5-success"):
                        yield Static("Driver successfully disqualified!", classes="status-message")
                    with Center(id="feature5-failure"):
                        yield Static("Driver could not be disqualified!", classes="status-message")

            with VerticalScroll(id="advancedfeature1", classes="feature-scroll"):
                with ContentSwitcher(
                    id="advancedfeature1-switcher", initial='advancedfeature1-interface'
                ):
                    with Container(id="advancedfeature1-interface", classes="feature-input"):
                        with Center():
                            yield Static(
                                "Please input a driver's name and a race's name to see the history."
                            )
                        with Center():
                            yield Input(
                                placeholder="Driver Name...",
                                id="advancedfeature1-dname",
                                type="text",
                            )
                        with Center():
                            yield Input(
                                placeholder="Race Name...",
                                id="advancedfeature1-rname",
                                type="text",
                            )
                        with Center():
                            yield Button("Go", id="advancedfeature1-go")
                    with Center(id="advancedfeature1-table-container"):
                        yield DataTable(id="advancedfeature1-table", classes="feature-output-table")

            with VerticalScroll(id="advancedfeature2a", classes="feature-scroll"):
                with Container(id="advancedfeature2a-interface", classes="feature-input"):
                    yield Static(
                        "Create an account."
                    )
                    with Center():
                        yield Input(
                            placeholder="Username",
                            id="advancedfeature2a-username",
                            type="text",
                        )
                    with Center():
                        yield Input(
                            placeholder="Password",
                            id="advancedfeature2a-password",
                            type="text",
                        )
                    with Center():
                        yield Button("Go", id="advancedfeature2a-go")

            with VerticalScroll(id="advancedfeature2b", classes="feature-scroll"):
                with Container(id="advancedfeature2b-interface", classes="feature-input"):
                    yield Static(
                        "Grant full permissions to an account."
                    )
                    with Center():
                        yield Input(
                            placeholder="Username",
                            id="advancedfeature2b-username",
                            type="text",
                        )
                    with Center():
                        yield Button("Go", id="advancedfeature2b-go")
        # yield RichLog()

        yield Static(
            "Press \[Enter] to select a feature, press \[Escape] to go back, and press \[q] to quit.",
            id="helper-text",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "login":
            username = self.query_one("#username", Input).value
            password = self.query_one("#password", Input).value
            if self._db_login(username, password):
                self.query_one("#view", ContentSwitcher).current = "feature-table"
                self.query_one("#feature-table", DataTable).focus()
        if button_id == "seed-sample-btn":
            self._db_seed_sample()
            if self.seeded:
                self._db_add_modifications()
        if button_id == "seed-prod-btn":
            self._db_seed_prod()
            if self.seeded:
                self._db_add_modifications()
        if button_id == "feature1-go":
            season = self.query_one("#feature1-season", Input).value
            s = self.query_one("#feature1-start", Input).value
            e = self.query_one("#feature1-end", Input).value
            if season == "" or s == "" or e == "":
                self.notify("Please fill out all fields.")
                return
            rounds = self._count_rounds(season)
            if int(season) < 1989 or int(season) > 2024:
                self.notify("Please input a season between 1989 and 2024 (inclusive).")
            elif int(s) < 1 or int(s) > int(e):
                self.notify("Please input a valid starting round.")
            elif int(e) < 1 or int(e) > int(rounds):
                self.notify(
                    f"Please input a valid ending round. There are {rounds} rounds in the {season} season."
                )
            else:
                self._db_query_feature1(s, e, season)
                self.query_one(
                    "#feature1-switcher", ContentSwitcher
                ).current = "feature1-table-container"
                self.query_one("#feature1-table", DataTable).focus()
        if button_id == "feature2-go":
            rID = self.query_one("#feature2-raceid", Input).value
            dID = self.query_one("#feature2-driverid", Input).value
            if rID == "" or dID == "":
                self.notify("Please fill out all fields.")
                return
            elif int(rID) < 1 or int(dID) < 1:
                self.notify("Please input a valid ID")
                return
            elif not self._driverInRace(rID, dID):
                self.notify(f"Driver {dID} did not race in race {rID}.")
                return
            self._db_query_feature2(rID, dID)
            self.query_one(
                "#feature2-switcher", ContentSwitcher
            ).current = "feature2-table-container"
            self.query_one("#feature2-table", DataTable).focus()
        if button_id == "feature3-go":
            rID = self.query_one("#feature3-raceid", Input).value
            dID = self.query_one("#feature3-driverid", Input).value
            if rID == "" or dID == "":
                self.notify("Please fill out all fields.")
                return
            elif int(rID) < 1 or int(dID) < 1:
                self.notify("Please input a valid ID")
                return
            elif not self._driverInRace(rID, dID):
                self.notify(f"Driver {dID} did not race in race {rID}.")
                return
            self._db_query_feature3(rID, dID)
            self.query_one(
                "#feature3-switcher", ContentSwitcher
            ).current = "feature3-table-container"
            self.query_one("#feature3-table", DataTable).focus()
        if button_id == "feature4-go":
            rID = self.query_one("#feature4-raceid", Input).value
            lap_number = self.query_one("#feature4-lap-number", Input).value
            if rID == "" or lap_number == "":
                self.notify("Please fill out all fields.")
                return
            self._db_query_feature4(rID, lap_number)
            self.query_one(
                "#feature4-switcher", ContentSwitcher
            ).current = "feature4-table-container"
            self.query_one("#feature4-table", DataTable).focus()
        if button_id == "feature5-go":
            rID = self.query_one("#feature5-raceid", Input).value
            dID = self.query_one("#feature5-driverid", Input).value
            cID = self.query_one("#feature5-constructorid", Input).value
            if rID == "" or dID == "" or cID == "":
                self.notify("Please fill out all fields.")
                return
            resp = self._db_query_feature5(rID, dID, cID)
            if resp:
                self.query_one(
                    "#feature5-switcher", ContentSwitcher
                ).current = "feature5-success"
                self.notify("Driver successfully disqualified!")
            else:
                self.query_one(
                    "#feature5-switcher", ContentSwitcher
                ).current = "feature5-failure"
        if button_id == "advancedfeature1-go":
            dname = self.query_one("#advancedfeature1-dname", Input).value
            rname = self.query_one("#advancedfeature1-rname", Input).value
            if rname == "" or dname == "":
                self.notify("Please fill out all fields.")
                return
            self._db_query_advanced_feature1(dname, rname)
            self.query_one(
                "#advancedfeature1-switcher", ContentSwitcher
            ).current = "advancedfeature1-table-container"
        if button_id == "advancedfeature2a-go":
            username = self.query_one("#advancedfeature2a-username", Input).value
            password = self.query_one("#advancedfeature2a-password", Input).value
            if username == "" or password == "":
                self.notify("Please fill out all fields.")
                return
            self._db_advanced_feature2a(username, password)
        if button_id == "advancedfeature2b-go":
            username = self.query_one("#advancedfeature2b-username", Input).value
            if username == "":
                self.notify("Please fill out all fields.")
                return
            self._db_advanced_feature2b(username)

    def action_back(self) -> None:
        if self.cursor is None:
            return
        self._reset_feature1()
        self._reset_feature2()
        self._reset_feature3()
        self._reset_feature4()
        self._reset_feature5()
        self._reset_advanced_feature1()
        self._reset_advanced_feature2a()
        self._reset_advanced_feature2b()
        self.query_one("#view", ContentSwitcher).current = "feature-table"
        self.query_one("#feature-table", DataTable).focus()

    @on(DataTable.RowSelected)
    def on_data_table_cell_selected(self, event: DataTable.RowSelected) -> None:
        # self.query_one(RichLog).write(event.row_key)
        if event.row_key == "seedsample" or event.row_key == "seedprod":
            self.query_one("#view", ContentSwitcher).current = event.row_key
        elif (
            event.row_key == "feature1"
            or event.row_key == "feature2"
            or event.row_key == "feature3"
            or event.row_key == "feature4"
            or event.row_key == "feature5"
            or event.row_key == "advancedfeature1"
            or event.row_key == "advancedfeature2a"
            or event.row_key == "advancedfeature2b"
        ):
            if not self.seeded:
                self.query_one("#view", ContentSwitcher).current = "unseeded-error"
            else:
                self.query_one("#view", ContentSwitcher).current = event.row_key

    def on_mount(self) -> None:
        table = self.query_one("#feature-table", DataTable)
        table.focus()
        table.add_column("Feature")
        table.add_column("Description")
        table.add_row(
            "Seed Sample Data",
            "Seeds the database instance with sample data.",
            key="seedsample",
        )
        table.add_row(
            "Seed Production Data",
            "Seeds the database instance with production data.",
            key="seedprod",
        )
        table.add_row(
            "Driver Form",
            "Explore the forms of the drivers for a given timeframe of a season.",
            key="feature1",
        )
        table.add_row(
            "Average Lap Time",
            "Find the average time it takes a driver to complete a lap for a given race.",
            key="feature2",
        )
        table.add_row(
            "Pit Delta",
            "Find the difference between a driver's first lap and pit lap times for a given race.",
            key="feature3",
        )
        table.add_row(
            "Lap Info",
            "Get information about a particular lap in a given race.",
            key="feature4",
        )
        table.add_row(
            "Disqualify Driver",
            "Disqualify a specific driver from a specific race.",
            key="feature5",
        )
        table.add_row(
            "Driver Track History",
            "Given a track name and a driver name, find their statistics.",
            key="advancedfeature1",
        )
        table.add_row(
            "Create Account",
            "Create an account for a user.",
            key="advancedfeature2a",
        )
        table.add_row(
            "Grant Full Access",
            "Gives a user edit access.",
            key="advancedfeature2b",
        )

        table.cursor_type = "row"
        table.zebra_stripes = True


F1App().run()
