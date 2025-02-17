from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QTextEdit, QToolBar,
    QMainWindow, QGridLayout, QScrollArea, QGroupBox
)
import ModuleFinder
import os
from CellExecutor import CellExecutor

class WelcomeScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)

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
        self.moduleList.currentItemChanged.connect(self.moduleSelectionChanged)
        moduleListLayout.addWidget(self.moduleList)

        # list of cell packs
        moduleInfoLayout = QVBoxLayout()
        selectionLayout.addLayout(moduleInfoLayout)

        cellLabel = QLabel("Available cell packs:")
        moduleInfoLayout.addWidget(cellLabel)

        self.cellList = QListWidget()
        self.cellList.currentItemChanged.connect(self.cellPackSelectionChanged)
        moduleInfoLayout.addWidget(self.cellList)

        # info about modules
        moduleLabel = QLabel("Selected module info:")
        moduleInfoLayout.addWidget(moduleLabel)

        self.moduleInfo = QTextEdit()
        self.moduleInfo.setReadOnly(True)
        moduleInfoLayout.addWidget(self.moduleInfo)

        # controls
        reloadButton = QPushButton("Reload")
        reloadButton.clicked.connect(self.reloadClicked)
        mainLayout.addWidget(reloadButton)

        buttonLayout = QHBoxLayout()
        mainLayout.addLayout(buttonLayout)

        exitButton = QPushButton("Exit")
        exitButton.clicked.connect(self.exitClicked)
        buttonLayout.addWidget(exitButton)

        buttonLayout.addStretch()

        self.beginButton = QPushButton("Begin")
        self.beginButton.setDisabled(True)
        self.beginButton.clicked.connect(self.beginClicked)
        buttonLayout.addWidget(self.beginButton)

        self.reloadClicked()

    def populateModuleList(self):
        packages = ModuleFinder.findPackageJSONs(os.path.dirname(os.path.abspath(__file__)) + "\\packages")
        self.moduleListItems = []
        self.moduleList.clear()

        renderers = ModuleFinder.filterJSONsByType(packages, "renderer")
        environments = ModuleFinder.filterJSONsByType(packages, "environment")

        for renderer in renderers:
            self.moduleList.addItem(renderer["package name"])
            self.moduleListItems.append(renderer)
            rendererClass = renderer["package class"]

            for environment in environments:
                if rendererClass == environment["renderer class"]:
                    self.moduleList.addItem("   " + environment["package name"])
                    self.moduleListItems.append(environment)

    def moduleSelectionChanged(self, item):
        self.unselectCellPack()
        moduleIndex = self.moduleList.row(item)
        module = self.moduleListItems[moduleIndex]
        if "package description" in module:
            self.setModuleInfoText(module["package description"])
        else:
            self.setModuleInfoText("")

        if module["package type"] == "environment":
            self.beginButton.setEnabled(True)
            self.populateCellPackList(module)
        else:
            self.beginButton.setDisabled(True)
            self.cellList.clear()


    def populateCellPackList(self, selectedModule):
        self.cellList.clear()
        self.cellListItems = []
        if selectedModule["package type"] != "environment":
            return
        
        modules = ModuleFinder.findPackageJSONs(os.path.dirname(os.path.abspath(__file__)) + "\\packages")
        cellPacks = ModuleFinder.filterJSONsByType(modules, "cell")

        for cellPack in cellPacks:
            if cellPack["environment class"] == selectedModule["package class"]:
                self.cellList.addItem(cellPack["package name"])
                self.cellListItems.append(cellPack)


    def cellPackSelectionChanged(self, item):
        packIndex = self.cellList.row(item)

        module = self.cellListItems[packIndex]
        if "package description" in module:
            self.setModuleInfoText(module["package description"])
        else:
            self.setModuleInfoText("")

    def setModuleInfoText(self, text):
        self.moduleInfo.setText(text)

    def reloadClicked(self):
        self.moduleList.clear()
        self.cellList.clear()
        self.unselectModule()
        self.unselectCellPack()
        self.setModuleInfoText("")
        self.populateModuleList()
        self.beginButton.setDisabled(True)

    def unselectModule(self):
        self.moduleList.clearSelection()

    def unselectCellPack(self):
        self.cellList.clearSelection()

    def beginClicked(self):
        pass

    def exitClicked(self):
        self.close()  

class MainScreen(QMainWindow):
    def __init__(self, rendererData, environmentData, cellPackDataList):
        super().__init__()
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = QHBoxLayout(centralWidget)

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        simucellLayout = QVBoxLayout()
        mainLayout.addLayout(simucellLayout, 2)

        # simulation

        simulationLabel = QLabel("Simulation")
        simucellLayout.addWidget(simulationLabel)

        self.simulationImageLabel = QLabel()
        simucellLayout.addWidget(self.simulationImageLabel, 3)

        # cells

        cellLayout = QHBoxLayout()
        simucellLayout.addLayout(cellLayout, 2)

        cellListOuterLayout = QVBoxLayout()
        cellLayout.addLayout(cellListOuterLayout, 2)

        cellLabel = QLabel("Cells")
        cellListOuterLayout.addWidget(cellLabel)

        self.cellListWidget = QListWidget()
        self.cellListWidget.currentItemChanged.connect(self.cellListSelectionChanged)
        cellListOuterLayout.addWidget(self.cellListWidget)

        cellInfoLayout = QVBoxLayout()
        cellLayout.addLayout(cellInfoLayout, 1)

        self.cellInfoLabel = QLabel("Cell info")
        cellInfoLayout.addWidget(self.cellInfoLabel)

        self.cellInfo = QTextEdit()
        self.cellInfo.setReadOnly(True)
        cellInfoLayout.addWidget(self.cellInfo)


        # export functions

        exportLayout = QHBoxLayout()
        mainLayout.addLayout(exportLayout, 1)

        # environment exports

        environmentExportsOuterLayout = QVBoxLayout()
        exportLayout.addLayout(environmentExportsOuterLayout, 1)

        environmentExportsLabel = QLabel("Environment Settings")
        environmentExportsOuterLayout.addWidget(environmentExportsLabel)

        environmentExports = QScrollArea()
        environmentExports.setWidgetResizable(True)
        environmentExportsContainer = QWidget()
        environmentExports.setWidget(environmentExportsContainer)

        self.environmentExportsInnerLayout = QVBoxLayout()
        environmentExportsContainer.setLayout(self.environmentExportsInnerLayout)

        environmentExportsOuterLayout.addWidget(environmentExports)

        # renderer exports

        rendererExportsOuterLayout = QVBoxLayout()
        exportLayout.addLayout(rendererExportsOuterLayout, 1)

        rendererExportsLabel = QLabel("Renderer Settings")
        rendererExportsOuterLayout.addWidget(rendererExportsLabel)

        rendererExports = QScrollArea()
        rendererExports.setWidgetResizable(True)
        rendererExportsContainer = QWidget()
        rendererExports.setWidget(rendererExportsContainer)

        self.rendererExportsInnerLayout = QVBoxLayout()
        rendererExportsContainer.setLayout(self.rendererExportsInnerLayout)

        rendererExportsOuterLayout.addWidget(rendererExports)

        self.reload(rendererData, environmentData, cellPackDataList)

    def reload(self, rendererData, environmentData, cellPackDataList):
        rendererReference = ModuleFinder.loadRenderer(rendererData)
        environmentReference = ModuleFinder.loadEnvironment(environmentData)

        if rendererReference == None or environmentReference == None:
            self.loadingFailed()
            return
        self.renderer = rendererReference(self.simulationImageLabel.width(), self.simulationImageLabel.height())
        self.environment = environmentReference()

        self.executor = CellExecutor(self.environment, [])
        self.environment.setExecutor(self.executor)

        if self.executor == None:
            self.loadingFailed()
            return

        self.cellListWidget.clear()
        self.cellList = []
        for pack in cellPackDataList:
            self.cellList.append((None, pack))
            foundCells = ModuleFinder.loadCellPack(pack)
            if len(foundCells) == 0:
                continue

            self.cellListWidget.addItem(pack["package name"])
            for cellIndex in range(len(foundCells)):
                self.cellListWidget.addItem("    " + foundCells[cellIndex][1]["cell name"])
                self.cellList.append(foundCells[cellIndex])
        
    def loadingFailed(self):
        print("Loading error")

    def cellListSelectionChanged(self, item):
        cellIndex = self.cellListWidget.row(item)
        module = self.cellList[cellIndex]

        if "package description" in module[1]:
            self.cellInfo.setText(module[1]["package description"])

        if "cell description" in module[1]:
            self.cellInfo.setText(module[1]["cell description"])




        