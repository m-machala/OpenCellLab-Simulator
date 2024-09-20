class Executor:
    def __init__(self, environment):
        self.cellList = []
        self.environment = environment

    def cycleCells(self):
        for cell in self.cellList:
            cell.execute()