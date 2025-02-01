from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QTextEdit

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout()

        # introduction
        welcomeLabel = QLabel("Welcome to OCL!")
        mainLayout.addWidget(welcomeLabel)

        infoLabel = QLabel("To begin, please select an environment from the list below.")
        mainLayout.addWidget(infoLabel)

        selectionLayout = QHBoxLayout()
        mainLayout.addLayout(selectionLayout)

        # list of modules
        moduleListLayout = QVBoxLayout()
        selectionLayout.addLayout(moduleListLayout)

        moduleLabel = QLabel("Available modules:")
        moduleListLayout.addWidget(moduleLabel)

        self.moduleList = QListWidget()
        moduleListLayout.addWidget(self.moduleList)

        # list of cell packs
        moduleInfoLayout = QVBoxLayout()
        selectionLayout.addLayout(moduleInfoLayout)

        cellLabel = QLabel("Available cell packs:")
        moduleInfoLayout.addWidget(cellLabel)

        self.cellList = QListWidget()
        moduleInfoLayout.addWidget(self.cellList)

        # info about modules
        moduleLabel = QLabel("Selected module info:")
        moduleInfoLayout.addWidget(moduleLabel)

        self.moduleInfo = QTextEdit()
        self.moduleInfo.setReadOnly(True)
        moduleInfoLayout.addWidget(self.moduleInfo)

        # controls
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

    def populateModuleList(self):
        pass

    def moduleClicked(self):
        pass

    def populateCellPackList(self):
        pass

    def cellPackClicked(self):
        pass

    def setModuleInfoText(self, text):
        pass

    def reloadClicked(self):
        pass

    def beginClicked(self):
        pass

    def exitClicked(self):
        pass
