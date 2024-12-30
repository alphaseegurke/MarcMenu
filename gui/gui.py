import sys
from threading import Thread
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QTabWidget, QWidget, QLabel, QSlider,
    QCheckBox, QPushButton, QTableWidget, QTableWidgetItem, QScrollArea, QLineEdit, QMessageBox,
    QApplication, QStyle, QHBoxLayout, QTextEdit, QDialog
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import psutil
import shutil
import os
from pathlib import Path
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtCore import QPoint

def setup_logger(log_file):
    print(f"Logger setup in file: {log_file}")

def render_esp():
    print("ESP rendering started.")

def memory_access():
    print("Memory access started.")

# Liste der Zugangscodes
access_codes = []

class ESPAimbotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarcMenu")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QMenuBar, QTabBar, QTabWidget::tab-bar {
                background-color: #000000;
            }
            QTabWidget::pane {
                border: 1px solid #333333;
                background: #222222;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #000000;
                color: #ffffff;
                padding: 8px 20px;
                margin: 2px;
                border-radius: 3px;
            }
            QTabBar::tab:selected {
                background: #1a1a1a;
                border-bottom: 2px solid #00ff00;
            }
            QPushButton {
                background-color: #333333;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #444444;
                border: 1px solid #00ff00;
            }
            QCheckBox {
                color: white;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #333333;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #00ff00;
                background: #00ff00;
                border-radius: 3px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #666666;
                height: 8px;
                background: #333333;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #00ff00;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QTableWidget {
                background-color: #222222;
                color: white;
                gridline-color: #333333;
                border-radius: 5px;
                padding: 5px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: white;
                padding: 5px;
                border: none;
            }
            QLineEdit {
                background-color: #333333;
                color: white;
                padding: 8px;
                border: 1px solid #444444;
                border-radius: 4px;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)

        # Hauptlayout
        self.layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()
        self.create_home_tab()
        self.create_performance_boost_tab()
        self.create_cheats_tab()
        self.create_process_manager_tab()
        self.create_premium_tab()
        self.create_credits_tab()
        self.create_admin_tab()
        self.layout.addWidget(self.tabs)

        # Notfall-Quit Button
        self.emergency_button = QPushButton("Emergency Exit")
        self.emergency_button.setStyleSheet("""
            QPushButton {
                background-color: #660000;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #990000;
                border: 1px solid #ff0000;
            }
        """)
        self.emergency_button.clicked.connect(self.emergency_exit)
        self.layout.addWidget(self.emergency_button)

        # Setze Layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def create_home_tab(self):
        home_tab = QWidget()
        home_layout = QVBoxLayout()

        welcome_label = QLabel("Willkommen zu MarcMenu!")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        home_layout.addWidget(welcome_label)

        info_label = QLabel("Hier sind alle wichtigen Informationen und Funktionen.")
        info_label.setStyleSheet("color: white;")
        home_layout.addWidget(info_label)

        # Weitere wichtige Informationen können hier hinzugefügt werden

        home_tab.setLayout(home_layout)
        self.tabs.addTab(home_tab, "Home")

    def create_performance_boost_tab(self):
        performance_tab = QWidget()
        performance_layout = QVBoxLayout()

        performance_label = QLabel("Performance Boost Optionen:")
        performance_label.setStyleSheet("color: white;")
        performance_layout.addWidget(performance_label)

        # Beispieloptionen basierend auf dem Bild
        options = [
            "Windows Power Throttling",
            "Hibernation",
            "Windows Telemetry",
            "Windows Update Telemetry"
        ]
        for option in options:
            checkbox = QCheckBox(option)
            checkbox.setStyleSheet("color: white;")
            performance_layout.addWidget(checkbox)

        apply_button = QPushButton("Alle Optimierungen anwenden")
        apply_button.setStyleSheet("background-color: #00ff00; color: black;")
        performance_layout.addWidget(apply_button)

        performance_tab.setLayout(performance_layout)
        self.tabs.addTab(performance_tab, "Performance")

    def create_cheats_tab(self):
        cheats_tab = QWidget()
        cheats_layout = QVBoxLayout()

        cheats_label = QLabel("Cheats für dein Spiel:")
        cheats_label.setStyleSheet("color: white;")
        cheats_layout.addWidget(cheats_label)

        # Beispieloptionen basierend auf dem Bild
        cheats_options = [
            "Gott-Modus",
            "Unbegrenzte Munition",
            "Teleport",
            "Unsichtbarkeit"
        ]
        for cheat in cheats_options:
            checkbox = QCheckBox(cheat)
            checkbox.setStyleSheet("color: white;")
            cheats_layout.addWidget(checkbox)

        cheats_tab.setLayout(cheats_layout)
        self.tabs.addTab(cheats_tab, "Cheats")

    def create_process_manager_tab(self):
        process_tab = QWidget()
        process_layout = QVBoxLayout()

        process_label = QLabel("Aktive Prozesse:")
        process_label.setStyleSheet("color: white;")
        process_layout.addWidget(process_label)

        self.process_table = QTableWidget()
        self.process_table.setColumnCount(2)
        self.process_table.setHorizontalHeaderLabels(["Prozessname", "PID"])
        self.load_processes()
        process_layout.addWidget(self.process_table)

        inject_button = QPushButton("In Spiel injizieren")
        inject_button.clicked.connect(self.inject_into_game)
        process_layout.addWidget(inject_button)

        process_tab.setLayout(process_layout)
        self.tabs.addTab(process_tab, "Process Manager")

    def load_processes(self):
        processes = psutil.process_iter(['name', 'pid'])
        self.process_table.setRowCount(0)
        for process in processes:
            row_position = self.process_table.rowCount()
            self.process_table.insertRow(row_position)
            self.process_table.setItem(row_position, 0, QTableWidgetItem(process.info['name']))
            self.process_table.setItem(row_position, 1, QTableWidgetItem(str(process.info['pid'])))

    def inject_into_game(self):
        # Logik zum Injizieren in ein Spiel implementieren
        QMessageBox.information(self, "Injizieren", "In Spiel injizieren Funktion ist noch nicht implementiert.")

    def create_premium_tab(self):
        premium_tab = QWidget()
        premium_layout = QVBoxLayout()

        premium_label = QLabel("Kaufe Premium-Funktionen!")
        premium_label.setStyleSheet("font-size: 24px; color: white;")
        premium_layout.addWidget(premium_label)

        premium_info = QLabel("Erhalte Zugriff auf exklusive Cheats und Funktionen.")
        premium_info.setStyleSheet("color: white;")
        premium_layout.addWidget(premium_info)

        buy_button = QPushButton("Jetzt kaufen")
        buy_button.setStyleSheet("background-color: #00ff00; color: black;")
        premium_layout.addWidget(buy_button)

        premium_tab.setLayout(premium_layout)
        self.tabs.addTab(premium_tab, "Premium")

    def create_credits_tab(self):
        credits_tab = QWidget()
        credits_layout = QVBoxLayout()
        credits_label = QLabel("Credits")
        credits_label.setStyleSheet("color: white;")
        credits_layout.addWidget(credits_label)
        credits_tab.setLayout(credits_layout)
        self.tabs.addTab(credits_tab, "Credits")

    def create_admin_tab(self):
        admin_tab = QWidget()
        admin_layout = QVBoxLayout()

        # Admin Zugangscode
        self.admin_code_input = QLineEdit()
        self.admin_code_input.setPlaceholderText("Admin Zugangscode")
        admin_layout.addWidget(self.admin_code_input)

        admin_button = QPushButton("Zugang gewähren")
        admin_button.clicked.connect(self.check_admin_access)
        admin_layout.addWidget(admin_button)

        self.admin_message = QLabel("")
        admin_layout.addWidget(self.admin_message)

        admin_tab.setLayout(admin_layout)
        self.tabs.addTab(admin_tab, "Admin")

        # Admin-Funktionen (initial versteckt)
        self.admin_functions = QWidget()
        self.admin_functions_layout = QVBoxLayout()
        self.admin_functions_label = QLabel("Admin-Funktionen hier...")
        self.admin_functions_layout.addWidget(self.admin_functions_label)
        self.admin_functions.setLayout(self.admin_functions_layout)
        self.admin_functions.setVisible(False)  # Standardmäßig versteckt
        admin_layout.addWidget(self.admin_functions)

    def check_admin_access(self):
        admin_code = self.admin_code_input.text()
        if admin_code == "DEIN_ADMIN_CODE":  # Ersetze durch deinen echten Admin-Code
            self.admin_message.setText("Zugang gewährt!")
            self.admin_functions.setVisible(True)  # Admin-Funktionen anzeigen
        else:
            self.admin_message.setText("Ungültiger Zugangscode!")

    def emergency_exit(self):
        warning_box = QMessageBox(self)
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setWindowTitle("Emergency Exit")
        warning_box.setText("Emergency Exit - Are you sure?")
        warning_box.setInformativeText(
            "This will:\n"
            "1. Create a backup in Documents/SystemBackup\n"
            "2. Close all program processes\n"
            "3. Exit immediately\n\n"
            "Backup location: " + str(Path.home() / "Documents" / "SystemBackup")
        )
        warning_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        warning_box.setDefaultButton(QMessageBox.No)
        warning_box.setStyleSheet("""
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
        
        result = warning_box.exec()
        
        if result == QMessageBox.Yes:
            try:
                # Backup-Pfad erstellen
                documents_path = Path.home() / "Documents" / "SystemBackup"
                documents_path.mkdir(parents=True, exist_ok=True)
                
                # Aktuelles Verzeichnis kopieren
                current_dir = Path(__file__).parent.parent
                backup_path = documents_path / "data"
                shutil.copytree(current_dir, backup_path, dirs_exist_ok=True)
                
                # Erfolgsmeldung
                QMessageBox.information(
                    self,
                    "Backup Created",
                    f"Backup successfully created at:\n{backup_path}",
                    QMessageBox.Ok
                )
                
                # Alle Prozesse und Fenster schließen
                self.close()
                QApplication.quit()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Emergency exit failed: {str(e)}",
                    QMessageBox.Ok
                )
                QApplication.quit()

class LoginRegisterScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login/Register")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()

        self.code_input = QLineEdit(self)
        self.code_input.setPlaceholderText("Zugangscode")
        self.code_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.code_input)

        self.remember_me_checkbox = QCheckBox("Angemeldet bleiben")
        layout.addWidget(self.remember_me_checkbox)

        self.login_button = QPushButton("Anmelden", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Registrieren", self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        access_code = self.code_input.text()
        if access_code in access_codes:
            QMessageBox.information(self, "Erfolg", "Anmeldung erfolgreich!")
        else:
            QMessageBox.warning(self, "Fehler", "Ungültiger Zugangscode!")

    def register(self):
        access_code = self.code_input.text()
        if access_code not in access_codes:
            access_codes.append(access_code)
            QMessageBox.information(self, "Erfolg", "Registrierung erfolgreich!")
        else:
            QMessageBox.warning(self, "Fehler", "Zugangscode bereits verwendet!")

if __name__ == "__main__":
    # Logger einrichten
    setup_logger("esp_aimbot.log")

    # Start ESP-Rendering in einem Thread
    Thread(target=render_esp, daemon=True).start()

    # Start Memory Access
    Thread(target=memory_access, daemon=True).start()

    # Starte GUI
    app = QApplication(sys.argv)

    main_window = ESPAimbotGUI()
    main_window.show()

    sys.exit(app.exec())
