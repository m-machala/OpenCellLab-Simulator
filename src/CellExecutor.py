# This class contains a list of all the currently living cells. 
# The cycleCells method uses a for loop to go through all of them and execute their code. 
class CellExecutor:
    def __init__(self, environment, initialCellList):
        self.cellList = initialCellList
        self.currentCell = initialCellList[0]
        self._environment = environment

    def cycleCells(self):
        cellListCopy = self.cellList.copy()
        for i in range(len(cellListCopy)):
            self.currentCell = cellListCopy[i]
            if self.currentCell.cellBrain == None:
                continue
            self.currentCell.execute()

        self._environment.cellsCycled()

    def addCell(self, cell):
        if(cell.cellBrain == self.currentCell.cellBrain or cell.cellData == self.currentCell.cellData):
            return
        
        self.cellList.insert(self.cellList.index(self.currentCell), cell)

    def removeCell(self, cell):
        self.cellList.remove(cell)
