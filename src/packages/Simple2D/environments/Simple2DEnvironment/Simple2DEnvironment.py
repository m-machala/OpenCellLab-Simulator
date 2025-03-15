from base_classes.Environment import Environment
from base_classes.Cell import Cell
from ExportFunctions import ExportFunction, ControlElement

class Simple2DEnvironment(Environment):
    def __init__(self):
        super().__init__()
        
    def cellsCycled(self):
        pass

    def primaryInteraction(self, data):
        xCoordinate = data[0]
        yCoordinate = data[1]
        cellBrainReference = self._cellExecutor.selectedCellBrainReference
        if cellBrainReference == None:
            return

        for cell in self._cellExecutor.cellList:
            if cell.cellData["xPosition"] == xCoordinate and cell.cellData["yPosition"] == yCoordinate:
                return

        newCellBrain = cellBrainReference(self)
        newCell = Cell(newCellBrain)
        newCell.cellData["xPosition"] = xCoordinate
        newCell.cellData["yPosition"] = yCoordinate
        if hasattr(type(newCellBrain), "COLOR"):
            newCell.cellData["color"] = type(newCellBrain).COLOR
        else:
            newCell.cellData["color"] = (255, 255, 255)

        self._cellExecutor.addCell(newCell)
    
    def secondaryInteraction(self, data):
        xCoordinate = data[0]
        yCoordinate = data[1]

        for cell in self._cellExecutor.cellList:
            if cell.cellData["xPosition"] == xCoordinate and cell.cellData["yPosition"] == yCoordinate:
                self._cellExecutor.removeCell(cell)
                return
    
    def tertiaryInteraction(self, data):
        print("middle click")

    def checkForCell(self, relativeXCoordinate, relativeYcoordinate):
        currentCell = self._cellExecutor.currentCell
        if currentCell == None:
            return True
        
        currentCellX = currentCell.cellData["xPosition"]
        currentCellY = currentCell.cellData["yPosition"]

        checkedCellX = currentCellX + relativeXCoordinate
        checkedCellY = currentCellY + relativeYcoordinate

        for cell in self._cellExecutor.cellList:
            if cell.cellData["xPosition"] == checkedCellX and cell.cellData["yPosition"] == checkedCellY:
                return True
            
        return False

    def spawnCell(self, relativeXCoordinate, relativeYCoordinate, newCellBrain):
        if self.checkForCell(relativeXCoordinate, relativeYCoordinate):
            return
        
        currentCell = self._cellExecutor.currentCell
        newCell = Cell(newCellBrain)
        newCell.cellData["xPosition"] = currentCell.cellData["xPosition"] + relativeXCoordinate
        newCell.cellData["yPosition"] = currentCell.cellData["yPosition"] + relativeYCoordinate
        if hasattr(type(newCellBrain), "COLOR"):
            newCell.cellData["color"] = type(newCellBrain).COLOR
        else:
            newCell.cellData["color"] = (255, 255, 255)

        self._cellExecutor.addCell(newCell)

    def deleteCurrentCell(self):
        self._cellExecutor.removeCell(self._cellExecutor.currentCell)