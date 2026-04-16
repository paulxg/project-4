from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit,QMessageBox
from PyQt6.QtCore import pyqtSignal

from backend.Database import Database
from backend.UniversalData import CurrentUserdata


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


        register_button = QPushButton("Register")
        return_button = QPushButton("Return to start page")


        # Widgets zum Layout hinzufügen
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password_input)
        layout.addWidget(register_button)
        layout.addWidget(return_button)

        # Button verbinden
        register_button.clicked.connect(self.transfer_user_data)
        return_button.clicked.connect(self.return_signal.emit)

    def transfer_user_data(self):
        username = self.name_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Warning", "Please enter your username and pin!")
            return

        try:
            db = Database()
            success = db.create_user(username, password)

            if success:
                QMessageBox.information(self, "Success", "User created successfully!")
                self.name_input.clear()
                self.password_input.clear()
                self.request_main_window.emit()

            else:

                QMessageBox.warning(self, "Error ", f"Username or pin is invalid!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Issue with saving {e}")
