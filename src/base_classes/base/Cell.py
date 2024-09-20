class Cell:
    def __init__(self, cellData, cellBrain, environment):
        self.cellData = cellData
        self.cellBrain = cellBrain
        self.environment = environment

    def execute(self):
        self.cellBrain.run(self.environment)