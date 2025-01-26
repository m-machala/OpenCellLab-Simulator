from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QTextEdit

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout()

        welcomeLabel = QLabel("Welcome to OCL!")
        mainLayout.addWidget(welcomeLabel)

        infoLabel = QLabel("To begin, please select an environment from the list below.")
        mainLayout.addWidget(infoLabel)

        selectionLayout = QHBoxLayout()
        mainLayout.addLayout(selectionLayout)


        moduleListLayout = QVBoxLayout()
        selectionLayout.addLayout(moduleListLayout)

        moduleLabel = QLabel("Available modules:")
        moduleListLayout.addWidget(moduleLabel)

        moduleList = QListWidget()
        moduleListLayout.addWidget(moduleList)


        moduleInfoLayout = QVBoxLayout()
        selectionLayout.addLayout(moduleInfoLayout)

        cellLabel = QLabel("Available cell packs:")
        moduleInfoLayout.addWidget(cellLabel)

        cellList = QListWidget()
        moduleInfoLayout.addWidget(cellList)

        moduleLabel = QLabel("Selected module info:")
        moduleInfoLayout.addWidget(moduleLabel)

        moduleInfo = QTextEdit()
        moduleInfo.setReadOnly(True)
        moduleInfoLayout.addWidget(moduleInfo)


        reloadButton = QPushButton("Reload")
        mainLayout.addWidget(reloadButton)


        buttonLayout = QHBoxLayout()
        mainLayout.addLayout(buttonLayout)

        exitButton = QPushButton("Exit")
        buttonLayout.addWidget(exitButton)

        buttonLayout.addStretch()

        beginButton = QPushButton("Begin")
        buttonLayout.addWidget(beginButton)

        self.setLayout(mainLayout)
