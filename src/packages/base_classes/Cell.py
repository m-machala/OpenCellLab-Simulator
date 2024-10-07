

# This class represents a generic cell. It contains references to its brain and data classes.
class Cell:
    def __init__(self, cellBrain):
        self.cellData = {}
        self.cellBrain = cellBrain

    def execute(self):
        self.cellBrain.run()