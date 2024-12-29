import sys
from threading import Thread
from PySide6.QtWidgets import QApplication
from gui.gui import ESPAimbotGUI
from esp.rendering import render_esp
from memory.memory_access import memory_access
from utils.logger import setup_logger
from gui.login_register import LoginRegisterScreen

class MainApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_screen = LoginRegisterScreen()
        self.login_screen.login_successful.connect(self.start_main_application)
        self.login_screen.show()

    def start_main_application(self):
        # Start ESP-Rendering in einem Thread
        Thread(target=render_esp, daemon=True).start()

        # Start Memory Access
        Thread(target=memory_access, daemon=True).start()

    def run(self):
        return self.app.exec()

if __name__ == "__main__":
    # Logger einrichten
    setup_logger("access_log.log")

    main_app = MainApplication()
    sys.exit(main_app.run())
