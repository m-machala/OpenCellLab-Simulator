import os

if os.environ.get("XDG_SESSION_TYPE") == "wayland":
    os.environ["QT_QPA_PLATFORM"] = "xcb"

from UserInterface import WelcomeScreen
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
import sys

app = QApplication(sys.argv)
app.setStyle("Fusion")

main_window = WelcomeScreen()

icon = QIcon()
filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
icon.addFile(os.path.join(filePath, "16x16.png"), QSize(16, 16))
icon.addFile(os.path.join(filePath, "32x32.png"), QSize(32, 32))
icon.addFile(os.path.join(filePath, "48x48.png"), QSize(48, 48))
icon.addFile(os.path.join(filePath, "64x64.png"), QSize(64, 64))
icon.addFile(os.path.join(filePath, "128x128.png"), QSize(128, 128))
app.setWindowIcon(icon)
main_window.setWindowTitle("Open Cell Lab")


main_window.show()
sys.exit(app.exec())