from PyQt6.QtWidgets import (QPushButton, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QLabel, QMessageBox, QFrame)
from PyQt6.QtCore import pyqtSignal, Qt
from backend.database import Database


class LoginWindow(QWidget):
    request_main_window = pyqtSignal()
    signout_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign In")
        self.resize(760, 480)
        self.setMinimumSize(680, 420)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Linke Seite ───────────────────────────────────────────────
        left = QFrame()
        left.setStyleSheet("background-color: #000000;")
        left.setFixedWidth(300)

        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(40, 50, 40, 40)
        left_layout.setSpacing(0)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        brand = QLabel("Support\nSystem")
        brand.setStyleSheet("""
            color: #ffffff;
            font-size: 22pt;
            font-weight: bold;
            border: none;
            line-height: 1.2;
        """)
        left_layout.addWidget(brand)
        left_layout.addSpacing(16)

        tagline = QLabel("Manage and track\nyour support tickets\nin one place.")
        tagline.setStyleSheet("color: #a3a3a3; font-size: 10pt; border: none; line-height: 1.5;")
        left_layout.addWidget(tagline)
        left_layout.addStretch()

        version = QLabel("v8.0")
        version.setStyleSheet("color: #555555; font-size: 8pt; border: none;")
        left_layout.addWidget(version)

        root.addWidget(left)

        # ── Rechte Seite ──────────────────────────────────────────────
        right = QFrame()
        right.setStyleSheet("background-color: #ffffff;")

        right_layout = QVBoxLayout(right)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(60, 40, 60, 40)
        right_layout.setSpacing(0)

        title = QLabel("Welcome back")
        title.setStyleSheet("color: #0f172a; font-size: 15pt; font-weight: bold; border: none;")
        right_layout.addWidget(title)
        right_layout.addSpacing(4)

        subtitle = QLabel("Sign in to your account")
        subtitle.setStyleSheet("color: #94a3b8; font-size: 9pt; border: none;")
        right_layout.addWidget(subtitle)
        right_layout.addSpacing(28)

        right_layout.addWidget(self.label("Username"))
        right_layout.addSpacing(5)
        self.name_input = self.input("Enter your username")
        right_layout.addWidget(self.name_input)
        right_layout.addSpacing(14)

        right_layout.addWidget(self.label("Password"))
        right_layout.addSpacing(5)

        self.password_input = self.input("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.check_login)

        self.show_password = QPushButton("Show")
        self.show_password.setCheckable(True)
        self.show_password.setFixedSize(46, 40)
        self.show_password.setCursor(Qt.CursorShape.PointingHandCursor)
        self.show_password.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #94a3b8;
                border: none;
                font-size: 8pt;
                font-weight: 600;
            }
            QPushButton:hover { color: #000000; }
        """)
        self.show_password.clicked.connect(self.show_or_hide_password)

        pw_row = QHBoxLayout()
        pw_row.setSpacing(0)
        pw_row.addWidget(self.password_input)
        pw_row.addWidget(self.show_password)
        right_layout.addLayout(pw_row)
        right_layout.addSpacing(24)

        login_button = QPushButton("Sign In")
        login_button.setFixedHeight(42)
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                font-size: 10pt;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #1a1a1a; }
            QPushButton:pressed { background-color: #000000; }
        """)
        login_button.clicked.connect(self.check_login)
        right_layout.addWidget(login_button)
        right_layout.addSpacing(10)

        back_button = QPushButton("← Return to start")
        back_button.setFixedHeight(36)
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #94a3b8;
                border: none;
                font-size: 8.5pt;
            }
            QPushButton:hover { color: #475569; }
        """)
        back_button.clicked.connect(self.signout_signal.emit)
        right_layout.addWidget(back_button)

        root.addWidget(right)

    def label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #334155; font-size: 8.5pt; font-weight: 600; border: none;")
        return lbl

    def input(self, placeholder):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setFixedHeight(40)
        field.setStyleSheet("""
            QLineEdit {
                background-color: #f8fafc;
                color: #0f172a;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0px 12px;
                font-size: 9.5pt;
            }
            QLineEdit:hover { border: 1px solid #cbd5e1; }
            QLineEdit:focus {
                background-color: #ffffff;
                border: 1.5px solid #000000;
            }
        """)
        return field

    def show_or_hide_password(self, checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password.setText("Show")

    def check_login(self):
        username = self.name_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password!")
            return

        db = Database()
        success = db.check_login(username, password)

        if success is True:
            db.fetch_user_data(username, password)
            self.request_main_window.emit()
        elif success is False:
            QMessageBox.warning(self, "Error", "Wrong username or password!")
        else:
            QMessageBox.warning(self, "Error", "No database access")