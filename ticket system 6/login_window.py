from PyQt6.QtWidgets import (QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel, QMessageBox)
from PyQt6.QtCore import pyqtSignal

from universal_data import CurrentUserdata

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
        self.password_input.setPlaceholderText("Pin")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Submit")



        signout_button = QPushButton("Return to start page")

        # Widgets zum Layout hinzufügen
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Pin"))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(signout_button)

        # Button verbinden
        login_button.clicked.connect(self.check_login)
        signout_button.clicked.connect(self.signout_signal.emit)

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
                    if len(data) >= 3:
                        file_user = data[1].strip()
                        file_pw = data[2].strip()

                        if file_user == username and file_pw == password:
                            print("Login successful!")
                            CurrentUserdata.id = data[0]
                            CurrentUserdata.rank = data[3]
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