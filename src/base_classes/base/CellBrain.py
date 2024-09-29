from abc import ABC, abstractmethod
from Environment import Environment

# This class serves as the cell's "brain". It makes decisions on the cell's actions through the run method.
# It can also contain internal variables used for decision making. These shouldn't be accessed by the environment.
class CellBrain(ABC):

    @abstractmethod
    def run(self, environment: Environment):
        pass