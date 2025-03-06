from UserInterface import WelcomeScreen, MainScreen
from PyQt6.QtWidgets import QApplication
import sys
import ModuleFinder

modules = ModuleFinder.findPackageJSONs(".\\packages")
renderer = ModuleFinder.filterJSONsByType(modules, "renderer")[0]
environment = ModuleFinder.filterJSONsByType(modules, "environment")[0]
cells = ModuleFinder.filterJSONsByType(modules, "cell")


app = QApplication(sys.argv)
main_window = MainScreen(renderer, environment, cells)

main_window.setWindowTitle("Open Cell Lab")
main_window.show()
sys.exit(app.exec())