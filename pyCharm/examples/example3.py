import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        con = sqlite3.connect('mydatabase.db')
        return con
    except Error:
        print(Error)

    return None


def sql_table(con):
    cursor_obj = con.cursor()
    cursor_obj.execute(
        """
    CREATE TABLE employees (
    id integer PRIMARY KEY,
    name text,
    salary real,
    department text,
    position text,
    hireDate text)
      """
    )

    cursor_obj.execute('''
    CREATE TABLE sections (
    _id INTEGER PRIMARY KEY,
    name TEXT)''')

    cursor_obj.execute('''
    CREATE TABLE pages (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT NOT NULL,
    theme INTEGER NOT NULL,
    num INTEGER DEFAULT 100,
    FOREIGN KEY (theme)
    REFERENCES sections(_id))
    ''')

    con.commit()

    cursor_obj.execute("PRAGMA foreign_keys = ON")

    themes = [
        (1, 'Information'),
        (2, 'Digital Systems'),
        (3, 'Boolean Algebra')]

    cursor_obj.executemany('''
    INSERT INTO sections
    VALUES (?, ?)''', themes)

    cursor_obj.execute("SELECT * FROM sections")
    cursor_obj.fetchone()
    cursor_obj.fetchone()
    cursor_obj.__next__()
    cursor_obj.fetchall()

    cursor_obj.execute("SELECT * FROM sections")
    cursor_obj.fetchmany(2)
    cursor_obj.fetchmany(2)


if __name__ == "__main__":
    con = sql_connection()
    sql_table(con)

    con.commit()
    con.close()
