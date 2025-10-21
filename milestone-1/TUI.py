from turtledemo.penrose import start

import mysql.connector
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Container, VerticalScroll
from textual.widgets import Button, ContentSwitcher, Static, DataTable, RichLog, Input

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
        
        #seed {
            padding: 1;
            align: center middle;
            height: auto;
        }
        
        #feature1 {
            padding: 1;
            align: center middle;
            height: auto;
        }
        
        #feature1-interface {
            padding: 1;
            align: center middle;
            height: auto;
        }
    """
    def __init__(self):
        super().__init__()
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password"
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS racing_db;")
        self.cursor.execute("USE racing_db;")

    def _db_seed(self):
        def seed(n, c):
            with open(n, "r") as data_file:
                data_statements = data_file.read().split(';')
                for ds in data_statements:
                    if ds.strip():
                        c.execute(ds)

        self.query_one(RichLog).write("Seeding database")

        self.cursor.execute("DROP DATABASE racing_db;")
        self.cursor.execute("CREATE DATABASE racing_db;")
        self.cursor.execute("USE racing_db;")

        with open("schema.sql", "r") as schema_file:
            schema_statements = schema_file.read().split(';')
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

    def compose(self) -> ComposeResult:
        yield Static(self.LOGO, id="logo")

        with ContentSwitcher(id='view', initial="feature-table"):
            yield DataTable(id="feature-table")

            with VerticalScroll(id='seed'):
                yield Button("Seed the database", id="seed-btn")

            with VerticalScroll(id='feature1'):
                with ContentSwitcher(id='feature1-switcher', initial="feature1-interface"):
                    with Container(id="feature1-interface"):
                        yield Static("Please input a season, starting round, and an ending round")
                        yield Input(placeholder="Season...", id="feature1-season")
                        yield Input(placeholder="Start...", id="feature1-start")
                        yield Input(placeholder="End...", id="feature1-end")
                        yield Button("Go", id="feature1-go")
                    yield DataTable(id="feature1-table")

            with VerticalScroll(id='feature2'):
                with ContentSwitcher(id='feature2-switcher', initial="feature2-interface"):
                    with Container(id="feature2-interface"):
                        yield Static("Please input a raceID and a driverID")
                        yield Input(placeholder="Race ID...", id="feature2-raceid")
                        yield Input(placeholder="Driver ID...", id="feature2-driverid")
                        yield Button("Go", id="feature2-go")
                    yield DataTable(id="feature2-table")
            
            with VerticalScroll(id='feature3'):
                with ContentSwitcher(id='feature3-switcher', initial="feature3-interface"):
                    with Container(id="feature3-interface"):
                        yield Static("Please input a raceID and a driverID")
                        yield Input(placeholder="Race ID...", id="feature3-raceid")
                        yield Input(placeholder="Driver ID...", id="feature3-driverid")
                        yield Button("Go", id="feature3-go")
                    yield DataTable(id="feature3-table")

        yield RichLog()

        yield Static("Press \[Enter] to select a feature, press \[Escape] to go back, and press \[q] to quit.", id="helper-text")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "seed-btn":
            self._db_seed()
        if button_id == "feature1-go":
            season = self.query_one("#feature1-season", Input).value
            s = self.query_one("#feature1-start", Input).value
            e = self.query_one("#feature1-end", Input).value
            self._db_query_feature1(s, e, season)
            self.query_one("#feature1-switcher", ContentSwitcher).current = "feature1-table"
            self.query_one("#feature1-table", DataTable).focus()
        if button_id == "feature2-go":
            rID = self.query_one("#feature2-raceid", Input).value
            dID = self.query_one("#feature2-driverid", Input).value
            self._db_query_feature2(rID, dID)
            self.query_one("#feature2-switcher", ContentSwitcher).current = "feature2-table"
            self.query_one("#feature2-table", DataTable).focus()
        if button_id == "feature3-go":
            rID = self.query_one("#feature3-raceid", Input).value
            dID = self.query_one("#feature3-driverid", Input).value
            self._db_query_feature3(rID, dID)
            self.query_one("#feature3-switcher", ContentSwitcher).current = "feature3-table"
            self.query_one("#feature3-table", DataTable).focus()

    def action_back(self) -> None:
        self.query_one("#view", ContentSwitcher).current = "feature-table"
        self.query_one("#feature-table", DataTable).focus()

    @on(DataTable.RowSelected)
    def on_data_table_cell_selected(self, event: DataTable.RowSelected) -> None:
        self.query_one(RichLog).write(event.row_key)
        if event.row_key == "seed" or event.row_key == "feature1" or event.row_key == "feature2" or event.row_key == "feature3":
            self.query_one("#view", ContentSwitcher).current = event.row_key

    def on_mount(self) -> None:
        table = self.query_one("#feature-table", DataTable)
        table.focus()
        table.add_column("Feature")
        table.add_column( "Description")
        table.add_row( "Seed", "Seeds the database instance", key='seed')
        table.add_row("Driver Form", "Explore the forms of the drivers for a given timeframe of a season.", key='feature1')
        table.add_row("Average Lap Time", "Find the average time it takes a driver to complete a lap for a given race.", key='feature2')
        table.add_row("Pit Delta", "Find the difference between a driver's first lap and pit lap times for a given race.", key='feature3')
        table.add_row("Feature 4", "Feature 4.", key='feature4')
        table.add_row("Feature 5", "Feature 5.", key='feature5')

        table.cursor_type = "row"
        table.zebra_stripes = True

F1App().run()