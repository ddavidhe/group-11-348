# Milestone 2

## 1. Download Dependencies and MySQL

Ensure you are in the `milestone-2` directory before running these commands

```bash
source ../.venv/bin/activate
pip install -r ../requirements.txt
```

Download MySQL Community Server here: https://dev.mysql.com/downloads/mysql/

## 2. Install MySQL Community Server
You will be prompted to create a password for the database, this will be used in `app.py` to connect to your database. For example,

```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)
```

## 3. Turn on MySQL Community Server
The community server will be on by default.
- MacOS: Use spotlight search 'mysql' to find an interface in System Settings to turn it off and on.

You will also need to initialize the database, which is a button in the 'mysql' tab of System Settings.

## 4. Run the TUI Application
Perform a "Hello World" by running the app. Ensure you are in the `milestone-2` directory.

```bash
python3 TUI.py
```

The app connects the user to their local MySQL database and runs features against it.

## 5. Sample Database & Application
To create and load the sample database, please use the TUI application. Upon launching, navigate to the row named `Seed Sample Data`, press enter, and click the button in the center of the screen once. This will seed the database. Now, hit `[ESC]` to return to the main screen. 

To use the features, in the TUI application menu please use the arrow keys to select the desired feature and follow the prompts. The features implememented in the TUI are currently as follows:
- Getting the form of all drivers within a window of a given season. The user would give a season, starting round, and ending round, and be able to see how each driver performed during the window.
- Getting the average lap time of a driver for a given race.
- Getting the time difference between a selected driver's first lap and pit laps, for a selected race.
- Getting information on every driver's performance in a given lap of a given race.
- Allowing users to disqualify drivers from a given race. This involves dropping them to P20 and bumping everyone lower than them up.

## 6. Production Database
The production database was generated with the Jupyter Notebooks found in `milestone-2/production_data/data_collection`. To generate them, simply click run.

Sample data has been sourced from FastF1 (https://docs.fastf1.dev/). For all datasets except the lap and weather data, data was collected between 1989 and 2024 (inclusive). For lap and weather data though, Formula 1 as a whole only started collecting detailed telemetry from 2018 onwards. Thus, for lap and weather data only 2018 to 2024 (inclusive) was collected. To actually generate it, data was pulled from the FastF1 Python library nearly identical to the way it was done for the sample database and then formatted and stored as CSVs. Functions for collecting the data are in Jupyter Notebook files inside the repo. Note that FastF1 has a hard ceiling for API calls allowed, so functions to load things like mapping (between their primary keys and our primary keys) or the current state of the dataset were implemented to allow us to collect data in multiple sessions. We see this where we split results into years instead of doing it all in one go. Otherwise, we handle filtering laps the way we do in the sample dataset. 

To actually populate the production database, Python functions were created to take each row in and CSV, format it to a string that represents a tuple, and append it to an INSERT INTO table VALUES …; statement. This was then executed to load the data into the database. This is built into the TUI application. To load the production data then, repeat the steps of loading the sample data but select the `Seed Production Data` row in the menu.

To use the features, in the TUI application menu please use the arrow keys to select the desired feature and follow the prompts. The implementation of the features from SQL query to UI are found in the `milestone-2/TUI.py` file. The features implememented in the TUI are currently as follows:
- Getting the form of all drivers within a window of a given season. The user would give a season, starting round, and ending round, and be able to see how each driver performed during the window. The SQL implementation is found in `milestone-2/queries/feature-1/driver_form.sql`.
- Getting the average lap time of a driver for a given race. The SQL implementation is found in `milestone-2/queries/feature-2/average_lap.sql`.
- Getting the time difference between a selected driver's first lap and pit laps, for a selected race. The SQL implementation is found in `milestone-2/queries/feature-3/pit_delta.sql`.
- Getting information on every driver's performance in a given lap of a given race. The SQL implementation is found in `milestone-2/queries/feature-4/lap_info.sql`.
- Allowing users to disqualify drivers from a given race. This involves dropping them to P20 and bumping everyone lower than them up. The SQL implementation is found in `milestone-2/queries/feature-5/disqualify.sql`.
- Disqualifying a driver from a specific race. The SQL implementation is found in `milestone-2/queries/feature-5/disqualify.sql`.
