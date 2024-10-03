from abc import ABC, abstractmethod
from base_classes.base.Environment import Environment

# This class serves as the cell's "brain". It makes decisions on the cell's actions through the run method.
# It can also contain internal variables used for decision making. These shouldn't be accessed by the environment.
class CellBrain(ABC):
    def __init__(self, environment: Environment):
        self._environment = environment
    #@abstractmethod
    def run(self):
        print("Executed cell brain is " + str(self))
        print("My envionment is " + str(self._environment))
        print()
        self._environment.test()
        self._environment.addCell(CellBrain(self._environment))

        self._environment.deleteCurrentCell()