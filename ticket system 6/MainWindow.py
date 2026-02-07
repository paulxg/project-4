from PyQt6.QtWidgets import (QHBoxLayout, QPushButton, QWidget)
from PyQt6.QtCore import pyqtSignal
from UniversalData import CurrentUserdata

class MainWindow(QWidget):
    create_ticket_signal = pyqtSignal()
    mytickets_signal = pyqtSignal()
    signout_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ticket System")
        self.setFixedSize(400, 400)

        layout = QHBoxLayout()
        self.setLayout(layout)

        create_ticket_button = QPushButton("Create Ticket")
        my_tickets_button = QPushButton("My Tickets")

        layout.addWidget(create_ticket_button)
        layout.addWidget(my_tickets_button)

        #Modify button
        if CurrentUserdata.rank == "admin":
            modify_ticket_button = QPushButton("Modify Ticket")
            layout.addWidget(modify_ticket_button)

        #signout button
        signout_button = QPushButton("Signout")
        layout.addWidget(signout_button)

        create_ticket_button.clicked.connect(self.create_ticket_signal.emit)
        my_tickets_button.clicked.connect(self.mytickets_signal.emit)
        signout_button.clicked.connect(self.signout_signal.emit)