from abc import ABC, abstractmethod

# module for loading cells into the simulator without having to place them manually
class Loader(ABC):
    # returns a list of cells it wants to load in the desired execution order
    @abstractmethod
    def load(self, file):
        return []