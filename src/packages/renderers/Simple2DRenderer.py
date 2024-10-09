from packages.base_classes.Renderer import Renderer
class Simple2DRenderer(Renderer):
    def __init__(self, outputResolutionH, outputResolutionV):
        self.outputResolutionH = outputResolutionH
        self.outputResolutionV = outputResolutionV

    