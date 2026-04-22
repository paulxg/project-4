import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        # Mache sie direkt zu Klassen-Variablen (mit self.)
        self.connection = None
        self.cursor = None

        try:
            # self.connection statt nur connection nutzen
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="projekt_4_db"
            )

            if self.connection.is_connected():
                print("Erfolgreich mit der MySQL-Datenbank verbunden!")
                # Jetzt klappt auch der Cursor!
                self.cursor = self.connection.cursor()

        except Error as e:
            print(f"Fehler bei der Verbindung zu MySQL: {e}")

    def check_login(self, username, password):
        # Falls es keine Datenbankverbindung gibt, brich ab, bevor es kracht
        if not self.cursor:
            print("Kein Datenbankzugriff möglich.")
            return None

        # Hier schickst du die Abfrage an MySQL
        query = "SELECT id, username, rank FROM userdata WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))

        # fetchone() holt das erste gefundene Ergebnis
        return self.cursor.fetchone()

    def create_user(self, username, password):
        if not self.cursor:
            print("Kein Datenbankzugriff möglich.")
            return False

        try:
            # Wir fügen den Nutzer hinzu. Standardmäßig bekommt er den Rang "user" und den Status "private" (oder was auch immer in deiner Tabelle steht)
            query = "INSERT INTO userdata (username, password, rank, status) VALUES (%s, %s, %s, %s)"
            # Hier übergeben wir die Werte, die an die Stelle der %s rücken
            self.cursor.execute(query, (username, password, "user", "private"))

            # WICHTIG: Änderungen in der Datenbank endgültig speichern
            self.connection.commit()
            return True

        except mysql.connector.IntegrityError:
            # Dieser Fehler wird von MySQL geworfen, wenn ein Username schon existiert
            # (Vorausgesetzt, du hast den Username in Workbench auf "UNIQUE" gestellt)
            return False