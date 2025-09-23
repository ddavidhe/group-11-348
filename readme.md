# project

1. Download SQLite
SQLite is native to Linux/MacOS. If using Windows, you can download it here: https://www.sqlite.org/download.html

2. Create Racer Database

```bash
sqlite3 racers.db < schema.sql
sqlite3 racers.db < data.sql
```

3. Run the Application
Perform a "Hello World" by running the app. It connects the user to the database and reads all entries that are in the table.

```bash
python3 app.py
```