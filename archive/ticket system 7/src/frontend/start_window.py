from PyQt6.QtWidgets import (QHBoxLayout, QPushButton, QWidget)
from PyQt6.QtCore import pyqtSignal

class StartWindow(QWidget):
    #Signal: Jemand will zum Login
    request_login = pyqtSignal()
    request_registration = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign in/up")
        self.setFixedSize(300, 300)

        layout = QHBoxLayout()
        self.setLayout(layout)

        signin_button = QPushButton("Sign in")
        signup_button = QPushButton("Sign up")

        layout.addWidget(signin_button)
        layout.addWidget(signup_button)

        #Verbindung herstellen
        signin_button.clicked.connect(self.request_login.emit)
        signup_button.clicked.connect(self.request_registration.emit)