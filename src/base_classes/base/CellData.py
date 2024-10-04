from abc import ABC, abstractmethod

# This class is attached to a cell. It contains the part of its data processed by the environment. 
# The cell should not modify the contents of this class.
class CellData(ABC):
    @abstractmethod
    def __init__(self):
        pass