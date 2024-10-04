from abc import ABC, abstractmethod

# This class contains data about the cell used by the environment.
# The cell should not read or modify the contents of this class.
class CellData(ABC):
    @abstractmethod
    def __init__(self):
        pass