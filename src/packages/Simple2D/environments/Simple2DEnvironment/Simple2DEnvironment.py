from base_classes.Environment import Environment
from base_classes.Cell import Cell
from ExportFunctions import ExportFunction, ControlElement

class Simple2DEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self._stepCount = 0
        self._cellMap = {}

    def _updateCellMap(self, x, y, cell = None):
        if cell == None:
            self._cellMap.pop((x, y), None)
        else:
            self._cellMap[(x, y)] = cell
        
    def cellsCycled(self):
        self._stepCount += 1

    def primaryClick(self, data):
        self.addUserCell(data)

    def primaryDrag(self, originalData, newData):
        self.addUserCell(newData)

    def executorClearedCells(self):
        self._cellMap = {}
        for cell in self._cellExecutor.cellList:
            self._cellMap[(cell.cellData["xPosition"], cell.cellData["yPosition"])] = cell

    def addUserCell(self, data):
        xCoordinate = data[0]
        yCoordinate = data[1]

        cellBrainReference = self._cellExecutor.selectedCellBrainReference
        if cellBrainReference == None:
            return
        
        newCellBrain = cellBrainReference(self)

        self._spawnCell(xCoordinate, yCoordinate, newCellBrain)

    
    def secondaryClick(self, data):
        self.userRemoveCell(data)

    def secondaryDrag(self, originalData, newData):
        self.userRemoveCell(newData)        
            
    def userRemoveCell(self, data):
        xCoordinate = data[0]
        yCoordinate = data[1]

        if (xCoordinate, yCoordinate) in self._cellMap:
            self._cellExecutor.removeCell(self._cellMap[(xCoordinate, yCoordinate)])
            
        self._updateCellMap(xCoordinate, yCoordinate)
    
    def _checkForCellAbsolute(self, xCoordinate, yCoordinate):
        if (xCoordinate, yCoordinate) in self._cellMap:
            return True
        return False

    def checkForCell(self, relativeXCoordinate, relativeYcoordinate):
        currentCell = self._cellExecutor.currentCell
        if currentCell == None:
            return True
        
        currentCellX = currentCell.cellData["xPosition"]
        currentCellY = currentCell.cellData["yPosition"]

        checkedCellX = currentCellX + relativeXCoordinate
        checkedCellY = currentCellY + relativeYcoordinate

        return self._checkForCellAbsolute(checkedCellX, checkedCellY)
    
    def checkIfCellTypeEqual(self, relativeXCoordinate, relativeYcoordinate, cellType):
        currentCell = self._cellExecutor.currentCell
        if currentCell == None:
            return True
        
        currentCellX = currentCell.cellData["xPosition"]
        currentCellY = currentCell.cellData["yPosition"]

        checkedCellX = currentCellX + relativeXCoordinate
        checkedCellY = currentCellY + relativeYcoordinate

        if (checkedCellX, checkedCellY) in self._cellMap:
            return isinstance(self._cellMap[(checkedCellX, checkedCellY)].cellBrain, cellType)

        return False

    def _spawnCell(self, xCoordinate, yCoordinate, newCellBrain):
        if self._checkForCellAbsolute(xCoordinate, yCoordinate):
            return

        newCell = Cell(newCellBrain)
        newCell.cellData["xPosition"] = xCoordinate
        newCell.cellData["yPosition"] = yCoordinate
        if hasattr(type(newCellBrain), "COLOR"):
            newCell.cellData["color"] = type(newCellBrain).COLOR
        else:
            newCell.cellData["color"] = (255, 255, 255)
        
        self._cellExecutor.addCell(newCell)

        self._updateCellMap(xCoordinate, yCoordinate, newCell)

    def spawnCell(self, relativeXCoordinate, relativeYCoordinate, newCellBrain):
        if self.checkForCell(relativeXCoordinate, relativeYCoordinate):
            return
        
        currentCell = self._cellExecutor.currentCell

        self._spawnCell(currentCell.cellData["xPosition"] + relativeXCoordinate, currentCell.cellData["yPosition"] + relativeYCoordinate, newCellBrain)

    def deleteCurrentCell(self):
        currentCell = self._cellExecutor.currentCell
        if currentCell == None:
            return
        
        currentCellX = currentCell.cellData["xPosition"]
        currentCellY = currentCell.cellData["yPosition"]

        self._updateCellMap(currentCellX, currentCellY)
        self._cellExecutor.removeCell(currentCell)

    def deleteCurrentSpawnNewCell(self, newCellBrain):
        currentCell = self._cellExecutor.currentCell
        xPosition = currentCell.cellData["xPosition"]
        yPosition = currentCell.cellData["yPosition"]

        self.deleteCurrentCell()

        self._spawnCell(xPosition, yPosition, newCellBrain)
        
    def getCurrentStepNumber(self):
        return self._stepCount