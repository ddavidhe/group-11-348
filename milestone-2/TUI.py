from turtledemo.penrose import start

import mysql.connector
import numpy as np
import pandas as pd
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, HorizontalScroll, VerticalScroll
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

        #feature1 {
            padding: 1;
            align: center middle;
            content-align: center middle;
            height: auto;
        }

        #feature1-interface Static {
            text-align: center;
        }

        #feature1-interface {
            padding: 1;
            align: center middle;
            content-align: center middle;
            height: auto;
        }

        #feature1-interface Input {
            width: 50%;
            text-align: center;
        }

        #feature1-interface Button {
            width: auto;
        }

        #feature1-table {
            width: auto;
            margin-top: 1;
            margin-bottom: 1;
        }

        #feature5 {
            padding: 1;
            align: center middle;
            content-align: center middle;
            height: auto;
        }

        #feature5-interface Static {
            text-align: center;
        }

        #feature5-interface {
            padding: 1;
            align: center middle;
            content-align: center middle;
            height: auto;
        }

        #feature5-interface Input {
            width: 50%;
            text-align: center;
        }

        #feature5-interface Button {
            width: auto;
        }

        #unseeded-error {
            padding: 1;
            align: center middle;
            height: auto;
        }

        Horizontal {
            align: center middle;
            height: auto;
        }
    """

    def __init__(self):
        super().__init__()
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="password"
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS racing_db;")
        self.cursor.execute("USE racing_db;")
        self.seeded = False

    def _db_seed_sample(self):
        def seed(n, c):
            with open(n, "r") as data_file:
                data_statements = data_file.read().split(";")
                for ds in data_statements:
                    if ds.strip():
                        c.execute(ds)

        # self.query_one(RichLog).write("Seeding sample database.")

        self.cursor.execute("DROP DATABASE racing_db;")
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

    def _db_seed_prod(self):
        # self.query_one(RichLog).write("Seeding production database.")

        self.cursor.execute("DROP DATABASE racing_db;")
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

    def _count_rounds(self, season):
        self.cursor.execute(f"SELECT COUNT(*) FROM races WHERE season = {season}")
        return self.cursor.fetchone()[0]

    def _db_query_feature1(self, s, e, season):
        with open("queries/feature-1/driver_form.sql", "r") as driver_form:
            driver_form_template = driver_form.read()
            driver_form_template = driver_form_template.format(s, e, season)
            self.cursor.execute(driver_form_template)
            table = self.query_one("#feature1-table", DataTable)
            table.add_columns("First Name", "Last Name", "CODE", "Points")
            for row in self.cursor.fetchall():
                table.add_row(row[0], row[1], row[2], row[3])
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
            for row in self.cursor.fetchall():
                table.add_row(row[0])
            table.cursor_type = "row"
            table.zebra_stripes = True

    def _db_query_feature3(self, rID, dID):
        with open("queries/feature-3/pit_delta.sql", "r") as pit_delta:
            pit_delta_template = pit_delta.read()
            pit_delta_template = pit_delta_template.format(rID, dID)
            self.cursor.execute(pit_delta_template)
            table = self.query_one("#feature3-table", DataTable)
            table.add_columns("Pit Stop Delta Times")
            for row in self.cursor.fetchall():
                table.add_row(row[0])
            table.cursor_type = "row"
            table.zebra_stripes = True

    def _db_query_feature5(self, rID, dID, cID):
        with open("queries/feature-5/disqualify.sql", "r") as disqualify:
            disqualify_template = disqualify.read()
            disqualify_template = disqualify_template.format(rID=rID, dID=dID, cID=cID)
            # Execute the transaction
            for statement in disqualify_template.split(";"):
                if statement.strip():
                    self.cursor.execute(statement)
            self.conn.commit()

    def _reset_feature5(self):
        self.query_one(
            "#feature5-switcher", ContentSwitcher
        ).current = "feature5-interface"
        self.query_one("#feature5-raceid", Input).value = ""
        self.query_one("#feature5-driverid", Input).value = ""
        self.query_one("#feature5-constructorid", Input).value = ""

    def compose(self) -> ComposeResult:
        yield Static(self.LOGO, id="logo")

        with ContentSwitcher(id="view", initial="feature-table"):
            yield DataTable(id="feature-table")

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

            with VerticalScroll(id="feature1"):
                with ContentSwitcher(
                    id="feature1-switcher", initial="feature1-interface"
                ):
                    with Container(id="feature1-interface"):
                        yield Static(
                            "Please input a season, starting round, and an ending round."
                        )
                        with Horizontal():
                            yield Input(
                                placeholder="Season...",
                                id="feature1-season",
                                type="integer",
                            )
                        with Horizontal():
                            yield Input(
                                placeholder="Start...",
                                id="feature1-start",
                                type="integer",
                            )
                        with Horizontal():
                            yield Input(
                                placeholder="End...", id="feature1-end", type="integer"
                            )
                        with Horizontal():
                            yield Button("Go", id="feature1-go")
                    with Horizontal(id="feature1-table-container"):
                        yield DataTable(id="feature1-table")

            with VerticalScroll(id="feature2"):
                with ContentSwitcher(
                    id="feature2-switcher", initial="feature2-interface"
                ):
                    with Container(id="feature2-interface"):
                        yield Static("Please input a raceID and a driverID")
                        yield Input(placeholder="Race ID...", id="feature2-raceid")
                        yield Input(placeholder="Driver ID...", id="feature2-driverid")
                        yield Button("Go", id="feature2-go")
                    yield DataTable(id="feature2-table")

            with VerticalScroll(id="feature3"):
                with ContentSwitcher(
                    id="feature3-switcher", initial="feature3-interface"
                ):
                    with Container(id="feature3-interface"):
                        yield Static("Please input a raceID and a driverID")
                        yield Input(placeholder="Race ID...", id="feature3-raceid")
                        yield Input(placeholder="Driver ID...", id="feature3-driverid")
                        yield Button("Go", id="feature3-go")
                    yield DataTable(id="feature3-table")

            with VerticalScroll(id="feature5"):
                with ContentSwitcher(
                    id="feature5-switcher", initial="feature5-interface"
                ):
                    with Container(id="feature5-interface"):
                        yield Static(
                            "Please input a race ID, driver ID, and constructor ID to disqualify a driver."
                        )
                        with Horizontal():
                            yield Input(
                                placeholder="Race ID...",
                                id="feature5-raceid",
                                type="integer",
                            )
                        with Horizontal():
                            yield Input(
                                placeholder="Driver ID...",
                                id="feature5-driverid",
                                type="integer",
                            )
                        with Horizontal():
                            yield Input(
                                placeholder="Constructor ID...",
                                id="feature5-constructorid",
                                type="integer",
                            )
                        with Horizontal():
                            yield Button("Disqualify", id="feature5-go")
                    with Container(id="feature5-success"):
                        yield Static("Driver successfully disqualified!")

        # yield RichLog()

        yield Static(
            "Press \[Enter] to select a feature, press \[Escape] to go back, and press \[q] to quit.",
            id="helper-text",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "seed-sample-btn":
            self._db_seed_sample()
        if button_id == "seed-prod-btn":
            self._db_seed_prod()
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
            self._db_query_feature2(rID, dID)
            self.query_one(
                "#feature2-switcher", ContentSwitcher
            ).current = "feature2-table"
            self.query_one("#feature2-table", DataTable).focus()
        if button_id == "feature3-go":
            rID = self.query_one("#feature3-raceid", Input).value
            dID = self.query_one("#feature3-driverid", Input).value
            self._db_query_feature3(rID, dID)
            self.query_one(
                "#feature3-switcher", ContentSwitcher
            ).current = "feature3-table"
            self.query_one("#feature3-table", DataTable).focus()
        if button_id == "feature5-go":
            rID = self.query_one("#feature5-raceid", Input).value
            dID = self.query_one("#feature5-driverid", Input).value
            cID = self.query_one("#feature5-constructorid", Input).value
            if rID == "" or dID == "" or cID == "":
                self.notify("Please fill out all fields.")
                return
            try:
                self._db_query_feature5(rID, dID, cID)
                self.query_one(
                    "#feature5-switcher", ContentSwitcher
                ).current = "feature5-success"
                self.notify("Driver successfully disqualified!")
            except Exception as e:
                self.notify(f"Error: {str(e)}")

    def action_back(self) -> None:
        self._reset_feature1()
        self._reset_feature5()
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
            or event.row_key == "feature5"
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
        table.add_row("Feature 4", "Feature 4.", key="feature4")
        table.add_row(
            "Disqualify Driver",
            "Disqualify a specific driver from a specific race.",
            key="feature5",
        )

        table.cursor_type = "row"
        table.zebra_stripes = True


F1App().run()
