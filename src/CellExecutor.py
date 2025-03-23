# This class contains a list of all the currently living cells. 
# The cycleCells method uses a for loop to go through all of them and execute their code. 
class CellExecutor:
    def __init__(self, environment, initialCellList):
        self.cellList = initialCellList
        self.currentCell = None
        self._environment = environment
        # Cell brain reference selected by the user in the UI
        self.selectedCellBrainReference = None

    def selectCellBrainReference(self, cellBrain):
        self.selectedCellBrainReference = cellBrain

    def cycleCells(self):
        cellListCopy = self.cellList.copy()
        for i in range(len(cellListCopy)):
            self.currentCell = cellListCopy[i]
            if self.currentCell.cellBrain == None:
                continue
            self.currentCell.execute()

        self._environment.cellsCycled()

    def addCell(self, cell):
        for livingCell in self.cellList:
            if(cell.cellBrain == livingCell.cellBrain or cell.cellData == livingCell.cellData):
                return
        insertionIndex = 0
        if self.currentCell != None:
            insertionIndex = self.cellList.index(self.currentCell)
        self.cellList.insert(insertionIndex, cell)

    def removeCell(self, cell):
        if self.currentCell == cell:
            self.currentCell = None
        self.cellList.remove(cell)
        
    def clearCells(self):
        self.currentCell = None
        self.cellList.clear()
        self._environment.executorClearedCells()
