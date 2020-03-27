import sqlite3
from flask import g

DATABASE = 'invertedIndexes.db';
con = sqlite3.connect("invertedIndexes.db")
print("Database opened successfully")
con.execute("create table indexes (id INTEGER PRIMARY KEY AUTOINCREMENT, token TEXT NOT NULL, idf REAL, totalDocs INTEGER NOT NULL, tokenOccurences TEXT NOT NULL)")
print("Table created successfully")
con.close()
