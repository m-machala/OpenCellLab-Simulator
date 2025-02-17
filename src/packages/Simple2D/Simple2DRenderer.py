from PIL import Image
from base_classes.Renderer import Renderer
from ExportFunctions import ExportFunction, ControlElement

class Simple2DRenderer(Renderer):
    def __init__(self, outputResolutionW, outputResolutionH):
        super().__init__(outputResolutionW, outputResolutionH)
        self.scale = 1
        self.xCenterPosition = 0
        self.yCenterPosition = 0

        self.exportFunctions = [
            ExportFunction(self.moveUp, "Move up", ControlElement.BUTTON),
            ExportFunction(self.moveDown, "Move down", ControlElement.BUTTON),
            ExportFunction(self.moveLeft, "Move left", ControlElement.BUTTON),
            ExportFunction(self.moveRight, "Move right", ControlElement.BUTTON)            
        ]

    def render(self, simple2DCellList):
        outputBaseWidth = self.outputResolutionW
        outputBaseHeight = self.outputResolutionH

        gridTopBound = (self.yCenterPosition + outputBaseHeight // 2) - outputBaseHeight
        gridBottomBound = (self.yCenterPosition + outputBaseHeight // 2)
        gridLeftBound = (self.xCenterPosition + outputBaseWidth // 2) - outputBaseWidth
        gridRightBound = (self.xCenterPosition + outputBaseWidth // 2)

        outputImage = Image.new("RGB", (outputBaseWidth, outputBaseHeight))
        outputImagePixels = outputImage.load()

        for cell in simple2DCellList:
            if gridLeftBound <= cell.cellData["xPosition"] < gridRightBound and gridTopBound <= cell.cellData["yPosition"] < gridBottomBound:
                outputImagePixels[cell.cellData["xPosition"] - gridLeftBound, cell.cellData["yPosition"] - gridTopBound] = cell.cellData["color"]
        
        return outputImage

    def moveUp(self):
        self.yCenterPosition -= 1

    def moveDown(self):
        self.yCenterPosition += 1

    def moveLeft(self):
        self.xCenterPosition -= 1

    def moveRight(self):
        self.xCenterPosition += 1

    #def zoomIn(self):
    #    self.scale += 1
    #
    #def zoomOut(self):
    #    self.scale -= 1
    #    if self.scale < 1:
    #        self.scale = 1