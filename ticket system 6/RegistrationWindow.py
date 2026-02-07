from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import pyqtSignal


class RegistrationWindow(QWidget):
    request_main_window = pyqtSignal()
    return_signal = pyqtSignal()

    def __init__(self):
        # super().__init__() ruft den Bauplan von QWidget auf, damit wir ein echtes Fenster sind
        super().__init__()
        self.setWindowTitle("Create your account")
        self.setFixedSize(300, 300)

        # Layout erstellen
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Widgets erstellen
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Pin")


        register_button = QPushButton("register")

        return_button = QPushButton("Return to start page")

        # Widgets zum Layout hinzufügen
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Pin"))
        layout.addWidget(self.password_input)
        layout.addWidget(register_button)
        layout.addWidget(return_button)

        # Button verbinden
        register_button.clicked.connect()
        return_button.clicked.connect(self.return_signal.emit)