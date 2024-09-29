from CellBrain import CellBrain
from CellData import CellData
from Environment import Environment

# This class represents a generic cell. It contains references to its brain and data classes.
# It also contains a reference to the environment used in the execute function.
# This is so the cell can gain info from the environment and also execute environment commands.
class Cell:
    def __init__(self, cellData: CellData, cellBrain: CellBrain, environment: Environment):
        self.cellData = cellData
        self.cellBrain = cellBrain
        self.environment = environment

    def execute(self):
        self.cellBrain.run(self.environment)