from UserInterface import WelcomeScreen, MainScreen
from PyQt6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
main_window = MainScreen()
main_window.setWindowTitle("Open Cell Lab")
main_window.show()
sys.exit(app.exec())