from packages.base_classes.Environment import Environment
from packages.base_classes.Cell import Cell

class Simple2DEnvironment(Environment):

    def cellsCycled(self):
        pass

    def checkForCell(self, relativeXCoordinate, relativeYcoordinate):
        currentCell = self._cellExecutor.currentCell
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