from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel, QMessageBox, QToolButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction

from backend.universal_data import CurrentUserdata
from backend.database import Database

class LoginWindow(QWidget):
    request_main_window = pyqtSignal()
    signout_signal = pyqtSignal()

    def __init__(self):
        # super().__init__() ruft den Bauplan von QWidget auf
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 300)

        #Layout erstellen
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Widgets erstellen
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.returnPressed.connect(self.check_login) #fängt Enter-Taste ab und führt check_login durch
        self.password_input.setPlaceholderText("Pin")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Augen icon (ist ein PyQt Standard Icon)

        icon = self.style().standardIcon(
            self.style().StandardPixmap.SP_FileDialogDetailedView
        )

        login_button = QPushButton("Submit")

        # Augen-Button ist eine QAction (welches icon wird angezeigt, text zum icon, self -> im fenster)

        self.show_password = QToolButton()
        self.show_password.setIcon(icon)
        self.show_password.setCheckable(True)
        self.show_password.setToolTip("show password")
        self.show_password.clicked.connect(self.show_or_hide_password)


        # Augen Button ins Passwort input Feld

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.show_password)


        signout_button = QPushButton("Return to start page")

        # Widgets zum Layout hinzufügen

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Pin"))
        layout.addLayout(password_layout)
        layout.addWidget(login_button)
        layout.addWidget(signout_button)

        # Button verbinden
        login_button.clicked.connect(self.check_login)
        signout_button.clicked.connect(self.signout_signal.emit)

    def show_or_hide_password(self, checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password.setToolTip("Passwort verstecken")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password.setToolTip("Passwort anzeigen")

    def check_login(self):
        username = self.name_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and pin!")
            return

        db = Database()
        user = db.check_login(username, password)

        if user:
            CurrentUserdata.id = user[0]
            CurrentUserdata.rank = user[2]
            self.request_main_window.emit()
        else:
            QMessageBox.warning(self, "Error", "Falscher Username oder Pin!")