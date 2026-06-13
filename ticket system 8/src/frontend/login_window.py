from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel, QMessageBox, QToolButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

from backend.universal_data import CurrentUserdata
from backend.database import Database, DatabaseError

class LoginWindow(QWidget):
    request_main_window = pyqtSignal()
    signout_signal = pyqtSignal()

    def __init__(self):
        # super().__init__() ruft den Bauplan von QWidget auf, damit wir ein echtes Fenster sind
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300, 300)
        self.setMinimumSize(250, 250)

        # Layout erstellen
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Widgets erstellen
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.returnPressed.connect(self.check_login) #fängt Enter-Taste ab und führt check_login durch
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Submit")

        self.show_password = QToolButton()
        self.show_password.setText("👁")
        self.show_password.setCheckable(True)
        self.show_password.setToolTip("Show password")
        self.show_password.clicked.connect(self.show_or_hide_password)


        # Augen Button ins Passwort input Feld
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.show_password)


        signout_button = QPushButton("Return to start page")

        # Widgets zum Layout hinzufügen
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Password"))
        layout.addLayout(password_layout)
        layout.addWidget(login_button)
        layout.addWidget(signout_button)

        # Button verbinden
        login_button.clicked.connect(self.check_login)
        signout_button.clicked.connect(self.signout_signal.emit)

    def show_or_hide_password(self, checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password.setText("🚫")
            self.show_password.setToolTip("Hide password")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password.setText("👁")
            self.show_password.setToolTip("Show password")

    def check_login(self):
        username = self.name_input.text().strip()
        #.strip() um bspw. ungewollte Leerzeichen der Eingabe zu entfernen
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and pin!")
            return

        try:
            db = Database()
            success = db.check_login(username, password)

            if success is True:
                db.fetch_user_data(username, password)
                self.request_main_window.emit()
                print({"id": CurrentUserdata.id})
            elif success is False:
                QMessageBox.warning(self, "Error", "Wrong username or password!")
        except DatabaseError as e:
            QMessageBox.critical(self, "Database Error", str(e))
