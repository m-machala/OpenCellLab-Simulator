from base_classes.base.CellData import CellData

# This class represents the environment in which all of the cells exist.
# It is able to answer questions about the cell's surrounding and contains commands that the cells can use.
class Environment:
    def setActiveCellData(self, cellData: CellData):
        self._activeCellData = cellData

    def test(self):
        print("Running environment function test.")
        print("The current active cell's data is " + str(self._activeCellData))
        print("The environment is: " + str(self))
        print()