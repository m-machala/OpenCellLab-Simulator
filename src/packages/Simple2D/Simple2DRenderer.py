from io import BytesIO
from PIL import Image
from base_classes.Renderer import Renderer
from ExportFunctions import ExportFunction, ControlElement
import math

class Simple2DRenderer(Renderer):
    def __init__(self, outputResolutionW, outputResolutionH):
        super().__init__(outputResolutionW, outputResolutionH)
        self.scale = 1
        self.moveSpeed = 1
        self.xCenterPosition = 0
        self.yCenterPosition = 0

        self.exportFunctions = [
            ExportFunction(self.moveUp, "Move up", ControlElement.REPEATINGBUTTON, [10]),
            ExportFunction(self.moveDown, "Move down", ControlElement.REPEATINGBUTTON, [10]),
            ExportFunction(self.moveLeft, "Move left", ControlElement.REPEATINGBUTTON, [10]),
            ExportFunction(self.moveRight, "Move right", ControlElement.REPEATINGBUTTON, [10]),
            ExportFunction(self.zoomIn, "Zoom in", ControlElement.BUTTON),
            ExportFunction(self.zoomOut, "Zoom out", ControlElement.BUTTON),
            ExportFunction(self.setMoveSpeed, "Camera speed", ControlElement.SLIDER, [1, 25, 1])            
        ]

    def render(self, simple2DCellList):
        outputBaseWidth = self.outputResolutionW
        outputBaseHeight = self.outputResolutionH

        gridTopBound = self.yCenterPosition - outputBaseHeight // (2 * self.scale)
        gridBottomBound = math.ceil(self.yCenterPosition + outputBaseHeight / (2 * self.scale))
        gridLeftBound = self.xCenterPosition - outputBaseWidth // (2 * self.scale)
        gridRightBound = math.ceil(self.xCenterPosition + outputBaseWidth / (2 * self.scale))

        outputImage = Image.new("RGB", (outputBaseWidth, outputBaseHeight))
        outputImagePixels = outputImage.load()
        if outputImagePixels is None:
            return None
        
        for cell in simple2DCellList:
            if gridLeftBound - 1 <= cell.cellData["xPosition"] <= gridRightBound and gridTopBound - 1 <= cell.cellData["yPosition"] <= gridBottomBound:
                for scaleX in range(self.scale):
                    for scaleY in range(self.scale):
                        xPosition = ((cell.cellData["xPosition"] - gridLeftBound) * self.scale) + scaleX
                        yPosition = ((cell.cellData["yPosition"] - gridTopBound) * self.scale) + scaleY

                        if 0 <= xPosition < self.outputResolutionW and 0 <= yPosition < self.outputResolutionH:
                            outputImagePixels[xPosition, yPosition] = cell.cellData["color"]

        # Convert PIL image to PNG bytes
        buffer = BytesIO()
        outputImage.save(buffer, format="PNG")
        return buffer.getvalue()
    
    def convertFromImageCoordinates(self, xCoordinate, yCoordinate):
        xConverted = (xCoordinate // self.scale) + (math.floor(self.xCenterPosition) - self.outputResolutionW // (2 * self.scale))
        yConverted = (yCoordinate // self.scale) + (math.floor(self.yCenterPosition) - self.outputResolutionH // (2 * self.scale))
        return [xConverted, yConverted]

    def moveUp(self):
        self.yCenterPosition -= self.moveSpeed / self.scale

    def moveDown(self):
        self.yCenterPosition += self.moveSpeed / self.scale

    def moveLeft(self):
        self.xCenterPosition -= self.moveSpeed / self.scale

    def moveRight(self):
        self.xCenterPosition += self.moveSpeed / self.scale

    def zoomIn(self):
        self.scale += 1
    
    def zoomOut(self):
        self.scale -= 1
        if self.scale < 1:
            self.scale = 1

    def setMoveSpeed(self, speed):
        self.moveSpeed = speed

