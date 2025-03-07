from abc import ABC, abstractmethod

# This class represents the environment in which all of the cells exist
# It is able to answer questions about the cell's surrounding and contains commands that the cells can use
# An environment works within a renderer
# This means that the cells in an environments must follow conventions of the renderer
# For example: 
#   A renderer may work with a 2D coordinate system and RGB colors
#   This means that all of the cells working with that renderer have to have this data to be rendered properly
#   It also means that the environment within the renderer should work with this data
class Environment(ABC):   
    def __init__(self):
        self.exportFunctions = []

    # This function sets the internal reference to the executor class
    # It should be called every time an instance of an environment has been created
    # Both the environment and the executor have a reference to each other
    # This means that the executor can't be set in the __init__ function, as it would create issues with circular assignment
    def setExecutor(self, cellExecutor):
        self._cellExecutor = cellExecutor

    # This function is called every time all of the active cells have been executed, and are ready for the next loop
    @abstractmethod
    def cellsCycled(self):
        pass

    # Used for handling user interaction with the simulation
    # The data variable contains data about the interactions in an arbitrary form set by the renderer
    # Please check your renderer's documentation to see what data is being passed
    # The primary interaction usually represents a left click onto the simulation window
    @abstractmethod
    def primaryInteraction(self, data):
        pass

    # Used for handling user interaction with the simulation
    # The data variable contains data about the interactions in an arbitrary form set by the renderer
    # Please check your renderer's documentation to see what data is being passed
    # The primary interaction usually represents a right click onto the simulation window
    @abstractmethod
    def secondaryInteraction(self, data):
        pass

    # Used for handling user interaction with the simulation
    # The data variable contains data about the interactions in an arbitrary form set by the renderer
    # Please check your renderer's documentation to see what data is being passed
    # The primary interaction usually represents a middle click onto the simulation window
    @abstractmethod
    def tertiaryInteraction(self, data):
        pass
