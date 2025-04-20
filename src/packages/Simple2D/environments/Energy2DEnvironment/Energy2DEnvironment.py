from base_classes.Environment import Environment
from base_classes.Cell import Cell
import math

class Energy2DEnvironment(Environment):
    def __init__(self, renderer):
        super().__init__(renderer)
        self._stepCount = 0
        self._cellMap = {}
        
    def _getEnvironmentEnergyLevel(self):
        return math.cos((self._stepCount) * math.pi / 30) / -10

    def _updateCellMap(self, x, y, cell = None):
        if cell == None:
            self._cellMap.pop((x, y), None)
        else:
            self._cellMap[(x, y)] = cell
        
    def _cellsCycled(self):
        self._stepCount += 1
        colorLevel = int((self._getEnvironmentEnergyLevel() + 0.1) * 5 * 127)
        self._renderer.setBackgroundColor((colorLevel, colorLevel, 0))

    def _cellSwitched(self):
        currentCell = self._cellExecutor.currentCell
        currentCell["energy"] += self._getEnvironmentEnergyLevel()
        if 0 >= currentCell["energy"] or 1 < currentCell["energy"]:
            self.deleteCurrentCell()
        self._cellActed = False


    def _primaryClick(self, data):
        self.addUserCell(data)

    def _primaryDrag(self, originalData, newData):
        self.addUserCell(newData)

    def _executorClearedCells(self):
        self._cellMap = {}

    def addUserCell(self, data):
        xCoordinate = data[0]
        yCoordinate = data[1]

        cellBrainReference = self._cellExecutor.selectedCellBrainReference
        if cellBrainReference == None:
            return
        
        newCellBrain = cellBrainReference(self)

        self._spawnCell(xCoordinate, yCoordinate, newCellBrain)

    
    def _secondaryClick(self, data):
        self.userRemoveCell(data)

    def _secondaryDrag(self, originalData, newData):
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
        cellCheckBaseCost = 0.025
        cellCheckCost = cellCheckBaseCost * (relativeXCoordinate // 1 + relativeYcoordinate // 1)

        currentCell = self._cellExecutor.currentCell
        if currentCell == None:
            return True
        if currentCell["energy"] < cellCheckCost:
            return True
        currentCell["energy"] -= cellCheckCost
        
        currentCellX = currentCell.cellData["xPosition"]
        currentCellY = currentCell.cellData["yPosition"]

        checkedCellX = currentCellX + relativeXCoordinate
        checkedCellY = currentCellY + relativeYcoordinate

        return self._checkForCellAbsolute(checkedCellX, checkedCellY)
    
    def checkIfCellTypeEqual(self, relativeXCoordinate, relativeYcoordinate, cellType):
        cellCheckBaseCost = 0.025
        cellCheckCost = cellCheckBaseCost * (relativeXCoordinate // 1 + relativeYcoordinate // 1)
        
        currentCell = self._cellExecutor.currentCell
        if currentCell == None:
            return True
        if currentCell["energy"] < cellCheckCost:
            return True
        currentCell["energy"] -= cellCheckCost
        
        currentCellX = currentCell.cellData["xPosition"]
        currentCellY = currentCell.cellData["yPosition"]

        checkedCellX = currentCellX + relativeXCoordinate // 1
        checkedCellY = currentCellY + relativeYcoordinate // 1

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
        newCell.cellData["energy"] = 0.5
        
        self._cellExecutor.addCell(newCell)

        self._updateCellMap(xCoordinate, yCoordinate, newCell)

    def spawnCell(self, xDirection, yDirection, newCellBrain):
        spawnCost = 0.5
        if self._cellActed or self.getEnergyLevel() < spawnCost:
            return

        currentCell = self._cellExecutor.currentCell
        oldXPosition = currentCell["xPosition"]
        oldYPosition = currentCell["yPosition"]
        xDirection, yDirection = self._determineDirection(xDirection, yDirection)
        newXPosition = oldXPosition + xDirection
        newYPosition = oldYPosition + yDirection
        
        if self._checkForCellAbsolute(newXPosition, newYPosition):
            return

        self._cellActed = True
        self._spawnCell(newXPosition, newYPosition, newCellBrain)


    def deleteCurrentCell(self):
        currentCell = self._cellExecutor.currentCell
        if currentCell == None:
            return
        
        currentCellX = currentCell.cellData["xPosition"]
        currentCellY = currentCell.cellData["yPosition"]

        self._updateCellMap(currentCellX, currentCellY)
        self._cellExecutor.removeCell(currentCell)
        
    def getCurrentStepNumber(self):
        return self._stepCount
    
    def getEnergyLevel(self):
        return self._cellExecutor.currentCell["energy"]
    
    def _determineDirection(self, x, y):
        newX = 0
        newY = 0
        if abs(x) >= abs(y):
            newX += math.copysign(1, x)
        else:
            newY += math.copysign(1, y)

        return (newX, newY)

    def move(self, xDirection, yDirection):
        if self._cellActed:
            return

        movementCost = 0.1
        if self._cellActed or self.getEnergyLevel() < movementCost:
            return
        
        currentCell = self._cellExecutor.currentCell
        if currentCell == None:
            return
        oldXPosition = currentCell["xPosition"]
        oldYPosition = currentCell["yPosition"]
        xDirection, yDirection = self._determineDirection(xDirection, yDirection)
        newXPosition = oldXPosition + xDirection
        newYPosition = oldYPosition + yDirection

        if not self._checkForCellAbsolute(newXPosition, newYPosition):
            currentCell["xPosition"] = newXPosition
            currentCell["yPosition"] = newYPosition

            self._updateCellMap(oldXPosition, oldYPosition)
            self._updateCellMap(newXPosition, newYPosition, currentCell)

            currentCell["energy"] -= movementCost

            self._cellActed = True

    def giveEnergy(self, xDirection, yDirection, energyValue):
        if self._cellActed:
            return

        currentCell = self._cellExecutor.currentCell
        if currentCell == None:
            return
        oldXPosition = currentCell["xPosition"]
        oldYPosition = currentCell["yPosition"]
        xDirection, yDirection = self._determineDirection(xDirection, yDirection)
        newXPosition = oldXPosition + xDirection
        newYPosition = oldYPosition + yDirection

        if not self._checkForCellAbsolute(newXPosition, newYPosition):
            return
        
        trueEnergyValue = min(max(0, energyValue), currentCell["energy"])
        currentCell["energy"] -= trueEnergyValue
        self._cellMap[("newXPosition", "newYPosition")]["energy"] += trueEnergyValue

        self._cellActed = True