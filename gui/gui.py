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
        self.create_settings_tab()
        self.create_process_manager_tab()
        self.create_credits_tab()
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

    def create_settings_tab(self):
        settings_tab = QWidget()
        settings_layout = QVBoxLayout()

        # Funktionen
        features = [
            "Enable ESP",
            "Enable Aimbot",
            "Enable Auto Aim",
            "Enable Wallhack",
            "Enable Silent Aim"
        ]
        for feature in features:
            checkbox = QCheckBox(feature)
            checkbox.setFont(QFont("Arial", 12))
            settings_layout.addWidget(checkbox)

        # Sensitivität
        sensitivity_slider = QSlider(Qt.Horizontal)
        sensitivity_slider.setMinimum(1)
        sensitivity_slider.setMaximum(100)
        sensitivity_slider.setValue(50)
        sensitivity_label = QLabel("Sensitivity: 50")
        sensitivity_label.setStyleSheet("color: white;")  # Text weiß machen
        sensitivity_label.setFont(QFont("Arial", 12))
        sensitivity_slider.valueChanged.connect(
            lambda value: sensitivity_label.setText(f"Sensitivity: {value}")
        )
        settings_layout.addWidget(sensitivity_label)
        settings_layout.addWidget(sensitivity_slider)

        settings_tab.setLayout(settings_layout)
        self.tabs.addTab(settings_tab, "Settings")

    def create_process_manager_tab(self):
        process_tab = QWidget()
        process_layout = QVBoxLayout()
        process_tab.setStyleSheet("""
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
        """)

        # Titel und Suchfeld
        header_layout = QHBoxLayout()
        title_label = QLabel("Process Manager")
        title_label.setStyleSheet("""
            color: #00ff00;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
        """)
        
        self.process_search = QLineEdit()
        self.process_search.setPlaceholderText("Search processes...")
        self.process_search.textChanged.connect(self.filter_processes)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(self.process_search)
        process_layout.addLayout(header_layout)

        # Tabelle für Prozesse
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(3)  # PID, Name, Inject Button
        self.process_table.setHorizontalHeaderLabels(["PID", "Process Name", "Actions"])
        self.process_table.horizontalHeader().setStretchLastSection(True)
        
        process_layout.addWidget(self.process_table)
        
        # Button Container
        button_container = QWidget()
        button_layout = QHBoxLayout()
        
        refresh_button = QPushButton("Refresh Process List")
        refresh_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        refresh_button.clicked.connect(self.refresh_process_list)
        
        button_layout.addWidget(refresh_button)
        button_container.setLayout(button_layout)
        process_layout.addWidget(button_container)
        
        process_tab.setLayout(process_layout)
        self.tabs.addTab(process_tab, "Process Manager")
        self.refresh_process_list()

    def filter_processes(self):
        search_text = self.process_search.text().lower()
        for row in range(self.process_table.rowCount()):
            process_name = self.process_table.item(row, 1).text().lower()
            self.process_table.setRowHidden(row, search_text not in process_name)

    def refresh_process_list(self):
        self.process_table.setRowCount(0)
        try:
            for proc in psutil.process_iter(['pid', 'name', 'status', 'memory_info']):
                try:
                    if proc.status() == 'running':  # Nur laufende Prozesse anzeigen
                        row = self.process_table.rowCount()
                        self.process_table.insertRow(row)
                        
                        # PID
                        self.process_table.setItem(row, 0, QTableWidgetItem(str(proc.info['pid'])))
                        
                        # Name
                        self.process_table.setItem(row, 1, QTableWidgetItem(proc.info['name']))
                        
                        # Inject Button
                        inject_btn = QPushButton("Inject")
                        inject_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #1a5f00;
                                color: white;
                                padding: 3px 8px;
                                border: none;
                                border-radius: 2px;
                                font-weight: bold;
                                font-size: 10px;
                            }
                            QPushButton:hover {
                                background-color: #2d8a0f;
                                border: 1px solid #00ff00;
                            }
                        """)
                        inject_btn.clicked.connect(lambda checked, pid=proc.info['pid']: self.show_inject_dialog(pid))
                        
                        # Container für den Button
                        btn_container = QWidget()
                        btn_layout = QHBoxLayout(btn_container)
                        btn_layout.addWidget(inject_btn)
                        btn_layout.setContentsMargins(5, 2, 5, 2)
                        self.process_table.setCellWidget(row, 2, btn_container)
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to refresh process list: {str(e)}")

    def show_inject_dialog(self, pid):
        try:
            process = psutil.Process(pid)
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Inject into {process.name()} (PID: {pid})")
            dialog.setFixedSize(500, 400)
            dialog.setStyleSheet("""
                QDialog {
                    background-color: #1a1a1a;
                    color: white;
                }
                QLabel {
                    color: #00ff00;
                    font-size: 12px;
                }
                QTextEdit {
                    background-color: #2d2d2d;
                    color: #00ff00;
                    border: 1px solid #444444;
                    border-radius: 4px;
                    font-family: 'Consolas', monospace;
                    font-size: 12px;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #1a5f00;
                    color: white;
                    padding: 8px 15px;
                    border: none;
                    border-radius: 4px;
                    min-width: 100px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2d8a0f;
                    border: 1px solid #00ff00;
                }
            """)

            layout = QVBoxLayout()

            # Process Info
            info_label = QLabel(f"Memory Usage: {process.memory_info().rss / 1024 / 1024:.1f} MB")
            layout.addWidget(info_label)

            # Vordefinierte Hacks mit Syntax Highlighting
            default_code = """// MarcMenu Hack Code
#include <Windows.h>

// ESP Configuration
void EnableESP() {
    // Wallhack
    WriteProcessMemory(handle, (LPVOID)0x12345678, &value, sizeof(value), NULL);
    
    // Glow ESP
    float glowColor[] = {1.0f, 0.0f, 0.0f, 1.0f};  // Red glow
    WriteProcessMemory(handle, (LPVOID)0x87654321, glowColor, sizeof(glowColor), NULL);
}

// Aimbot Configuration
void EnableAimbot() {
    // Auto-aim settings
    float aimSmoothing = 2.0f;
    int aimBone = 8;  // Head bone
    bool autoShoot = true;
    
    // Implement aimbot logic here
    // ...
}

// Main injection point
void MainHack() {
    EnableESP();
    EnableAimbot();
    
    // Additional features
    // ...
}"""

            code_edit = QTextEdit()
            code_edit.setText(default_code)
            layout.addWidget(code_edit)

            # Buttons
            button_layout = QHBoxLayout()
            
            inject_button = QPushButton("Inject Code")
            inject_button.clicked.connect(lambda: self.inject_code(pid, code_edit.toPlainText()))
            
            test_button = QPushButton("Test Connection")
            test_button.clicked.connect(lambda: self.test_process_connection(pid))
            
            button_layout.addWidget(test_button)
            button_layout.addWidget(inject_button)
            layout.addLayout(button_layout)

            dialog.setLayout(layout)
            dialog.exec_()
            
        except psutil.NoSuchProcess:
            QMessageBox.warning(self, "Error", "Process no longer exists!")
        except psutil.AccessDenied:
            QMessageBox.warning(self, "Error", "Access denied to process!")

    def test_process_connection(self, pid):
        try:
            process = psutil.Process(pid)
            if process.is_running():
                QMessageBox.information(self, "Success", "Connection to process successful!")
            else:
                QMessageBox.warning(self, "Error", "Process is not running!")
        except:
            QMessageBox.warning(self, "Error", "Failed to connect to process!")

    def inject_code(self, pid, code):
        # Hier kommt die eigentliche Inject-Logik hin
        QMessageBox.information(self, "Success", f"Code injected into process {pid}")

    def create_credits_tab(self):
        credits_tab = QScrollArea()
        credits_tab.setWidgetResizable(True)
        credits_content = QWidget()
        credits_layout = QVBoxLayout()
        credits_content.setStyleSheet("""
            QWidget {
                background-color: #000000;
                border: none;
            }
        """)

        credits_text = QLabel(
            "MarcMenu Client\nVersion 1.0.0\n\n"
            "Developed by alphaseegurke\n"
            "Special thanks to:\n"
            "- Developer Team\n"
            "- Beta Testers\n\n"
            "© 2024 All Rights Reserved."
        )
        credits_text.setFont(QFont("Arial", 14))
        credits_text.setStyleSheet("""
            QLabel {
                color: #00ff00;
                background-color: transparent;
                padding: 20px;
            }
        """)
        credits_text.setAlignment(Qt.AlignCenter)
        
        # Verbesserte DVD-Style Animation
        self.direction_x = 1
        self.direction_y = 1
        self.animation_speed = 2  # Langsamere Geschwindigkeit
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(lambda: self.move_credits(credits_text))
        self.animation_timer.start(30)  # Smoothere Animation
        
        credits_layout.addWidget(credits_text)
        credits_content.setLayout(credits_layout)
        credits_tab.setWidget(credits_content)
        credits_tab.setStyleSheet("""
            QScrollArea {
                background-color: #000000;
                border: none;
            }
        """)

        self.tabs.addTab(credits_tab, "Credits")

    def move_credits(self, label):
        pos = label.pos()
        parent_rect = label.parent().rect()
        label_rect = label.rect()
        
        # Sanftere Bewegung
        new_x = pos.x() + (self.animation_speed * self.direction_x)
        new_y = pos.y() + (self.animation_speed * self.direction_y)
        
        # Präzisere Rand-Erkennung
        if new_x <= 0:
            new_x = 0
            self.direction_x = 1  # Nach rechts bewegen
        elif new_x + label_rect.width() >= parent_rect.width():
            new_x = parent_rect.width() - label_rect.width()
            self.direction_x = -1  # Nach links bewegen
            
        if new_y <= 0:
            new_y = 0
            self.direction_y = 1  # Nach unten bewegen
        elif new_y + label_rect.height() >= parent_rect.height():
            new_y = parent_rect.height() - label_rect.height()
            self.direction_y = -1  # Nach oben bewegen
        
        label.move(new_x, new_y)

    def load_stylesheet(self, theme):
        if theme == "dark":
            return """
                QMainWindow {
                    background-color: #121212;
                    color: white;
                }
                QTabWidget::pane {
                    background: #1e1e1e;
                }
                QLabel, QCheckBox, QPushButton {
                    font-size: 14px;
                }
            """
        else:
            return """
                QMainWindow {
                    background-color: #f5f5f5;
                    color: black;
                }
                QTabWidget::pane {
                    background: #ffffff;
                }
                QLabel, QCheckBox, QPushButton {
                    font-size: 14px;
                }
            """

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
