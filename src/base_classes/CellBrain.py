from abc import ABC, abstractmethod

# This class serves as the cell's "brain". It makes decisions on the cell's actions through the run method
# It can also contain internal variables used for decision making. These shouldn't be accessed by the environment
# The cell brain has a reference to the environment, meaning that it can call its functions to perform actions and to find information about the world
# Functions and variables starting with _ are private, therefore you should not use them, otherwise you risk breaking things
class CellBrain(ABC):
    def __init__(self, environment):
        self._environment = environment
        
    @abstractmethod
    def run(self):
        pass