from abc import ABC, abstractmethod

# This class serves as the cell's "brain". It makes decisions on the cell's actions through the run method.
# It can also contain internal variables used for decision making. These shouldn't be accessed by the environment.
class CellBrain(ABC):
    def __init__(self, environment):
        self._environment = environment
        
    @abstractmethod
    def run(self):
        pass