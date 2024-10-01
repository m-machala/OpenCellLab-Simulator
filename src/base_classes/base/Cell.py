from base_classes.base.CellBrain import CellBrain
from base_classes.base.CellData import CellData
from base_classes.base.Environment import Environment

# This class represents a generic cell. It contains references to its brain and data classes.
# It also contains a reference to the environment used in the execute function.
# This is so the cell can gain info from the environment and also execute environment commands.
class Cell:
    def __init__(self, cellData: CellData, cellBrain: CellBrain, environment: Environment):
        self.cellData = cellData
        self._cellBrain = cellBrain
        self.environment = environment

        print("Init cell " + str(self))
        print("Brain " + str(self._cellBrain))
        print("Data " + str(self.cellData))
        print()

    def execute(self):
        self._cellBrain.run(self.environment)