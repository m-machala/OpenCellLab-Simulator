from abc import ABC, abstractmethod

# module for loading cells into the simulator without having to place them manually
# loaders can, but don't have to, be made for a specific environment. if it is made for a specific envirnoment, it should create cells through this environment
# otherwise it should create cells through the cell executor
class Loader(ABC):
    def __init__(self, executor, environment):
        self.executor = executor
        self.environment = environment

    # returns a list of cells it wants to load in the desired execution order
    @abstractmethod
    def load(self, filePath, cellClasses):
        return []