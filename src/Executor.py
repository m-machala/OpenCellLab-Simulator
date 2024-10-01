from base_classes.base.Environment import Environment
from base_classes.base.Cell import Cell
from base_classes.base.CellBrain import CellBrain
from base_classes.base.CellData import CellData

# This class contains a list of all the currently living cells. 
# The cycleCells method uses a for loop to go through all of them and execute their code. 
class Executor:
    def __init__(self):
        self._cellList = []
    
    def setEnvironment(self, environment: Environment):
        self._environment = environment

        self._cellList.append(Cell(CellData(), CellBrain(), self._environment))

    def cycleCells(self):
        for cell in self._cellList:
            self._environment.setActiveCellData(cell.cellData)
            cell.execute()