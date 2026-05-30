from PyQt6.QtWidgets import QTableView, QWidget, QVBoxLayout, QPushButton, QHeaderView, QAbstractItemView, QHBoxLayout, \
    QLineEdit, QTabWidget, QLabel, QTabBar, QTextEdit, QMessageBox, QComboBox
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from backend.database import Database
from backend.universal_data import CurrentUserdata

class TicketManagerWindow(QWidget):
    request_main_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ticket Manager")
        self.resize(950, 600)
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

        #backtomain pushbutton
        self.backtomain = QPushButton("Back to Main Window")
        self.backtomain.clicked.connect(self.request_main_window.emit)
        main_layout.addWidget(self.backtomain)
        
    # NEU: Diese Methode kümmert sich um das Erstellen und Anzeigen des Tabs
    def open_edit_tab(self, ticket_number, category):
        tab_edit = TicketEdit(ticket_number)
        # Using the full category name directly in the tab title
        self.tabs.addTab(tab_edit, f"#{ticket_number} - {category}")
        self.tabs.setCurrentWidget(tab_edit)  # Wechselt automatisch direkt in den neuen Tab

    def close_tab(self, index):
        self.tabs.removeTab(index)


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
        data = db.get_user_tickets(CurrentUserdata.id)
        self.load_table_data(data)

    def load_table_data(self, mysql_data):
        model = QStandardItemModel()
        # Added "status" to the header labels
        model.setHorizontalHeaderLabels(["ticket number", "time of issuing", "category", "short description", "detailed description", "status"])
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
    def __init__(self, ticket_number):
        super().__init__()

        db = Database()
        mysql_data = db.ticket_edit_fetch(ticket_number)
        
        #Error handling, falls Datenbank nichts zurückgibt
        # Added "N/A" for status (index 5)
        if not mysql_data:
            mysql_data = ["", "N/A", "N/A", "N/A", "N/A", "N/A"]

        layout = QVBoxLayout()
        self.setLayout(layout)

        #Date of Issueing
        date_val = str(mysql_data[1]) if mysql_data[1] else "N/A"
        date_issuing_label = QLabel(f"Date of issueing: {date_val}")

        #Support Category
        cat_val = str(mysql_data[2]) if mysql_data[2] else "N/A"
        support_category_label = QLabel(f"I have a problem with: {cat_val}")

        # Problem-Kurzbeschreibung Input
        prob_val = str(mysql_data[3]) if mysql_data[3] else "N/A"
        problem_label = QLabel(f"Describe your problem briefly: {prob_val}")
        problem_label.setWordWrap(True)

        #Detaillierte Problembeschreibung
        long_prob_val = str(mysql_data[4]) if mysql_data[4] else "N/A"
        long_problem_label = QLabel(f"Describe your problem in detail: {long_prob_val}")
        long_problem_label.setWordWrap(True)

        # Status
        status_label = QLabel("Status:")
        self.status_dropdown = QComboBox()
        self.status_dropdown.addItems(["open", "in progress", "closed"])
        # Set current status from mysql_data (index 5 for status)
        if len(mysql_data) > 5 and mysql_data[5] in ["open", "in progress", "closed"]:
            self.status_dropdown.setCurrentText(mysql_data[5])
        
        # Comment
        comment_label = QLabel("Comment:")
        self.comment_input = QTextEdit()
        self.comment_input.setFixedHeight(125)
        # Assuming comment is at index 6 if it exists, otherwise default to empty
        if len(mysql_data) > 6 and mysql_data[6]:
            self.comment_input.setText(str(mysql_data[6]))
        
        #Adding to Layout
        layout.addWidget(date_issuing_label)
        layout.addWidget(support_category_label)
        layout.addWidget(problem_label)
        layout.addWidget(long_problem_label)
        layout.addWidget(status_label)
        layout.addWidget(self.status_dropdown) # Add status dropdown to layout
        layout.addWidget(comment_label)
        layout.addWidget(self.comment_input) # Add comment input to layout

        # Submit Button
        self.submit_button = QPushButton("Submit")

        # Layouting des Submit Button
        self.submit_button.setStyleSheet("""
                        QPushButton {
                            background-color: #003B00;      
                            color: #FFFFFF;
                        }
                        QPushButton:hover {
                            background-color: #004200;      
                        }
                        QPushButton:pressed {
                            background-color: #003B00;      
                        }
                        """)

        layout.addWidget(self.submit_button)

        # NEU: Button muss zuerst erstellt werden!
        self.delete_button = QPushButton("Delete")

        def submit_action():
            status = self.status_dropdown.currentText() # Get status from dropdown
            comment = self.comment_input.toPlainText() # Get comment from QTextEdit

            if status or comment: # Only update if a status or comment is provided
                db = Database()
                db.comment_status(status, comment, ticket_number)
                QMessageBox.information(self, "Success", "Ticket status and/or comment updated!")
            else:
                QMessageBox.warning(self, "Warning", "No status or comment provided to update.")
                
        self.submit_button.clicked.connect(submit_action)

        def delete_ticket_action():
            # ticket_number_input.text() gibt es nicht, wir nehmen stattdessen die lokale Variable
            if ticket_number:  
                db = Database()
                print("jetzt delete methode aufrufen")
                if db.delete_ticket(ticket_number):
                    print("Ticket gelöscht!")
                    # Hinweis: self.load_table_data() klappt hier nicht, da das TicketEdit-Widget keinen Zugriff auf die Tabellen-Methode hat.

        self.delete_button.clicked.connect(delete_ticket_action)

        self.delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #3B0000;      
                    color: #FFFFFF;
                }
                QPushButton:hover {
                    background-color: #420000;      
                }
                QPushButton:pressed {
                    background-color: #3B0000;      
                }
                """)
        layout.addWidget(self.delete_button)