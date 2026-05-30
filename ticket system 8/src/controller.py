#todo claim/view (tickets (also abarbeiten))
#todo zeitbasierte Priorisierung von tickets
#todo error handling: im Terminal oder auch im Programm?
#todo ticket autolöschen nach ticketschließen; alternativ: prio=0
#todo automatisch Fenster close nach comment (admin) WEEEEEEN juckt das

#todo Fenster schöner machen [Anton ist wieder im Game!]
#todo passwort hashen mit bcrypt (Paul)
#todo user löschen/bearbeiten etc.
#todo Wie kann der Admin mit dem Kunden in Kontakt treten? (Anstelle von Username vllt email?)
#todo Filterfunktion (mit order/Group by sql befehl)
#todo my account view / profil zum ändern von Name etc
#todo anschauen von rank userinfo etc
#todo created tickets resolved tickets open tickets (count)
#todo Suchfeld in Ticket Tabelle zum Suchen nach stichwörtern
#todo passwort ändern im Profil
#todo admin dashboard ( wv tickets sinbd offen/ in bearbeitung pro kategorie etc)
#fehlerlog?
#todo ticket nur bearbeiten/zurückziewhen wenn auch offen
#todo alte tickets im log?
#darkmode?
#todo claim ticket/ bearbeiter definieren
#todo tickets als pdf csv exportieren
#todo log, wer hat wann was gelöscht
#passwort stärke bei registrtierung
#todo Datenbankverbindung auto wieder herstellen wenn weg ohne restart
#todo Animierter Übergang zwischen Fenstern (vllt einfach stacked widget)
#todo Farbige Kategorie-Badges in der Ticket-Tabelle
#todo Ticket-Zähler als Badge auf dem „My Tickets"-Button
#todo Ticket-Dringlichkeit automatisch aus der Beschreibung erkennen (Schlüsselwörter wie „dringend", „funktioniert nicht")
#todo Dark/Light Mode pro Nutzer gespeichert in der Datenbank
#todo filter nach insults
#todo user notification bei Ticket Bearbeitung

from frontend.start_window import StartWindow
from frontend.login_window import LoginWindow
from frontend.main_window import MainWindow
from frontend.create_ticket import CreateTicket
from frontend.mytickets_window import TicketManagerWindow
from backend.universal_data import CurrentUserdata
from frontend.registration_window import RegistrationWindow


#Controller
class Controller:
    def __init__(self):
        self.current_window = None
        self.show_start_screen()

    def show_start_screen(self):
        self.current_window = StartWindow()

        #Wir verbinden das Signal des Fensters mit unserer Methode
        self.current_window.request_login.connect(self.show_login_screen)
        self.current_window.request_registration.connect(self.show_registration_screen)

        self.current_window.show()

    def show_login_screen(self):
        self.current_window.close()

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

        print("TicketManager aufrufen")
        self.current_window = TicketManagerWindow()

        self.current_window.request_main_window.connect(self.show_main_window)

        self.current_window.show()
