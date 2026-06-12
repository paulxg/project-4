import sqlite3

class Database:
    def __init__(self):

        self.db_name = "backend/database.db"
        self.create_tables()

    def create_tables(self):
        query1 = """
            CREATE TABLE IF NOT EXISTS userdata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                rank TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """

        query2 = """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                factor FLOAT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                category TEXT NOT NULL,
                shortdescription TEXT NOT NULL,
                longdescription TEXT
            )
        """

        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(query1)
            cursor.execute(query2)
            # Migration: user_id Spalte hinzufügen falls DB schon existiert
            try:
                cursor.execute("ALTER TABLE tickets ADD COLUMN user_id INTEGER NOT NULL DEFAULT 0")
            except sqlite3.OperationalError:
                pass
            connection.commit()


    def create_user(self, username, password):

        rank = "user"
        status = "private"

        query = "INSERT INTO userdata (username, password, rank, status) VALUES ( ?, ?, ?, ?)"

        try:
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                cursor.execute(query, (username, password, rank, status))
                connection.commit()
                return True #erfolgreich angelegt

        except sqlite3.IntegrityError:
            # Fehler tritt auf, wenn z.B. der Username schon existiert (UNIQUE)
            return False

    def create_ticket(self, user_id, factor, category, shortdescription, longdescription):
        query = """
            INSERT INTO tickets (user_id, factor, category, shortdescription, longdescription)
            VALUES (?, ?, ?, ?, ?)
        """
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(query, (user_id, factor, category, shortdescription, longdescription))
            connection.commit()

    def get_user_tickets(self, user_id):
        query = "SELECT category, shortdescription, longdescription FROM tickets WHERE user_id = ?"
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(query, (user_id,))
            return cursor.fetchall()

    def check_login(self, username, password):
        query = "SELECT id, username, rank FROM userdata WHERE username = ? AND password = ?"
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(query, (username, password))
            return cursor.fetchone()
