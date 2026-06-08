from PyQt6.QtWidgets import (QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel, QComboBox, QFileDialog, QTextEdit,
                             QMessageBox)
from backend.universal_data import CurrentUserdata, ProgramData
from backend.prioritizing import Prioritizing
from PyQt6.QtCore import pyqtSignal
from backend.database import Database, DatabaseError


class CreateTicket(QWidget):
    request_main_window = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Ticket")
        self.resize(550, 600)
        self.setMinimumSize(450, 500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        #Dropdown Menü
        self.dropdown = QComboBox()
        self.dropdown_Items = ProgramData.support_categories
        self.dropdown.addItems(self.dropdown_Items)
        self.category = ""

        # Begrenzung der Anzeige im Dropdown
        self.dropdown.setMaxVisibleItems(5)

        # Label für Dropdown
        self.label = QLabel("I have a problem with:*")
        layout.addWidget(self.label)
        layout.addWidget(self.dropdown)

        # Problem-Kurzbeschreibung Input
        problem_label = QLabel("Describe your problem briefly:*")
        self.problem = QLineEdit()
        self.problem.setPlaceholderText("max. 30 characters")
        self.problem.setMaxLength(30)

        layout.addWidget(problem_label)
        layout.addWidget(self.problem)

        # detaillierte Problembeschreibung
        long_problem_label = QLabel("Describe your problem in detail:")
        self.description = QTextEdit()
        self.description.setFixedHeight(125)
        self.description.setPlaceholderText("Max 200 characters")
        layout.addWidget(long_problem_label)
        layout.addWidget(self.description)

        # Character Counter
        self.character_counter = QLabel("0/250")
        layout.addWidget(self.character_counter)

        # Signal für das Counter-Updating
        self.description.textChanged.connect(self.update_character_counter)

        #Pflichtfeld
        required = QLabel("*required inputs")
        layout.addWidget(required)


        # Submit Button
        self.submit_button = QPushButton("Submit")

        #Layouting des Submit Button
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
        self.submit_button.clicked.connect(self.submit)

        layout.addWidget(self.submit_button)

        # Back to Main Button
        self.backmain = QPushButton("Back to Main Window")
        self.backmain.clicked.connect(self.request_main_window.emit)

        # layouting des Back to Main Button
        self.backmain.setStyleSheet("""
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

        layout.addWidget(self.backmain)
        self.problem_quick = ""
        self.datetime = ""
        self.factor = ""

# Update Character Counter
    def update_character_counter(self):
        text = self.description.toPlainText()
        length = len(text)
        self.max_len = 250

        if length <= self.max_len-50:
            self.character_counter.setStyleSheet("color: white;")
        if length >= self.max_len :
            self.character_counter.setStyleSheet("color: orange;")
        if length > self.max_len:
            self.character_counter.setStyleSheet("color: red;")

        self.character_counter.setText(f"{length}/{self.max_len}")

#Funktion des Submit Button
    def submit(self):
        print("submit started")
        category = self.dropdown.currentText()
        problem_quick = self.problem.text()
        text = self.description.toPlainText()
        text_to_single_line = text.replace("\n", " ").replace("\r", "")
        print("text successfully fetched from widgets")

        p = Prioritizing()
        p.setprio(category)
        print(f"Your ticket priority is {p.prio}")
        self.factor = p.prio

        #text length check
        if len(text_to_single_line) > 250:
            #PopUp wenn zu lang und Submitted
            print("Description too long!")
            QMessageBox.warning(self, "Error", f"Description exceeds {self.max_len} characters")

        elif len(problem_quick) == 0:
            print("Quick description required")
            QMessageBox.warning(self, "Error", "Quick description required!")


        else:
            print("text length check successful")
            try:
                db = Database()
                db.create_ticket(
                    CurrentUserdata.id,
                    self.factor,
                    category,
                    problem_quick,
                    text_to_single_line,
                    "open"  # Automatically assign "open" status
                )

                # Inputs in die Textboxen löschen nach dem schreiben
                inputs1 = self.findChildren(QLineEdit)
                for input_field in inputs1:
                    input_field.clear()

                inputs2 = self.findChildren(QTextEdit)
                for input_field in inputs2:
                    input_field.clear()
                self.success_notification()
            except DatabaseError as e:
                QMessageBox.critical(self, "Database Error", str(e))

    def success_notification(self):
        success = QMessageBox()
        choice = self.dropdown.currentText()
        success.setWindowTitle("Success")
        success.setText(f"Your Ticket concerning {choice} has been received!")
        success.exec()