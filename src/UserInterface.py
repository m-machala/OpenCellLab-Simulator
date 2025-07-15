from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QTextEdit, QToolBar,
    QMainWindow, QCheckBox, QScrollArea, QRadioButton, 
    QButtonGroup, QSlider, QSpinBox, QSizePolicy,
    QListWidgetItem
)
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt6.QtGui import QAction, QActionGroup, QIcon, QPixmap, QImage, QMouseEvent
import ModuleFinder
import os
import sys
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
        self.selectedCells = []

        # introduction
        self.welcomeLabel = QLabel("Welcome to OCL!")
        mainLayout.addWidget(self.welcomeLabel)

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
        path = os.path.join(getFilePath(), "packages")
        #self.welcomeLabel.setText(path)
        packages = ModuleFinder.findPackageJSONs(path)
        self.moduleListItems = []
        self.moduleList.clear()

        renderers = ModuleFinder.filterJSONsByType(packages, "renderer")
        environments = ModuleFinder.filterJSONsByType(packages, "environment")

        for renderer in renderers:
            if "package image path" in renderer and os.path.exists(renderer["package image path"]):
                imagePath = renderer["package image path"]
            else:
                imagePath = os.path.join(getFilePath(), "icons", "missing.png")
                
            item = QListWidgetItem(QIcon(imagePath), renderer["package name"])
            self.moduleList.addItem(item)
            self.moduleListItems.append(renderer)
            rendererClass = renderer["package class"]

            for environment in environments:
                if rendererClass == environment["renderer class"]:
                    if "package image path" in environment and os.path.exists(environment["package image path"]):
                        imagePath = environment["package image path"]
                    else:
                        imagePath = os.path.join(getFilePath(), "icons", "missing.png")
                    
                    item = QListWidgetItem(QIcon(imagePath), "   " + environment["package name"])
                    self.moduleList.addItem(item)
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
            self.selectedCells = []

            self.beginButton.setDisabled(True)
            self.cellList.clear()


    def populateCellPackList(self, selectedModule):
        if selectedModule["package type"] != "environment":
            return
        self.cellList.clear()
        self.selectedCells = []

        modules = ModuleFinder.findPackageJSONs(os.path.join(getFilePath(), "packages"))
        cellPacks = ModuleFinder.filterJSONsByType(modules, "cell")

        for cellPack in cellPacks:
            if cellPack["environment class"] == selectedModule["package class"]:
                self.cellList.addItem(cellPack["package name"])
                self.selectedCells.append(cellPack)


    def cellPackSelectionChanged(self, item):
        packIndex = self.cellList.row(item)
        
        if packIndex == -1:
            return

        module = self.selectedCells[packIndex]
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

        # timers

        self.simulationTimer = QTimer()
        self.simulationTimer.setInterval(250)
        self.simulationTimer.timeout.connect(self.simulationTimerTriggered)
        self.simulationTimer.stop()

        # toolbar

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        playAction = QAction(QIcon(), "Play", self)
        toolbar.addAction(playAction)
        playAction.triggered.connect(self.simulationTimer.start)

        pauseAction = QAction(QIcon(), "Pause", self)
        toolbar.addAction(pauseAction)
        pauseAction.triggered.connect(self.simulationTimer.stop)
        pauseAction.triggered.connect(self.updateSimulationView)

        self.stepAction = QAction(QIcon(), "Step", self)
        toolbar.addAction(self.stepAction)
        self.stepAction.triggered.connect(self.stepClicked)

        self.clearAction = QAction(QIcon(), "Clear", self)
        toolbar.addAction(self.clearAction)
        self.clearAction.triggered.connect(self.clearClicked)

        toolbar.addSeparator()

        mouseModeGroup = QActionGroup(self)
        mouseModeGroup.setExclusive(True)

        self.clickModeAction = QAction(QIcon(), "Click", self)
        self.clickModeAction.setCheckable(True)
        self.clickModeAction.setChecked(True)
        mouseModeGroup.addAction(self.clickModeAction)
        toolbar.addAction(self.clickModeAction)

        self.dragModeAction = QAction(QIcon(), "Drag", self)
        self.dragModeAction.setCheckable(True)
        mouseModeGroup.addAction(self.dragModeAction)
        toolbar.addAction(self.dragModeAction)

        toolbar.addSeparator()

        interactionModeGroup = QActionGroup(self)
        interactionModeGroup.setExclusive(True)

        self.environmentModeAction = QAction(QIcon(), "Environment", self)
        self.environmentModeAction.setCheckable(True)
        self.environmentModeAction.setChecked(True)
        interactionModeGroup.addAction(self.environmentModeAction)
        toolbar.addAction(self.environmentModeAction)

        self.rendererModeAction = QAction(QIcon(), "Renderer", self)
        self.rendererModeAction.setCheckable(True)
        interactionModeGroup.addAction(self.rendererModeAction)
        toolbar.addAction(self.rendererModeAction)


        # simulation and cell selection        

        simucellLayout = QVBoxLayout()
        mainLayout.addLayout(simucellLayout, 2)

        # simulation

        simulationLabel = QLabel("Simulation")
        simucellLayout.addWidget(simulationLabel)

        self.simulationImageLabel = SimulationLabel()
        self.simulationImageLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.simulationImageLabel.setMinimumSize(1, 1)
        self.simulationImageLabel.leftClicked.connect(self.imageLeftClicked)
        self.simulationImageLabel.rightClicked.connect(self.imageRightClicked)
        self.simulationImageLabel.middleClicked.connect(self.imageMiddleClicked)
        self.simulationImageLabel.leftDragged.connect(self.imageLeftDragged)
        self.simulationImageLabel.rightDragged.connect(self.imageRightDragged)
        self.simulationImageLabel.middleDragged.connect(self.imageMiddleDragged)
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
        self.exportTimers = []
        # get references to main modules
        rendererReference = ModuleFinder.loadRenderer(rendererData)
        environmentReference = ModuleFinder.loadEnvironment(environmentData)

        if rendererReference == None or environmentReference == None:
            self.loadingFailed()
            return
        
        # instantiate main modules and connect them
        self.renderer = rendererReference(self.simulationImageLabel.width(), self.simulationImageLabel.height())
        self.environment = environmentReference(self.renderer)

        self.executor = CellExecutor(self.environment, [])

        self.environment._setExecutor(self.executor)

        if self.executor == None:
            self.loadingFailed()
            return

        # load cell list and save cell references
        self.cellListWidget.clear()
        self.cellList = []
        for pack in cellPackDataList:
            foundCells = ModuleFinder.loadCellPack(pack)
            if len(foundCells) == 0:
                continue

            self.cellList.append((None, pack))
            self.cellListWidget.addItem(pack["package name"])
            for cellIndex in range(len(foundCells)):
                self.cellListWidget.addItem("    " + foundCells[cellIndex][1]["cell name"])
                self.cellList.append(foundCells[cellIndex])

        # load export functions
        # TODO: proper export cleaning

        # renderer exports
        self.radioGroupsRenderer = {}
        for exportFunction in self.renderer._exportFunctions:
            element = self.buildExportElement(exportFunction, True)
            self.rendererExportsInnerLayout.addWidget(element)
        self.rendererExportsInnerLayout.addStretch(1)

        # environment exports
        self.radioGroupsEnvironment = {}
        for exportFunction in self.environment._exportFunctions:
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
    
    def simulationTimerTriggered(self):
        self.executor._cycleCells()
        self.updateSimulationView()

    def stepClicked(self):
        self.simulationTimer.stop()
        self.simulationTimerTriggered()

    def clearClicked(self):
        self.simulationTimer.stop()
        self.executor.clearCells()
        self.updateSimulationView()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.renderer._setOutputResolution(self.simulationImageLabel.width(), self.simulationImageLabel.height())
        self.updateSimulationView()

    def updateSimulationView(self):
        self.simulationImageLabel.setPixmap(QPixmap.fromImage(QImage.fromData(self.renderer.render(self.executor.cellList))))

    def determineReceiver(self):
        if self.environmentModeAction.isChecked():
            return self.environment
        elif self.rendererModeAction.isChecked():
            return self.renderer
        else:
            return None
        
    def processCoordinates(self, x, y):
        if self.environmentModeAction.isChecked():
            return self.renderer.convertFromImageCoordinates(x, y)
        elif self.rendererModeAction.isChecked():
            return (x, y)

    def imageLeftClicked(self, x, y):
        receiver = self.determineReceiver()
        processedCoordinates = self.processCoordinates(x, y)
        if not receiver or not processedCoordinates:
            return
        
        self.originalLeft = processedCoordinates
        if self.clickModeAction.isChecked():
            receiver._primaryClick(processedCoordinates)
        self.updateSimulationView()

    def imageRightClicked(self, x, y):
        receiver = self.determineReceiver()
        processedCoordinates = self.processCoordinates(x, y)
        if not receiver or not processedCoordinates:
            return
        
        self.originalRight = processedCoordinates
        if self.clickModeAction.isChecked():
            receiver._secondaryClick(processedCoordinates)
        self.updateSimulationView()

    def imageMiddleClicked(self, x, y):
        receiver = self.determineReceiver()
        processedCoordinates = self.processCoordinates(x, y)
        if not receiver or not processedCoordinates:
            return
        
        self.originalMiddle = processedCoordinates
        if self.clickModeAction.isChecked():
            receiver._tertiaryClick(processedCoordinates)
        self.updateSimulationView()


    def imageLeftDragged(self, x, y):
        if not self.dragModeAction.isChecked(): return
        receiver = self.determineReceiver()
        processedCoordinates = self.processCoordinates(x, y)
        if not receiver or not processedCoordinates:
            return
        
        receiver._primaryDrag(self.originalLeft, processedCoordinates)
        self.originalLeft = processedCoordinates
        self.updateSimulationView()

    def imageRightDragged(self, x, y):
        if not self.dragModeAction.isChecked(): return
        receiver = self.determineReceiver()
        processedCoordinates = self.processCoordinates(x, y)
        if not receiver or not processedCoordinates:
            return
        
        receiver._secondaryDrag(self.originalRight, processedCoordinates)
        self.originalRight = processedCoordinates
        self.updateSimulationView()

    def imageMiddleDragged(self, x, y):
        if not self.dragModeAction.isChecked(): return
        receiver = self.determineReceiver()
        processedCoordinates = self.processCoordinates(x, y)
        if not receiver or not processedCoordinates:
            return
        
        receiver._tertiaryDrag(self.originalMiddle, processedCoordinates)
        self.originalMiddle = processedCoordinates
        self.updateSimulationView()
        

    def showEvent(self, event):
        super().showEvent(event)
        self.renderer._setOutputResolution(self.simulationImageLabel.width(), self.simulationImageLabel.height())
        self.updateSimulationView()


class SimulationLabel(QLabel):
    leftClicked = pyqtSignal(int, int)
    rightClicked = pyqtSignal(int, int)
    middleClicked = pyqtSignal(int, int)

    leftDragged = pyqtSignal(int, int)
    rightDragged = pyqtSignal(int, int)
    middleDragged = pyqtSignal(int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.leftDragging = False
        self.rightDragging = False
        self.middleDragging = False

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
        x = int(event.position().x())
        y = int(event.position().y())
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftDragging = True
            self.leftClicked.emit(x, y)
            self.leftDragged.emit(x, y)

        if event.button() == Qt.MouseButton.RightButton:
            self.rightDragging = True
            self.rightClicked.emit(x, y)
            self.rightDragged.emit(x, y)

        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleDragging = True
            self.middleClicked.emit(x, y)
            self.middleDragged.emit(x, y)

    def mouseMoveEvent(self, event: QMouseEvent):
        x = int(event.position().x())
        y = int(event.position().y())
        if self.leftDragging:
            self.leftDragged.emit(x, y)

        if self.rightDragging:
            self.rightDragged.emit(x, y)

        if self.middleDragging:
            self.middleDragged.emit(x, y)

    def mouseReleaseEvent(self, event:QMouseEvent):
        if self.leftDragging and event.button() == Qt.MouseButton.LeftButton:
            self.leftDragging = False

        if self.rightDragged and event.button() == Qt.MouseButton.RightButton:
            self.rightDragging = False

        if self.middleDragging and event.button() == Qt.MouseButton.MiddleButton:
            self.middleDragging = False

def getFilePath():
    if getattr(sys, "frozen", False):
        path = os.path.dirname(sys.executable)
    else:
        path = os.path.dirname(os.path.abspath(__file__))

    return path
