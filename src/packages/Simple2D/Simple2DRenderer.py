from io import BytesIO
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
            ExportFunction(self.moveUp, "Move up", ControlElement.REPEATINGBUTTON, [10]),
            ExportFunction(self.moveDown, "Move down", ControlElement.REPEATINGBUTTON, [10]),
            ExportFunction(self.moveLeft, "Move left", ControlElement.REPEATINGBUTTON, [10]),
            ExportFunction(self.moveRight, "Move right", ControlElement.REPEATINGBUTTON, [10])            
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
        if outputImagePixels is None:
            return None
        
        for cell in simple2DCellList:
            if gridLeftBound <= cell.cellData["xPosition"] < gridRightBound and gridTopBound <= cell.cellData["yPosition"] < gridBottomBound:
                outputImagePixels[cell.cellData["xPosition"] - gridLeftBound, cell.cellData["yPosition"] - gridTopBound] = cell.cellData["color"]

        # Convert PIL image to PNG bytes
        buffer = BytesIO()
        outputImage.save(buffer, format="PNG")
        return buffer.getvalue()

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

