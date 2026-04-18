#todo (attachment fixen) [später]
#todo claim/view (tickets (also abarbeiten))
#todo Priorisierung von tickets
#todo status von tickets in Bearbeitung
#todo Fenstergrößen anpassen
#todo Fenster schöner machen [Anton ist ragequitet] Lorena wirds versuchen
#todo Login connecten Database (Lorena)
#todo AllTickets & MyTickets Database (Paul)
#todo Create ticket Database (Anton)
#todo passwort hashen mit bcrypt (Paul)
#todo user löschen/bearbeiten etc.
#todo main.py window einführen, die den Controller startet (weil Konvention)

import sys
from PyQt6.QtWidgets import (QApplication)

from frontend.start_window import StartWindow
from frontend.login_window import LoginWindow
from frontend.main_window import MainWindow
from frontend.create_ticket import CreateTicket
from frontend.mytickets_window import MyTicketsWindow
from backend.universal_data import CurrentUserdata
from frontend.registration_window import RegistrationWindow


# 1. Der Controller (Der Manager)
class Controller:
    def __init__(self):
        self.current_window = None
        self.show_start_screen()

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
