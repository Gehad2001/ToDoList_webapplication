import sqlite3, os
from database import get_db

def create_tables(db):
    conn = db
    with open("tables.sql",'r') as tables:
        conn.execute(tables.read())
    conn.commit()
    conn.close()
    print("Database created!")
    return True
create_tables(get_db())
