import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit)
from PyQt6.QtCore import pyqtSignal

class StartWindow(QWidget):
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

        btn_signin.clicked.connect(self.request_login.emit)

class LoginWindow(QWidget):
    login_success = pyqtSignal(str)

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
        user = self.username.text()
        if user == "admin":
            self.login_success.emit(user)
        else:
            print("Falsch (nutze 'admin')")

class RealAppWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Das eigentliche Programm")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel(f"Hallo {username}! Hier läuft die App."))
        layout.addWidget(QPushButton("Arbeit erledigen..."))

class WindowManager:
    def __init__(self):
        self.current_window = None

    def show_start_screen(self):
        self.current_window = StartWindow()
        self.current_window.request_login.connect(self.show_login_screen)
        self.current_window.show()

    def show_login_screen(self):
        self.current_window.close()
        self.current_window = LoginWindow()
        self.current_window.login_success.connect(self.show_main_app)
        self.current_window.show()

    def show_main_app(self, username):
        self.current_window.close()
        self.current_window = RealAppWindow(username)
        self.current_window.show()

app = QApplication(sys.argv)
manager = WindowManager()
manager.show_start_screen()

sys.exit(app.exec())