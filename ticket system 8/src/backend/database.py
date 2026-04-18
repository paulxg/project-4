import mysql.connector

class Database:
    def __init__(self):
        self.database_connection()

    def database_connection(self):
        try:
            # Verbindung aufbauen
            connection = mysql.connector.connect(
                host="localhost",  # Da XAMPP lokal läuft
                user="root",  # Standard-Benutzer bei XAMPP
                password="",  # Standardmäßig leer bei XAMPP
                database="meine_datenbank"  # Hier DEINEN Datenbanknamen eintragen
            )

            if connection.is_connected():
                print("Erfolgreich mit der MySQL-Datenbank verbunden!")
                return connection

        except mysql.connector.Error as error:
            print(f"Fehler bei der Verbindung zur Datenbank: {error}")
            return None

