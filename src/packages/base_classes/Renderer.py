from abc import ABC

class Renderer(ABC):
    def __init__(self, outputResolutionW, outputResolutionH):
        self.setOutputResolution(outputResolutionW, outputResolutionH)

    def setOutputResolution(self, outputResolutionW, outputResolutionH):
        self.outputResolutionW = outputResolutionW
        self.outputResolutionH = outputResolutionH