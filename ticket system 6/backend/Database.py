import sqlite3

class Database:
    def __init__(self):

        self.db_name = "backend/database.db"
        self.create_tables()

    def create_tables(self):
        userdata_table_query = """
            CREATE TABLE IF NOT EXISTS userdata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                rank TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """

        tickets_table_query = """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY,
                factor FLOAT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                category TEXT NOT NULL,
                shortdescription TEXT NOT NULL,
                longdescription TEXT
            )
        """

        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(userdata_table_query)
            cursor.execute(tickets_table_query)
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
            # Dieser Fehler tritt auf, wenn z.B. der Username schon existiert (UNIQUE)
            return False

    def check_login(self, username, password):
        query = "SELECT * FROM userdata WHERE username = ? AND password = ?"
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(query, (username, password))
            connection.commit()
