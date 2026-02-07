import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit)
from PyQt6.QtCore import pyqtSignal

# 1. Das Start-Fenster (Sign In / Sign Up Auswahl)

class StartWindow(QWidget):
    # Wir definieren ein eigenes Signal: "Jemand will zum Login"
    request_login = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Willkommen")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        btn_signin = QPushButton("Zum Login")
        btn_signup = QPushButton("Registrieren (Dummy)")

        layout.addWidget(QLabel("Wähle eine Aktion:"))
        layout.addWidget(btn_signin)
        layout.addWidget(btn_signup)

        # Wenn der Button gedrückt wird, feuern wir unser Signal ab
        # Wir rufen NICHT das andere Fenster auf, wir schreien nur "LOGIN!" in den Raum.
        btn_signin.clicked.connect(self.request_login.emit)


# 2. Das Login-Fenster

class LoginWindow(QWidget):
    # Signal: "Login war erfolgreich"
    login_success = pyqtSignal(str)  # Wir senden den Username mit

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.username = QLineEdit()
        self.username.setPlaceholderText("User")
        btn_submit = QPushButton("Einloggen")

        layout.addWidget(QLabel("Bitte einloggen:"))
        layout.addWidget(self.username)
        layout.addWidget(btn_submit)

        btn_submit.clicked.connect(self.check_login)

    def check_login(self):
        # ... Hier käme deine echte Überprüfung mit der Datei ...
        user = self.username.text()
        if user == "admin":  # Simulierter Erfolg
            # Wir senden das Signal an den Controller
            self.login_success.emit(user)
        else:
            print("Falsch (nutze 'admin')")


# 3. Das "Echte" Hauptprogramm

class RealAppWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Das eigentliche Programm")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel(f"Hallo {username}! Hier läuft die App."))
        layout.addWidget(QPushButton("Arbeit erledigen..."))


# 4. Der Controller (Der Manager)

class WindowManager:
    def __init__(self):
        self.current_window = None

    def show_start_screen(self):
        # Wir erstellen das Startfenster
        self.current_window = StartWindow()

        # Wir verbinden das Signal des Fensters mit unserer Methode
        self.current_window.request_login.connect(self.show_login_screen)

        self.current_window.show()

    def show_login_screen(self):
        # Altes Fenster schließen
        self.current_window.close()

        # Neues Fenster erstellen
        self.current_window = LoginWindow()

        # Auf Erfolg hören
        self.current_window.login_success.connect(self.show_main_app)

        self.current_window.show()

    def show_main_app(self, username):
        self.current_window.close()

        # Das eigentliche Programm starten
        self.current_window = RealAppWindow(username)
        self.current_window.show()

# Main Execution
app = QApplication(sys.argv)

# Der Manager übernimmt die Kontrolle
manager = WindowManager()
manager.show_start_screen()

sys.exit(app.exec())