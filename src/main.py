from UserInterface import WelcomeScreen
from PyQt6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
app.setStyle("Fusion")
main_window = WelcomeScreen()

main_window.setWindowTitle("Open Cell Lab")
main_window.show()
sys.exit(app.exec())