from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel, QMessageBox, QToolButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction

from backend.UniversalData import CurrentUserdata

class LoginWindow(QWidget):
    request_main_window = pyqtSignal()
    signout_signal = pyqtSignal()

    def __init__(self):
        # super().__init__() ruft den Bauplan von QWidget auf, damit wir ein echtes Fenster sind
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
        # Hier greifen wir auf UNSERE (self) Eingabefelder zu
        username = self.name_input.text()
        password = self.password_input.text()

        user_found = False

        try:
            # 'with' schließt die Datei automatisch, auch bei Fehlern
            with open("../userdata.txt", "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) >= 3:
                        file_user = data[1].strip()
                        file_pw = data[2].strip()

                        if file_user == username and file_pw == password:
                            print("Login successful!")
                            CurrentUserdata.id = data[0]
                            CurrentUserdata.rank = data[3]
                            CurrentUserdata.company = data[4]
                            user_found = True
                            self.request_main_window.emit()
                            break

            if not user_found:
                notification = QMessageBox()
                notification.setWindowTitle("Error")
                notification.setText("Hä gib doch ein richgtiges Passwort ein")
                notification.setIcon(QMessageBox.Icon.Warning)
                notification.exec()


        except FileNotFoundError:
            print("Fehler: userdata.txt wurde nicht gefunden!")