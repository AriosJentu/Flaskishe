import sqlite3 as db

studb = db.connect("studb.db")
cursr = studb.cursor()