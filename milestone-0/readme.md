# Milestone 0

## 1. Download Dependencies and MySQL

Ensure you are in the milestone-0 directory before running these commands

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

## 4. Run the Application
Perform a "Hello World" by running the app.

```bash
python3 app.py
```

Currently the app connects the user to their local MySQL database, creates and populates a test table, and reads all entries from it.
