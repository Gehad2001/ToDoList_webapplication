import sqlite3

def get_db():
    db = sqlite3.connect('todo.db',detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db