#registration window[Lorena]-
# und in username file schreiben [Lorena]
#todo nicht doppelte usernames [Lorena]
#todo fixen dass user wirklich in die nächste Zeile geschrieben wird [Lorena]
#todo (attachment fixen) [später]
#clear Ticket Form nach submit
#success noti nach submit
#submit button für create ticket
#user ids generieren (auto zuweisung) [Lorena]
#jedem user id hinzugefügt
#universal variablen connected
#universal_data Kategorien dahin ausgelagert
#main_window: "modify" nur für admins sichtbar
#Sicherheitsupdate: Username und Passwort nicht mehr plain in universal_data gespeichert
#Zurückbuttons + Signout
#farbige BacktoMain Buttons (dann kam der ragequit)
#txt datei wird jetzt über "csv" ausgelesen und geschrieben (wegen splitting trotz Komma in Sätzen usw.)
#Counter und Begrenzung in create Ticket
#mytickets window angebunden
#mytickets schöner machen [Paul]
#mytickets Category Bearbeitung unterbinden [Paul]
#todo MyTickets unterscheiden nach admin/user [Paul]
#todo claim/view (tickets (also abarbeiten))
#todo Priorisierung von tickets
#todo status von tickets in Bearbeitung
#todo Fenstergrößen anpassen
#todo Fenster schöner machen [Anton ist ragequitet] Lorena wirds versuchen
#todo Ticket creation Textfeld verkleinern [Anton]

import sys
from PyQt6.QtWidgets import (QApplication)

from StartWindow import StartWindow
from LoginWindow import LoginWindow
from MainWindow import MainWindow
from CreateTicket import CreateTicket
from MyTicketsWindow import MyTicketsWindow
from UniversalData import CurrentUserdata
from RegistrationWindow import RegistrationWindow
from AllTicketsWindow import AllTicketsWindow

# 1. Der Controller (Der Manager)
class Controller:
    def __init__(self):
        self.current_window = None

    def show_start_screen(self):
        #Wir erstellen das Startfenster
        self.current_window = StartWindow()

        #Wir verbinden das Signal des Fensters mit unserer Methode
        self.current_window.request_login.connect(self.show_login_screen)
        self.current_window.request_registration.connect(self.show_registration_screen)

        self.current_window.show()


    def show_login_screen(self):
        self.current_window.close()

        #Neues Fenster erstellen
        self.current_window = LoginWindow()

        self.current_window.request_main_window.connect(self.show_main_window)
        self.current_window.signout_signal.connect(self.show_start_screen)

        self.current_window.show()

        CurrentUserdata.rank = None
        CurrentUserdata.id = None

    def show_registration_screen(self):
        self.current_window.close()

        #Neues Fenster erstellen
        self.current_window = RegistrationWindow()

        self.current_window.request_main_window.connect(self.show_main_window)
        self.current_window.return_signal.connect(self.show_start_screen)

        self.current_window.show()

        CurrentUserdata.rank = None
        CurrentUserdata.id = None

    def show_main_window(self):
        self.current_window.close()

        self.current_window = MainWindow()

        self.current_window.create_ticket_signal.connect(self.create_ticket)
        self.current_window.mytickets_signal.connect(self.myticket_window)
        self.current_window.signout_signal.connect(self.show_start_screen)
        self.current_window.request_alltickets_window.connect(self.alltickets_window)

        self.current_window.show()

    def create_ticket(self):
        self.current_window.close()

        self.current_window = CreateTicket()

        self.current_window.request_main_window.connect(self.show_main_window)

        self.current_window.show()

    def myticket_window(self):
        self.current_window.close()

        self.current_window = MyTicketsWindow()

        self.current_window.request_main_window.connect(self.show_main_window)

        self.current_window.show()

    def alltickets_window(self):
        self.current_window.close()

        self.current_window = AllTicketsWindow()

        self.current_window.request_main_window.connect(self.show_main_window)

        self.current_window.show()



# --- Das Hauptprogramm ---
app = QApplication(sys.argv)

# Der Manager übernimmt die Kontrolle
manager = Controller()
manager.show_start_screen()

app.exec()