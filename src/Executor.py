from base_classes.base.Environment import Environment

# This class contains a list of all the currently living cells. 
# The cycleCells method uses a for loop to go through all of them and execute their code. 
class Executor:
    def __init__(self, environment: Environment):
        self.cellList = []
        self.environment = environment

    def cycleCells(self):
        for cell in self.cellList:
            cell.execute()