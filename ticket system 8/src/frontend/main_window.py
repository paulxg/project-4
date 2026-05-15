from PyQt6.QtWidgets import (QHBoxLayout, QPushButton, QWidget)
from PyQt6.QtCore import pyqtSignal
from backend.universal_data import CurrentUserdata

class MainWindow(QWidget):
    create_ticket_signal = pyqtSignal()
    request_alltickets_signal = pyqtSignal()
    mytickets_signal = pyqtSignal()
    signout_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ticket System")
        self.resize(400, 400)
        self.setMinimumSize(300, 300)

        layout = QHBoxLayout()
        self.setLayout(layout)

        create_ticket_button = QPushButton("Create Ticket")

        layout.addWidget(create_ticket_button)

        #AllTickets Button
        if CurrentUserdata.rank == "admin":
            alltickets_button = QPushButton("All Tickets")
            layout.addWidget(alltickets_button)
            alltickets_button.clicked.connect(self.request_alltickets_signal.emit)

        else:
            my_tickets_button = QPushButton("My Tickets")
            layout.addWidget(my_tickets_button)
            my_tickets_button.clicked.connect(self.mytickets_signal.emit)


        #signout button
        signout_button = QPushButton("Signout")
        layout.addWidget(signout_button)

        create_ticket_button.clicked.connect(self.create_ticket_signal.emit)
        signout_button.clicked.connect(self.signout_signal.emit)