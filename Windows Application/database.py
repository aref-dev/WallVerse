import sqlite3
import json

class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect("local.db", check_same_thread=False)
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

    def add_pack(self, pack_file):
        with open(pack_file, "r") as file:
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

    def remove_pack(self, pack_name):
        self.cursor.execute("DELETE FROM Quotes WHERE PackName = ?", (pack_name,))
        self.cursor.execute("DELETE FROM Packs WHERE Name = ?", (pack_name,))
        self.connection.commit()

    def get_info(self):
        self.cursor.execute("SELECT Name, Description FROM Packs")
        all_packs = self.cursor.fetchall()
        return all_packs


    def fetch_random_quote(self, pack_name):
        self.cursor.execute("SELECT QuoteText FROM Quotes "
                            "WHERE PackName = ? "
                            "ORDER BY RANDOM() LIMIT 1", (pack_name,))
        random_quote = self.cursor.fetchone()
        return random_quote[0]

