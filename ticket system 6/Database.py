import sqlite3

class Database:
    def __init__(self, db_name = "database.db"):

        self.db_name = db_name
        self.create_tables()

    def create_tables(self):
        query = """
            CREATE TABLE IF NOT EXISTS userdata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                rank TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """

        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()


    def create_user(self, username, password, rank="user", status="private"):
        query = "INSERT INTO userdata (username, password, rank, status) VALUES ( ?, ?, ?, ?)"

        try:
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                cursor.execute(query, (username, password, rank, status))
                connection.commit()
                return True #erfolgreich angelegt

        except sqlite3.IntegrityError:
            # Dieser Fehler tritt auf, wenn z.B. der Username schon existiert (UNIQUE)
            return False

    def check_login(self, username, password):
        query = "SELECT * FROM userdata WHERE username = ? AND password = ?"
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(query, (username, password))
            connection.commit()
