import sqlite3

def init_db():
    conn = sqlite3.connect('racers.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS racers (
            uid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team TEXT,
            age INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

def read_all():
    conn = sqlite3.connect('racers.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM racers')
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
    
    conn.close()


if __name__ == '__main__':
    init_db()
    read_all()