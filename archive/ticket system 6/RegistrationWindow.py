from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit,QMessageBox
from PyQt6.QtCore import pyqtSignal


class RegistrationWindow(QWidget):
    request_main_window = pyqtSignal()
    return_signal = pyqtSignal()

    def __init__(self):
        # super().__init__() ruft den Bauplan von QWidget auf
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
        layout.addWidget(QLabel("Pin"))
        layout.addWidget(self.password_input)
        layout.addWidget(register_button)
        layout.addWidget(return_button)

        # Button verbinden
        register_button.clicked.connect(self.save_user_data)
        return_button.clicked.connect(self.return_signal.emit)

    def save_user_data(self):
        username = self.name_input.text().strip()
        pin = self.password_input.text().strip()

        if not username or not pin:
            QMessageBox.warning(self, "Warning", "Please enter your username and pin!")
            return
        if not pin.isdigit():
            QMessageBox.warning(self, "Warning", "The pin can only be digits!")
            return

        next_id = 1

        try:
        # damit programm nicht abstürzt

            with open("userdata.txt", "r", encoding="utf-8") as file:
                     lines = file.readlines()

            valid_lines = [line.strip() for line in lines if line.strip()]
                     # Prüfen, ob es mehr als nur die Kopfzeile gibt

            if len(valid_lines) > 1:
                # 1. Die allerletzte Zeile aus der Liste holen
                letzte_zeile = valid_lines[-1]

                # 2. Den Text am ersten Komma trennen und das erste Stück (die ID) nehmen
                letzte_id_text = letzte_zeile.split(',')[0]

                # 3. Den Text in eine Zahl umwandeln und + 1 rechnen
                next_id = int(letzte_id_text) + 1
        except FileNotFoundError:
            next_id = 1

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"issue with reading file: {e}")
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error reading file: {e}")
            return


        try:
            with open("userdata.txt", "a", encoding="utf-8") as file:
                file.write(f"{next_id},{username},{pin},user,private\n")

            QMessageBox.information(self, "Success", "User data saved!")

            self.name_input.clear()
            self.password_input.clear()

            self.request_main_window.emit()


        except Exception as e:
            QMessageBox.critical(self, "Error", f"issue with saving{e}")






