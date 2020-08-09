import sqlite3

conn = sqlite3.connect('./test.db')
c = conn.cursor()
c.execute('''DROP TABLE ephemeris_model''')

c.execute('''CREATE TABLE ephemeris_model (
             id INTEGER NOT NULL PRIMARY KEY,
             name TEXT NOT NULL,
             date TEXT NOT NULL)''')

c.execute()
