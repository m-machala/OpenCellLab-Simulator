from abc import ABC, abstractmethod

# The renderer class is used to display an image of the current running environment.
# You need to implement the render abstract method in your renderer.
class Renderer(ABC):
    def __init__(self, outputResolutionW, outputResolutionH):
        self.setOutputResolution(outputResolutionW, outputResolutionH)

    # The render function should return an image with the output resolution 
    # set in the constructor/setOutputResolution function.
    @abstractmethod
    def render(self):
        pass

    def setOutputResolution(self, outputResolutionW, outputResolutionH):
        self.outputResolutionW = outputResolutionW
        self.outputResolutionH = outputResolutionH