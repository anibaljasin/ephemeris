import sqlite3

conn = sqlite3.connect('./test.db')
cursor = conn.cursor()

cursor.execute('''DROP TABLE IF EXISTS ephemeris_repository''')
cursor.execute('''CREATE TABLE IF NOT EXISTS ephemeris_repository (
             id INTEGER NOT NULL PRIMARY KEY,
             name TEXT NOT NULL,
             date TEXT NOT NULL);''')

cursor.execute('''INSERT INTO ephemeris_repository VALUES
            (1, "dia del metegol", "2020-01-01"),
            (2, "dia del amigo", "2020-07-20"),
            (3, "dia del hermano", "2020-08-11"),
            (4, "dia del padre", "2020-09-15"),
            (5, "dia del futbol", "2020-06-24");''')

conn.commit()
conn.close()
