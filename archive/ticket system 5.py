import sys
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel, QComboBox, QFileDialog)
from PyQt6.QtCore import pyqtSignal

# 1. Der Controller (Der Manager)
class WindowManager:
    def __init__(self):
        self.current_window = None

    def show_start_screen(self):
        # Wir erstellen das Startfenster
        self.current_window = StartWindow()

        # Wir verbinden das Signal des Fensters mit unserer Methode
        self.current_window.request_login.connect(self.show_login_screen)

        self.current_window.show()

    def show_login_screen(self):
        # Altes Fenster schließen
        self.current_window.close()

        # Neues Fenster erstellen
        self.current_window = LoginWindow()

        self.current_window.request_main_window.connect(self.show_main_window)

        self.current_window.show()

    def show_main_window(self):
        self.current_window.close()

        self.current_window = MainWindow()

        self.current_window.create_ticket.connect(self.create_ticket)

        self.current_window.show()

    def create_ticket(self):
        self.current_window.close()

        self.current_window = CreateTicket()

        self.current_window.show()


#-------------------------------------------------------------------------------------------------

# Universal userdata
class CurrentUserdata:
    username = None
    password = None

#mit CurrentUserdata.username in anderen Klassen darauf zugreifen
#-------------------------------------------------------------------------------------------------
class StartWindow(QWidget):
    #Signal: "Jemand will zum Login"
    request_login = pyqtSignal()

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

        # Verbindung herstellen
        signin_button.clicked.connect(self.request_login.emit)


class LoginWindow(QWidget):
    request_main_window = pyqtSignal()

    def __init__(self):
        # super().__init__() ruft den Bauplan von QWidget auf, damit wir ein echtes Fenster sind
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 300)

        # Layout erstellen
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Widgets erstellen
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Pin")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Submit")

        # Widgets zum Layout hinzufügen
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Pin"))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        # Button verbinden
        login_button.clicked.connect(self.check_login)

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
                    if len(data) >= 2:
                        file_user = data[0].strip()
                        file_pw = data[1].strip()

                        if file_user == username and file_pw == password:
                            print("Login erfolgreich!")
                            user_found = True
                            self.request_main_window.emit()
                            break

            if not user_found:
                print("Benutzer oder Passwort falsch.")

        except FileNotFoundError:
            print("Fehler: userdata.txt wurde nicht gefunden!")


class MainWindow(QWidget):
    create_ticket = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ticket System")
        self.setFixedSize(300, 300)

        layout = QHBoxLayout()
        self.setLayout(layout)

        create_ticket_button = QPushButton("Create Ticket")
        my_tickets_button = QPushButton("My Ticket")
        modify_ticket_button = QPushButton("Modify Ticket")

        layout.addWidget(create_ticket_button)
        layout.addWidget(my_tickets_button)
        layout.addWidget(modify_ticket_button)

        create_ticket_button.clicked.connect(self.create_ticket.emit)

class CreateTicket(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Ticket")
        self.setFixedSize(600, 800)

        layout = QVBoxLayout()
        self.setLayout(layout)

        #Dropdown Menü
        self.dropdown = QComboBox()
        self.dropdown_Items = [" ","Safety", "Error", "test1", "test2", "test3"]
        self.dropdown.addItems(self.dropdown_Items)

        self.dropdown.setMaxVisibleItems(5)

        self.label = QLabel("I have a problem with:")

        layout.addWidget(self.label)
        layout.addWidget(self.dropdown)

        #Problem-Kurzbeschreibung
        problem_label = QLabel("Describe your problem:")
        self.problem = QLineEdit()
        self.problem.setPlaceholderText("max. 30 characters")
        self.problem.setMaxLength(30)

        layout.addWidget(problem_label)
        layout.addWidget(self.problem)

        #detailierte Problembeschreibung
        description_label = QLabel("Detailed description:")
        self.description = QLineEdit()
        self.description.setPlaceholderText("max. 250 characters")
        self.description.setMaxLength(250)

        layout.addWidget(description_label)
        layout.addWidget(self.description)

        #Submit Button
        submit_button = QPushButton("Submit")
        #submit_button.clicked.connect(self.submit)

        layout.addWidget(submit_button)

        # Attachment
        self.attachment_label = QLabel("Attachment:")
        self.attachment_button = QPushButton("Attach")

        self.attachment_button.clicked.connect(self.choose_attachment)
        layout.addWidget(self.attachment_label)
        layout.addWidget(self.attachment_button)


    def choose_attachment(self):
        datei = QFileDialog.getOpenFileName(self, "Open File", " ",
                                            "All Files ();; Pictures (.png .jpg.jpeg);;PDF (*.pdf)")

        if datei:
            self.attachment_label.setText(f"Attachment: {datei}")
            print("Attachment: ", datei)


# --- Das Hauptprogramm ---
app = QApplication(sys.argv)

# Der Manager übernimmt die Kontrolle
manager = WindowManager()
manager.show_start_screen()

app.exec()