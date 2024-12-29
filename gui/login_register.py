from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, 
                              QMessageBox, QDialog, QLabel, QTextEdit)
from PySide6.QtCore import Qt, Signal
from .access_codes import VALID_ACCESS_CODES
from .gui import ESPAimbotGUI
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import pytz

# Liste für dynamisch registrierte Codes
registered_codes = []

class ContactDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Contact Owner")
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 12px;
            }
            QLineEdit, QTextEdit {
                background-color: #333333;
                color: white;
                padding: 8px;
                border: 1px solid #444444;
                border-radius: 4px;
                margin: 5px;
            }
            QPushButton {
                background-color: #333333;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #444444;
                border: 1px solid #00ff00;
            }
        """)

        layout = QVBoxLayout()

        # Email
        layout.addWidget(QLabel("Your Email:"))
        self.email = QLineEdit()
        layout.addWidget(self.email)

        # Name
        layout.addWidget(QLabel("Your Name:"))
        self.name = QLineEdit()
        layout.addWidget(self.name)

        # Age
        layout.addWidget(QLabel("Your Age:"))
        self.age = QLineEdit()
        layout.addWidget(self.age)

        # Reason
        layout.addWidget(QLabel("Reason for Usage (min 15 words.):"))
        self.reason = QTextEdit()
        self.reason.setPlaceholderText("Please explain why you want to use MarcMenu...")
        layout.addWidget(self.reason)

        # Send Button
        self.send_button = QPushButton("Send Request")
        self.send_button.clicked.connect(self.send_email)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def send_email(self):
        if not all([self.email.text(), self.name.text(), self.age.text(), self.reason.toPlainText()]):
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
            return

        # Get current time in Germany
        de_tz = pytz.timezone('Europe/Berlin')
        current_time = datetime.now(de_tz)
        time_of_day = "morning" if 5 <= current_time.hour < 12 else "day" if 12 <= current_time.hour < 18 else "evening"

        email_content = f"""Good {time_of_day},

I need access to your "MarcMenu" I would be happy to receive positive feedback.

Here are my Details:
Name: {self.name.text()}
Age: {self.age.text()}
Email: {self.email.text()}
Reason: {self.reason.toPlainText()}

Your {self.name.text()}!"""

        try:
            msg = MIMEText(email_content)
            msg['Subject'] = "Zugangscode Anfrage"
            msg['From'] = self.email.text()
            msg['To'] = "alphaseegurke@gmail.com"

            # SMTP-Konfiguration für Gmail mit SSL
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # SSL statt TLS
            server.login("sendtoalphaseegurke@gmail.com", "wkcc ewaa orhs lljc")
            server.send_message(msg)
            server.quit()

            QMessageBox.information(self, "Success", "Request sent successfully! Now wait up to 24 Hours for respond.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to send email: {str(e)}")

class LoginRegisterScreen(QWidget):
    login_successful = Signal()  # Neues Signal

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
            }
            QLineEdit {
                background-color: #333333;
                color: white;
                padding: 8px;
                border: 1px solid #444444;
                border-radius: 4px;
                margin: 5px;
            }
            QPushButton {
                background-color: #333333;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #444444;
                border: 1px solid #00ff00;
            }
        """)

        layout = QVBoxLayout()

        self.code_input = QLineEdit(self)
        self.code_input.setPlaceholderText("Access Code")
        self.code_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.code_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        # Contact Owner Button
        self.contact_button = QPushButton("Contact Owner", self)
        self.contact_button.clicked.connect(self.show_contact_dialog)
        layout.addWidget(self.contact_button)

        self.setLayout(layout)

    def login(self):
        access_code = self.code_input.text()
        if access_code in VALID_ACCESS_CODES or access_code in registered_codes:
            success_box = QMessageBox(self)
            success_box.setIcon(QMessageBox.Information)
            success_box.setWindowTitle("Erfolg")
            success_box.setText("Anmeldung erfolgreich!")
            success_box.setStyleSheet("""
                QMessageBox {
                    background-color: #1a1a1a;
                }
                QMessageBox QLabel {
                    color: white;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #333333;
                    color: white;
                    padding: 6px 14px;
                    border: none;
                    border-radius: 4px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #444444;
                    border: 1px solid #00ff00;
                }
            """)
            success_box.exec()
            self.hide()
            self.main_window = ESPAimbotGUI()
            self.main_window.show()
            self.login_successful.emit()
        else:
            error_box = QMessageBox(self)
            error_box.setIcon(QMessageBox.Warning)
            error_box.setWindowTitle("Fehler")
            error_box.setText("Ungültiger Zugangscode!")
            error_box.setStyleSheet("""
                QMessageBox {
                    background-color: #1a1a1a;
                }
                QMessageBox QLabel {
                    color: white;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #333333;
                    color: white;
                    padding: 6px 14px;
                    border: none;
                    border-radius: 4px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #444444;
                    border: 1px solid #00ff00;
                }
            """)
            error_box.exec()

    def register(self):
        access_code = self.code_input.text()
        if access_code not in VALID_ACCESS_CODES and access_code not in registered_codes:
            registered_codes.append(access_code)
            QMessageBox.information(self, "Erfolg", "Registrierung erfolgreich!")
        else:
            QMessageBox.warning(self, "Fehler", "Zugangscode bereits verwendet!") 

    def show_contact_dialog(self):
        dialog = ContactDialog(self)
        dialog.exec_() 