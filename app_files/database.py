import sqlite3
import json

class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect("local.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        # self.cursor.execute("""DROP TABLE Packs""")
        # self.cursor.execute("""DROP TABLE Quotes""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Packs (
        Name TEXT PRIMARY KEY,
        Description TEXT
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Quotes (
        QuoteID INTEGER PRIMARY KEY,
        PackName TEXT,
        QuoteText TEXT,
        FOREIGN KEY (PackName) REFERENCES Packs(Name)
        )""")

    def insert(self, json_file):
        with open(json_file, "r") as file:
            data = json.load(file)
            pack_name = data["Name"]
            pack_description = data["Description"]
            quotes = data["Quotes"]

        self.cursor.execute("""INSERT OR IGNORE INTO Packs (Name, Description) 
        VALUES (?,?)""", (pack_name, pack_description))

        for quote in quotes:
            self.cursor.execute("""INSERT INTO Quotes (PackName, QuoteText)
            VALUES (?,?)""", (pack_name, quote))

        self.connection.commit()

