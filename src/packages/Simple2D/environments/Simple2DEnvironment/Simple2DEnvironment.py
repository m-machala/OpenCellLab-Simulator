from base_classes.Environment import Environment
from base_classes.Cell import Cell
from ExportFunctions import ExportFunction, ControlElement

class Simple2DEnvironment(Environment):
    def __init__(self):
        super().__init__()

        self.exportFunctions = [
            ExportFunction(self.exportTestButton, "Button", ControlElement.BUTTON),
            ExportFunction(self.exportTestButton, "Radial button 1", ControlElement.RADIOBUTTON, ["1"]),
            ExportFunction(self.exportTestButton, "Radial button 2", ControlElement.RADIOBUTTON, ["1"]),            
            ExportFunction(self.exportTestButton, "Checkbox", ControlElement.CHECKBOX),
            ExportFunction(self.exportTestSlider, "Slider", ControlElement.SLIDER, [-5, 5, 3]),
            ExportFunction(self.exportTestSlider, "Spinbox", ControlElement.SPINBOX, [-2, 2, 0])
        ]

    def cellsCycled(self):
        pass

    def primaryInteraction(self, data):
        print("left click")
    
    def secondaryInteraction(self, data):
        print("right click")
    
    def tertiaryInteraction(self, data):
        print("middle click")

    def checkForCell(self, relativeXCoordinate, relativeYcoordinate):
        currentCell = self._cellExecutor.currentCell
        if currentCell == None:
            return
        
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

    def exportTestButton(self):
        print("button pressed")

    def exportTestSlider(self, value):
        print("Value changed to: " + str(value))