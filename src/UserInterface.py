from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QTextEdit, QToolBar,
    QMainWindow, QCheckBox, QScrollArea, QRadioButton, 
    QButtonGroup, QSlider, QSpinBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QPixmap, QImage, QMouseEvent, QResizeEvent
import ModuleFinder
import os
from CellExecutor import CellExecutor
from ExportFunctions import ExportFunction, ControlElement
from base_classes.Cell import Cell

class WelcomeScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)

        self.selectedEnvironment = None
        self.selectedRenderer = None
        self.selectedCells = None

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
            self.selectedEnvironment = module
            for packIndex in range(moduleIndex, -1, -1):
                if self.moduleListItems[packIndex]["package type"] == "renderer":
                    self.selectedRenderer = self.moduleListItems[packIndex]
                    break

            self.beginButton.setEnabled(True)
            self.populateCellPackList(module)
        else:
            self.selectedEnvironment = None
            self.selectedRenderer = None
            self.selectedCells = None

            self.beginButton.setDisabled(True)
            self.cellList.clear()


    def populateCellPackList(self, selectedModule):
        self.cellList.clear()
        self.cellListItems = []
        if selectedModule["package type"] != "environment":
            return
        
        modules = ModuleFinder.findPackageJSONs(os.path.dirname(os.path.abspath(__file__)) + "\\packages")
        cellPacks = ModuleFinder.filterJSONsByType(modules, "cell")
        self.selectedCells = cellPacks

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
        mainScreen = MainScreen(self.selectedRenderer, self.selectedEnvironment, self.selectedCells)
        self.setCentralWidget(mainScreen)
        self.resize(1000, 750)

    def exitClicked(self):
        self.close()  

class MainScreen(QMainWindow):
    def __init__(self, rendererData, environmentData, cellPackDataList):
        super().__init__()
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = QHBoxLayout(centralWidget)

        # timer

        self.timer = QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.timerTriggered)
        self.timer.stop()

        # toolbar

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        playAction = QAction(QIcon(), "Play", self)
        toolbar.addAction(playAction)
        playAction.triggered.connect(self.timer.start)

        pauseAction = QAction(QIcon(), "Pause", self)
        toolbar.addAction(pauseAction)
        pauseAction.triggered.connect(self.timer.stop)
        pauseAction.triggered.connect(self.updateSimulationView)

        self.stepAction = QAction(QIcon(), "Step", self)
        toolbar.addAction(self.stepAction)
        self.stepAction.triggered.connect(self.timer.stop)
        self.stepAction.triggered.connect(self.stepClicked)

        # simulation and cell selection        

        simucellLayout = QVBoxLayout()
        mainLayout.addLayout(simucellLayout, 2)

        # simulation

        simulationLabel = QLabel("Simulation")
        simucellLayout.addWidget(simulationLabel)

        self.simulationImageLabel = PixelPerfectLabel()
        self.simulationImageLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.simulationImageLabel.setMinimumSize(1, 1)
        self.simulationImageLabel.leftClicked.connect(self.imageLeftClicked)
        self.simulationImageLabel.rightClicked.connect(self.imageRightClicked)
        self.simulationImageLabel.middleClicked.connect(self.imageMiddleClicked)
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

        self.radioGroupsRenderer = {}
        self.radioGroupsEnvironment = {}
        self.reload(rendererData, environmentData, cellPackDataList)

    def reload(self, rendererData, environmentData, cellPackDataList):
        self.exportTimers = []
        # get references to main modules
        rendererReference = ModuleFinder.loadRenderer(rendererData)
        environmentReference = ModuleFinder.loadEnvironment(environmentData)

        if rendererReference == None or environmentReference == None:
            self.loadingFailed()
            return
        
        # instantiate main modules and connect them
        self.renderer = rendererReference(self.simulationImageLabel.width(), self.simulationImageLabel.height())
        self.environment = environmentReference()

        self.executor = CellExecutor(self.environment, [])

        self.environment.setExecutor(self.executor)

        if self.executor == None:
            self.loadingFailed()
            return

        # load cell list and save cell references
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

        # load export functions
        # TODO: proper export cleaning

        # renderer exports
        self.radioGroupsRenderer = {}
        for exportFunction in self.renderer.exportFunctions:
            element = self.buildExportElement(exportFunction, True)
            self.rendererExportsInnerLayout.addWidget(element)
        self.rendererExportsInnerLayout.addStretch(1)

        # environment exports
        self.radioGroupsEnvironment = {}
        for exportFunction in self.environment.exportFunctions:
            element = self.buildExportElement(exportFunction, False)
            self.environmentExportsInnerLayout.addWidget(element)
        self.environmentExportsInnerLayout.addStretch(1)
        
    def loadingFailed(self):
        print("Loading error")

    def cellListSelectionChanged(self, item):
        cellIndex = self.cellListWidget.row(item)
        module = self.cellList[cellIndex]

        if "package description" in module[1]:
            self.cellInfo.setText(module[1]["package description"])

        if "cell description" in module[1]:
            self.cellInfo.setText(module[1]["cell description"])

        if "package type" in module[1]:
            self.executor.selectCellBrainReference(None)
        else:
            self.executor.selectCellBrainReference(module[0])

    def buildExportElement(self, exportFunction, isRenderer):
        if isinstance(exportFunction, str):
            label = QLabel(exportFunction)
            return label
        
        controlElement = exportFunction.controlElement
        outputElement = None
        if controlElement == ControlElement.BUTTON:
            outputElement = QPushButton(exportFunction.name)
            outputElement.clicked.connect(exportFunction.functionReference)

        elif controlElement == ControlElement.REPEATINGBUTTON:
            outputElement = QPushButton(exportFunction.name)

            timer = QTimer()
            timer.setInterval(exportFunction.additionalArguments[0])
            timer.timeout.connect(exportFunction.functionReference)
            
            outputElement.pressed.connect(timer.start)
            outputElement.released.connect(timer.stop)

            self.exportTimers.append(timer)

        elif controlElement == ControlElement.RADIOBUTTON:
            if isRenderer:
                radioGroups = self.radioGroupsRenderer
            else:
                radioGroups = self.radioGroupsEnvironment

            outputElement = QRadioButton(exportFunction.name)

            if exportFunction.additionalArguments[0] in radioGroups:
                radioGroups[exportFunction.additionalArguments[0]].addButton(outputElement)
            else:
                newGroup = QButtonGroup()
                radioGroups[exportFunction.additionalArguments[0]] = newGroup
                newGroup.addButton(outputElement)
                outputElement.setChecked(True)
            outputElement.clicked.connect(exportFunction.functionReference)
                
        elif controlElement == ControlElement.CHECKBOX:
            outputElement = QCheckBox(exportFunction.name)
            outputElement.clicked.connect(exportFunction.functionReference)

        elif controlElement == ControlElement.SLIDER:
            outputElement = QWidget()
            
            outputLayout = QVBoxLayout()
            outputElement.setLayout(outputLayout)

            label = QLabel(exportFunction.name)
            outputLayout.addWidget(label)
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setMinimum(exportFunction.additionalArguments[0])
            slider.setMaximum(exportFunction.additionalArguments[1])
            slider.setValue(exportFunction.additionalArguments[2])
            slider.valueChanged.connect(exportFunction.functionReference)
            outputLayout.addWidget(slider)

            if isRenderer:
                slider.valueChanged.connect(self.updateSimulationView)
            
        elif controlElement == ControlElement.SPINBOX:
            outputElement = QWidget()
            
            outputLayout = QVBoxLayout()
            outputElement.setLayout(outputLayout)

            label = QLabel(exportFunction.name)
            outputLayout.addWidget(label)
            spinbox = QSpinBox()
            spinbox.setMinimum(exportFunction.additionalArguments[0])
            spinbox.setMaximum(exportFunction.additionalArguments[1])
            spinbox.setValue(exportFunction.additionalArguments[2])
            spinbox.valueChanged.connect(exportFunction.functionReference)
            outputLayout.addWidget(spinbox)

            if isRenderer:
                spinbox.valueChanged.connect(self.updateSimulationView)

        if isRenderer and outputElement != None:
            if not (controlElement == ControlElement.SLIDER or controlElement == ControlElement.SPINBOX):
                if controlElement == ControlElement.REPEATINGBUTTON:
                    self.exportTimers[-1].timeout.connect(self.updateSimulationView)
                else:
                    outputElement.clicked.connect(self.updateSimulationView) # type: ignore

        return outputElement
    
    def timerTriggered(self):
        self.executor.cycleCells()
        self.updateSimulationView()

    def stepClicked(self):
        self.timerTriggered()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.renderer.setOutputResolution(self.simulationImageLabel.width(), self.simulationImageLabel.height())
        self.updateSimulationView()

    def updateSimulationView(self):
        self.simulationImageLabel.setPixmap(QPixmap.fromImage(QImage.fromData(self.renderer.render(self.executor.cellList))))

    def imageLeftClicked(self, x, y):
        self.environment.primaryInteraction(self.renderer.convertFromImageCoordinates(x, y))
        self.updateSimulationView()

    def imageRightClicked(self, x, y):
        self.environment.secondaryInteraction(self.renderer.convertFromImageCoordinates(x, y))
        self.updateSimulationView()

    def imageMiddleClicked(self, x, y):
        self.environment.tertiaryInteraction(self.renderer.convertFromImageCoordinates(x, y))
        self.updateSimulationView()

    def showEvent(self, event):
        super().showEvent(event)
        self.renderer.setOutputResolution(self.simulationImageLabel.width(), self.simulationImageLabel.height())
        self.updateSimulationView()


class PixelPerfectLabel(QLabel):
    leftClicked = pyqtSignal(int, int)
    rightClicked = pyqtSignal(int, int)
    middleClicked = pyqtSignal(int, int)
    def sizeHint(self):
        if self.width() > 0:
            width = self.width()
        else:
            width = 100

        if self.height() > 0:
            height = self.height()
        else:
            height = 100

        return QSize(width, height)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            x = event.position().x()
            y = event.position().y()
            self.leftClicked.emit(int(x), int(y))

        if event.button() == Qt.MouseButton.RightButton:
            x = event.position().x()
            y = event.position().y()
            self.rightClicked.emit(int(x), int(y))

        if event.button() == Qt.MouseButton.MiddleButton:
            x = event.position().x()
            y = event.position().y()
            self.middleClicked.emit(int(x), int(y))
