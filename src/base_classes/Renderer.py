from abc import ABC, abstractmethod

# The renderer class is used to display an image of the current running environment.
# You need to implement the render abstract method in your renderer.
# You can also put function references into the exportFunctions list in the form of a tuple.
# The tuple has to contain a name and a function reference.
# An example of a correct tuple would be: ("Zoom in", zoomImage)  where zoomImage is a function in your code.
class Renderer(ABC):
    # If you want to have your own init function in your renderer, feel free to use the following commented code:
    # def __init__(self, outputResolutionW, outputResolutionH):
    #     super().__init__(outputResolutionW, outputResolutionH)

    def __init__(self, outputResolutionW, outputResolutionH):
        self.setOutputResolution(outputResolutionW, outputResolutionH)
        self.exportFunctions = []

    # The render function should return an image in the output resolution 
    # set in the constructor/setOutputResolution function.
    @abstractmethod
    def render(self, cellDataList):
        pass
    
    # This function should transform the coordinates of the rendered image into a form usable by environments
    # The main purpose of this function is to determine which part of the simulation the user is interacting with
    # The output of this function can vary based on what's convenient for the renderer and its environments
    # The output will be handed directly to the active environment's functions for interpreting clicks
    @abstractmethod
    def convertFromImageCoordinates(self, xCoordinate, yCoordinate):
        pass

    # Sets the output resolution. This function is called whenever the simulation window in the UI is resized
    # W is width, H is height
    def setOutputResolution(self, outputResolutionW, outputResolutionH):
        self.outputResolutionW = outputResolutionW
        self.outputResolutionH = outputResolutionH

    # Returns a list of functions to be exported into the UI
    # For more info check ExportFunctions.py
    def getExportFunctions(self):
        return self.exportFunctions
    
    # Used for handling the user left-clicking the simulation
    # The data variable contains a tuple of the x and y coordinates
    def _primaryClick(self, data):
        pass
    
    # Same as above but for a click and drag
    # originalData represents the interaction data from the initial press, newData represents the current data
    def _primaryDrag(self, originalData, newData):
        pass

    # Used for handling the user right-clicking the simulation
    # The data variable contains a tuple of the x and y coordinates
    def _secondaryClick(self, data):
        pass

    # Same as above but for a click and drag
    # originalData represents the interaction data from the initial press, newData represents the current data
    def _secondaryDrag(self, originalData, newData):
        pass

    # Used for handling the user middle-clicking the simulation
    # The data variable contains a tuple of the x and y coordinates
    def _tertiaryClick(self, data):
        pass

    # Same as above but for a click and drag
    # originalData represents the interaction data from the initial press, newData represents the current data
    def _tertiaryDrag(self, originalData, newData):
        pass
    