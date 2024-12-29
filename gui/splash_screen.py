from PySide6.QtWidgets import QSplashScreen, QVBoxLayout, QLabel, QProgressBar, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)  # Fenster ohne Rand
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #121212; color: white;")

        # Layout und Widgets
        layout = QVBoxLayout(self)
        logo = QLabel(self)
        logo.setPixmap(QPixmap("D:\Cheat Menus\MarcMenu\picture\MM.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(logo, alignment=Qt.AlignCenter)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2b2b2b;
                color: white;
                border-radius: 10px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.progress_bar)

        self.label = QLabel("Loading...")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

    def start_loading(self, callback):
        self.progress = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)
        self.callback = callback

    def update_progress(self):
        self.progress += 1
        self.progress_bar.setValue(self.progress)
        if self.progress >= 100:
            self.timer.stop()
            self.callback()
