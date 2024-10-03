# This class represents a generic cell. It contains references to its brain and data classes.
# It also contains a reference to the environment used in the execute function.
# This is so the cell can gain info from the environment and also execute environment commands.
class Cell:
    def __init__(self, cellData, cellBrain):
        self.cellData = cellData
        self.cellBrain = cellBrain

        print("Init cell " + str(self))
        print("Brain " + str(self.cellBrain))
        print("Data " + str(self.cellData))
        print()

    def execute(self):
        self.cellBrain.run()