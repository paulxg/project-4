from selectors import SelectSelector

from PyQt6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel

# das wird laufen
app = QApplication([])

# Hauptfenster (einf ein grosses Widget) erstellen
window = QWidget()
window.setFixedSize(300, 300)

# Alle Widgets kommen horizontal rein (rechts ran)
layout = QHBoxLayout()
window.setLayout(layout)

# Widgets erstellen
signin_button = QPushButton("Sign in")
signup_button = QPushButton("Sign up")

# Hau die Buttons ins Layout
layout.addWidget(signin_button)
layout.addWidget(signup_button)


#log in fenster
window2 = None

def sign_in():
    # window2 (die variable) bleibt im ganzen Code definiert
    global window2
    #Hauptfenster (einf ein grosses Widget) erstellen
    window2 = QWidget()
    window2.setFixedSize(300, 300)

    # vertikal alle sachen hinzufügen
    layout2 = QVBoxLayout()
    window2.setLayout(layout2)

    # Eingabefelder/submit button benennen
    name_label = QLabel("Username")
    password_label = QLabel("Pin")
    submit2_button = QPushButton("Submit")
    # Eingabefelder definiert (dass sie welche sind)
    name_input = QLineEdit()
    password_input = QLineEdit()

    #Eingabefelder/submit button hinzugefügt
    layout2.addWidget(name_label)
    layout2.addWidget(name_input)
    layout2.addWidget(password_label)
    layout2.addWidget(password_input)
    layout2.addWidget(submit2_button)

    window2.show()

    def login_clicked():  # Achte auf korrekte Funktions-Definition
        username = name_input.text()  # Kein Komma am Ende!
        password = password_input.text()  # Kein Komma am Ende!

        user_found = False  # Wir merken uns, ob wir jemanden gefunden haben

        with open(file="userdata.txt", mode="r", encoding="utf-8") as userdata:
            for line in userdata:
                data = line.strip().split(",")

                # Sicherheitscheck: Hat die Zeile überhaupt Daten?
                if len(data) >= 2:
                    if data[0] == username:
                        if data[1] == password:
                            print("Login erfolgreich!")
                            user_found = True
                            break  # Wir haben ihn, Schleife beenden!
                        else:
                            print("Passwort falsch!")
                            user_found = True  # Nutzer existiert, aber PW ist falsch
                            break

        if not user_found:
            print("Benutzer nicht gefunden!")

    submit2_button.clicked.connect(login_clicked)


signin_button.clicked.connect(sign_in)


window.show()
app.exec()

