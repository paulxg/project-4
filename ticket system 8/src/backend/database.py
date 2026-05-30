import mysql.connector
from mysql.connector import Error
from backend.universal_data import CurrentUserdata

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
        query = "SELECT 1 FROM userdata WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        user_checked = self.cursor.fetchone()
        if user_checked is not None:
            return True
        else:
            print("False")
            return False

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
            print("User erfolgreich erstellt!")
            return True

        except mysql.connector.IntegrityError as e:
            # Dieser Fehler wird von MySQL geworfen, wenn ein Username schon existiert
            # (Vorausgesetzt, du hast den Username in Workbench auf "UNIQUE" gestellt)
            print(f"IntegrityError (Vermutlich Username vergeben): {e}")
            return False

        except mysql.connector.Error as e:
            print(f"Allgemeiner SQL-Fehler beim Erstellen des Users: {e}")
            return False

        except Exception as e:
            # Fängt alle restlichen Python-Fehler ab
            print(f"Unerwarteter Fehler: {e}")
            return False

    #Schreibt id und rank in CurrentUserdata
    def fetch_user_data(self, username, password):
        if not self.cursor:
            print("Kein Datenbankzugriff möglich.")
            return []  #leere Liste zurückgeben, damit die Tabelle später nicht crasht

        print("Fetching user data...")
        query = "SELECT id,rank FROM userdata WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password,))
        mysql_data = self.cursor.fetchone()
        CurrentUserdata.id = mysql_data[0]
        CurrentUserdata.rank = mysql_data[1]
        print(f"current rank of acitve user: {CurrentUserdata.rank}")
        return True

    def get_user_tickets(self, user_id):
        if not self.cursor:
            print("Kein Datenbankzugriff möglich.")
            return []  #leere Liste zurückgeben, damit die Tabelle später nicht crasht

        query = "SELECT ticket_number, date_time, category, short_description, long_description FROM tickets WHERE user_id_ref = %s OR (SELECT rank FROM userdata WHERE id = %s) = 'admin' ORDER BY factor DESC"
        self.cursor.execute(query, (user_id, user_id))
        mysql_data = self.cursor.fetchall()
        return mysql_data

    def get_all_tickets(self):
        if not self.cursor:
            print("Kein Datenbankzugriff möglich.")
            return []  #leere Liste zurückgeben, damit die Tabelle später nicht crasht

        query = "SELECT ticket_number, date_time, category, short_description, long_description FROM tickets"
        self.cursor.execute(query,)
        mysql_data = self.cursor.fetchall()
        return mysql_data

    def create_ticket(self, user_id, factor, category, short_description, long_description):
        if not self.cursor:
            print("Kein Datenbankzugriff möglich.")
            return False

        try:
            query = "INSERT INTO tickets (user_id_ref, factor, category, short_description, long_description) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (user_id, factor, category, short_description, long_description))
            self.connection.commit()
            return True

        except mysql.connector.Error as e:
            print(f"Fehler beim Erstellen des Tickets: {e}")
            return False

    def delete_ticket(self, ticket_number):
        if not self.cursor:
            print("Kein Datenbankzugriff möglich.")
            return False

        print("delete ticket gestartet")
        query = "DELETE FROM tickets WHERE ticket_number = %s"
        self.cursor.execute(query, (ticket_number,))
        self.connection.commit()
        return True

    def ticket_edit_fetch(self, ticket_number):
        if not self.cursor:
            print("Kein Datenbankzugriff möglich.")
            return []

        query = "SELECT ticket_number, date_time, category, short_description, long_description FROM tickets WHERE ticket_number = %s"
        self.cursor.execute(query, (ticket_number,))
        mysql_data = self.cursor.fetchone()
        return mysql_data

    def comment_status(self, status, comment,ticket_number):
        if not self.cursor:
            print("Kein Datenbankzugriff möglich.")
            return False

        query = "UPDATE tickets SET status = %s, comment = %s WHERE ticket_number = %s"
        self.cursor.execute(query, (status, comment, ticket_number))
        self.connection.commit()
        print("Status / Comment Update successful")
        return True