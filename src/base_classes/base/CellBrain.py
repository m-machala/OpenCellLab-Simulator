from abc import ABC, abstractmethod

class CellBrain(ABC):

    @abstractmethod
    def run(self, environment):
        pass