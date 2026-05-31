from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit,QMessageBox
from PyQt6.QtCore import pyqtSignal

from backend.database import Database, DatabaseError


class RegistrationWindow(QWidget):
    request_main_window = pyqtSignal()
    return_signal = pyqtSignal()

    def __init__(self):
        # super().__init__() ruft den Bauplan von QWidget auf, damit wir ein echtes Fenster sind
        super().__init__()
        self.setWindowTitle("Create your account")
        self.resize(300, 300)
        self.setMinimumSize(250, 250)

        # Layout erstellen
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Widgets erstellen
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.returnPressed.connect(self.transfer_user_data)  # fängt Enter-Taste ab und führt check_login durch

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
            QMessageBox.warning(self, "Warning", "Please enter your username and password!")
            return

        try:
            db = Database()
            check_user_exists = db.check_login(username, password)
            
            if check_user_exists is False:
                success = db.create_user(username, password)
                if success is True:
                    QMessageBox.information(self, "Success", "User created successfully!")
                    fetch_success = db.fetch_user_data(username, password)
                    if fetch_success is True:
                        self.request_main_window.emit()
                    else:
                        QMessageBox.warning(self, "Error", "User data could not be loaded after registration.")
                        self.return_signal.emit()
                else:
                    QMessageBox.warning(self, "Error", "User konnte nicht erstellt werden!")
                    self.return_signal.emit()
            elif check_user_exists is True:
                QMessageBox.warning(self, "Warning", "This username already exists! Please choose another username!")
                
        except DatabaseError as e:
            QMessageBox.critical(self, "Database Error", str(e))
