from base_classes.base.CellData import CellData
from base_classes.base.Cell import Cell

# This class represents the environment in which all of the cells exist.
# It is able to answer questions about the cell's surrounding and contains commands that the cells can use.
class Environment:   
    def setExecutor(self, cellExecutor):
        self._cellExecutor = cellExecutor

    def test(self):
        print("Cell " + str(self._cellExecutor.currentCell) + " has called the test function.")
        print()

    def addCell(self, cellBrain):
        newCell = Cell(CellData(), cellBrain)
        self._cellExecutor.addCell(newCell)
        print("Environment has created cell " + str(newCell))
        print()

    def deleteCurrentCell(self):
        self._cellExecutor.removeCell(self._cellExecutor.currentCell)
