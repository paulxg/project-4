import sys
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QPushButton,
                             QWidget, QVBoxLayout, QLineEdit, QLabel, QMessageBox)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hauptmenü")
        self.setFixedSize(300, 300)

        layout = QHBoxLayout()
        self.setLayout(layout)

        signin_button = QPushButton("Sign in")
        signup_button = QPushButton("Sign up")

        layout.addWidget(signin_button)
        layout.addWidget(signup_button)

        # Verbindung herstellen
        signin_button.clicked.connect(self.open_login_window)

        # Platzhalter für das zweite Fenster
        self.login_window = LoginWindow()

    def open_login_window(self):
        # Wir erstellen eine Instanz der LoginWindow-Klasse
        self.login_window.show()

class LoginWindow(QWidget):
    def __init__(self):
        # super().__init__() ruft den Bauplan von QWidget auf, damit wir ein echtes Fenster sind
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 300)

        # Layout erstellen
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Widgets erstellen
        # Wir nutzen 'self.', damit wir später in anderen Methoden (wie check_login)
        # darauf zugreifen können.
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Pin")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Submit")

        # Widgets zum Layout hinzufügen
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Pin"))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        # Button verbinden
        login_button.clicked.connect(self.check_login)

    def check_login(self):
        # Hier greifen wir auf UNSERE (self) Eingabefelder zu
        username = self.name_input.text()
        password = self.password_input.text()

        user_found = False

        try:
            # 'with' schließt die Datei automatisch, auch bei Fehlern
            with open("userdata.txt", "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) >= 2:
                        file_user = data[0].strip()
                        file_pw = data[1].strip()

                        if file_user == username and file_pw == password:
                            print("Login erfolgreich!")
                            user_found = True
                            self.close()  # Fenster schließen bei Erfolg
                            break

            if not user_found:
                print("Benutzer oder Passwort falsch.")

        except FileNotFoundError:
            print("Fehler: userdata.txt wurde nicht gefunden!")





# --- Das Hauptprogramm ---
app = QApplication(sys.argv)

# Wir bauen das Haupt-Objekt aus dem Bauplan
main_window = MainWindow()
main_window.show()

app.exec()