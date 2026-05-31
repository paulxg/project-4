from PyQt6.QtWidgets import QTableView, QWidget, QVBoxLayout, QPushButton, QHeaderView, QAbstractItemView, QHBoxLayout, \
    QLineEdit, QTabWidget, QLabel, QTabBar, QTextEdit, QMessageBox, QComboBox, QTextBrowser, QInputDialog
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from backend.database import Database
from backend.universal_data import CurrentUserdata

class TicketManagerWindow(QWidget):
    request_main_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ticket Manager")
        self.resize(1000, 600)
        self.setMinimumSize(600, 400)
        print("Fenster Size definiert")

        # Hauptlayout für dieses Fenster
        main_layout = QVBoxLayout(self)
        print("Hauptlayout erstellt")

        # 1. QTabWidget erstellen
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        print("QTabWidget erstellt")

        # 2. Instanz deines bestehenden Windows erstellen (jetzt als Widget)
        self.tab_mytickets = MyTicketsWindow()
        self.tabs.addTab(self.tab_mytickets, "My Tickets")
        
        # Remove the close button (x) for the first tab (index 0)
        self.tabs.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)
        self.tabs.tabBar().setTabButton(0, QTabBar.ButtonPosition.LeftSide, None)

        # NEU: Das Signal aus MyTicketsWindow abfangen, um den Tab sicher hier zu öffnen
        self.tab_mytickets.request_edit_ticket.connect(self.open_edit_tab)

        # 4. Das Tab-Widget in das Hauptfenster-Layout packen
        main_layout.addWidget(self.tabs)

        #Refresh Button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_ticket_table)
        main_layout.addWidget(self.refresh_button)

        #backtomain pushbutton
        self.backtomain = QPushButton("Back to Main Window")
        self.backtomain.clicked.connect(self.request_main_window.emit)
        main_layout.addWidget(self.backtomain)

    def refresh_ticket_table(self):
        """Leert die aktuelle Tabelle und lädt die Tickets neu aus der Datenbank."""
        db = Database()
        mysql_data = db.get_user_tickets(CurrentUserdata.id)
        self.tab_mytickets.load_table_data(mysql_data)

    # NEU: Diese Methode kümmert sich um das Erstellen und Anzeigen des Tabs
    def open_edit_tab(self, ticket_number, category):
        tab_edit = TicketEdit(ticket_number)
        tab_edit.ticket_deleted.connect(self.handle_ticket_deleted)
        # Using the full category name directly in the tab title
        self.tabs.addTab(tab_edit, f"#{ticket_number} - {category}")
        self.tabs.setCurrentWidget(tab_edit)  # Wechselt automatisch direkt in den neuen Tab

    def close_tab(self, index):
        widget = self.tabs.widget(index)
        self.tabs.removeTab(index)
        if widget:
            widget.deleteLater()

    def handle_ticket_deleted(self):
        """Schließt den Tab des gelöschten Tickets und aktualisiert die Tabelle."""
        widget = self.sender()  # Holt sich das Widget, welches das Signal ausgelöst hat
        if widget:
            index = self.tabs.indexOf(widget)
            if index != -1:
                self.close_tab(index)
        self.refresh_ticket_table()


class MyTicketsWindow(QWidget):
    request_edit_ticket = pyqtSignal(str, str) # NEU: Signal transmits ticket number and category

    def __init__(self):
        super().__init__()

        #Widget bekommt vertical layout, für weitere buttons unter Tabelle
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        #QTableview für Tabellenansicht
        self.tableview = QTableView() #sorgt für das tabellenartige Aussehen
        self.tableview.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) #Unterbindung editing
        self.tableview.doubleClicked.connect(self.edit_ticket)
        
        #Tabellenanpassung an Fenstergröße
        self.tableview.resizeColumnsToContents()
        self.tableview.resizeRowsToContents()
        self.tableview.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableview.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        #Widgets ins Layout packen
        self.layout.addWidget(self.tableview)

        db = Database()
        mysql_data = db.get_user_tickets(CurrentUserdata.id)
        self.load_table_data(mysql_data)

    def load_table_data(self, mysql_data):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ticket number", "time of issuing", "category", "short description", "detailed description", "status", "responsible admin id"])
        for row in mysql_data:
            items = [QStandardItem(str(field) if field else "") for field in row]
            model.appendRow(items)
        self.tableview.setModel(model)
    
    def edit_ticket(self, index):
        # Die Zeile des angeklickten Elements aus dem index holen
        row = index.row()
        # Das Model der Tabelle abrufen
        model = self.tableview.model()
        # Den Wert aus der angeklickten Zeile, Spalte 0 (ticket number) auslesen
        ticket_number = model.index(row, 0).data()
        # Den Wert aus der angeklickten Zeile, Spalte 2 (category) auslesen
        category = model.index(row, 2).data()
        
        # Ticketnummer per Signal an TicketManagerWindow schicken, falls wir nicht ins Leere geklickt haben
        if ticket_number and category:
            self.request_edit_ticket.emit(str(ticket_number), str(category))


class TicketEdit(QWidget):
    ticket_deleted = pyqtSignal()

    def __init__(self, ticket_number):
        super().__init__()
        self.ticket_number = ticket_number

        mysql_data = Database().ticket_edit_fetch(ticket_number) or ["", "N/A", "N/A", "N/A", "N/A", "N/A"]

        layout = QVBoxLayout()
        self.setLayout(layout)

        date_label = QLabel(f"Date of issueing: {mysql_data[1] or 'N/A'}")
        cat_label = QLabel(f"I have a problem with: {mysql_data[2] or 'N/A'}")
        prob_label = QLabel(f"Describe your problem briefly: {mysql_data[3] or 'N/A'}")
        prob_label.setWordWrap(True)
        long_prob_label = QLabel("Describe your problem in detail:")
        long_prob_text = QTextEdit()
        long_prob_text.setPlainText(mysql_data[4] or 'N/A')
        long_prob_text.setReadOnly(True)
        long_prob_text.setFixedHeight(60)

        layout.addWidget(date_label)
        layout.addWidget(cat_label)
        layout.addWidget(prob_label)
        layout.addWidget(long_prob_label)
        layout.addWidget(long_prob_text)

        if mysql_data[5] in ["in progress", "closed"]:
            # Chat
            self.chat_display = QTextBrowser()
            self.chat_display.setFixedHeight(120)
            self.chat_input = QLineEdit()
            self.chat_input.setPlaceholderText("Enter message...")
            self.chat_send_button = QPushButton("Send")
            self.chat_send_button.clicked.connect(self.send_message)
            self.chat_input.returnPressed.connect(self.send_message)
            layout.addWidget(QLabel("Chat:"))
            layout.addWidget(self.chat_display)

            if mysql_data[5] in ["in progress"]:
                chat_input_layout = QHBoxLayout()
                chat_input_layout.addWidget(self.chat_input)
                chat_input_layout.addWidget(self.chat_send_button)
                layout.addLayout(chat_input_layout)

            self.load_messages()

        if CurrentUserdata.rank == "admin":
            self.status_dropdown = QComboBox()
            self.status_dropdown.addItems(["open", "in progress", "closed"])
            if mysql_data[5] in ["open", "in progress", "closed"]:
                self.status_dropdown.setCurrentText(mysql_data[5])

            self.submit_button = QPushButton("Submit")
            self.submit_button.setStyleSheet("""
                QPushButton { background-color: #003B00; color: #FFFFFF; }
                QPushButton:hover { background-color: #004200; }
                QPushButton:pressed { background-color: #003B00; }
            """)
            self.submit_button.clicked.connect(self.submit_action)

            layout.addWidget(QLabel("Status:"))
            layout.addWidget(self.status_dropdown)
            layout.addWidget(self.submit_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setStyleSheet("""
            QPushButton { background-color: #3B0000; color: #FFFFFF; }
            QPushButton:hover { background-color: #420000; }
            QPushButton:pressed { background-color: #3B0000; }
        """)
        self.delete_button.clicked.connect(self.delete_ticket)
        layout.addWidget(self.delete_button)

    def load_messages(self):
        messages = Database().get_messages(self.ticket_number)
        content = f"<i> Hello, an admin is currently reviewing your ticket and will get back to you as soon as possible. Please provide any further information available below or pay for faster service.</i> <br> <br>" + "".join(
            f"<b>[{username}]</b> {timestamp} &mdash; {message}<br>"
            for username, message, timestamp in messages
        )
        self.chat_display.setHtml(content)
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    def send_message(self):
        text = self.chat_input.text().strip()
        if text:
            Database().send_message(self.ticket_number, CurrentUserdata.id, text)
            self.chat_input.clear()
            self.load_messages()

    def submit_action(self):
        status = self.status_dropdown.currentText()

        if status == "closed":
            text, ok = QInputDialog.getText(self, "Final Comment", "Please enter a final comment to close the ticket:")
            if ok and text.strip(): # Prüfen, ob OK geklickt wurde und der Text nicht leer ist
                Database().send_message(self.ticket_number, CurrentUserdata.id, text.strip())
                # Chatfenster direkt updaten, falls es bereits gerendert ist
                if hasattr(self, 'chat_display'):
                    self.load_messages()
            else:
                QMessageBox.warning(self, "Warning", "A final comment is required to close the ticket.")
                return # Funktion abbrechen, das Ticket wird noch nicht geschlossen!

        if status:
            Database().update_status(status, self.ticket_number)
            QMessageBox.information(self, "Success", "Ticket status updated!")
        else:
            QMessageBox.warning(self, "Warning", "No status provided to update.")

    def delete_ticket(self):
        if self.ticket_number:
            Database().delete_ticket(self.ticket_number)
            self.ticket_deleted.emit()