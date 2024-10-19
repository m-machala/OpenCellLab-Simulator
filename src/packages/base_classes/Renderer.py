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

    # The render function should return an image with the output resolution 
    # set in the constructor/setOutputResolution function.
    @abstractmethod
    def render(self, cellDataList):
        pass

    def setOutputResolution(self, outputResolutionW, outputResolutionH):
        self.outputResolutionW = outputResolutionW
        self.outputResolutionH = outputResolutionH

    def getExportFunctions(self):
        return self.exportFunctions