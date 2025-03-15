from io import BytesIO
from PIL import Image, ImageDraw
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

        gridTopBound = self.yCenterPosition - outputBaseHeight / (2 * self.scale)
        gridBottomBound = self.yCenterPosition + outputBaseHeight / (2 * self.scale)
        gridLeftBound = self.xCenterPosition - outputBaseWidth / (2 * self.scale)
        gridRightBound = self.xCenterPosition + outputBaseWidth / (2 * self.scale)

        outputImage = Image.new("RGB", (outputBaseWidth, outputBaseHeight))
        outputImageDraw = ImageDraw.Draw(outputImage)
        if outputImageDraw is None:
            return None
        
        for cell in simple2DCellList:
            if gridLeftBound - self.scale <= cell.cellData["xPosition"] <= gridRightBound + self.scale and gridTopBound - self.scale <= cell.cellData["yPosition"] <= gridBottomBound + self.scale:
                topLeftX = min(outputBaseWidth - 1, max(0, math.floor(((cell.cellData["xPosition"] - gridLeftBound) * self.scale))))
                topLeftY = min(outputBaseHeight - 1, max(0, math.floor(((cell.cellData["yPosition"] - gridTopBound) * self.scale))))

                bottomRightX = min(outputBaseWidth - 1, max(0, math.floor(((cell.cellData["xPosition"] - gridLeftBound) * self.scale) + self.scale - 1)))
                bottomRightY = min(outputBaseHeight - 1, max(0, math.floor(((cell.cellData["yPosition"] - gridTopBound) * self.scale) + self.scale - 1)))

                if (topLeftX == bottomRightX or topLeftY == bottomRightY) and self.scale != 1:
                    continue

                if topLeftX > bottomRightX or topLeftY > bottomRightY:
                    continue

                outputImageDraw.rectangle([(topLeftX, topLeftY), (bottomRightX, bottomRightY)], fill = cell.cellData["color"])

        # Convert PIL image to PNG bytes
        buffer = BytesIO()
        outputImage.save(buffer, format="PNG")
        return buffer.getvalue()
    
    def convertFromImageCoordinates(self, xCoordinate, yCoordinate):
        xConverted = math.floor((xCoordinate / self.scale) + (self.xCenterPosition - self.outputResolutionW / (2 * self.scale)))
        yConverted = math.floor((yCoordinate / self.scale) + (self.yCenterPosition - self.outputResolutionH / (2 * self.scale)))
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
        self.scale *= 2
    
    def zoomOut(self):
        self.scale //= 2
        if self.scale < 1:
            self.scale = 1

    def setMoveSpeed(self, speed):
        self.moveSpeed = speed

    def primaryDrag(self, originalData, newData):
        self.xCenterPosition += (originalData[0] - newData[0]) / self.scale
        self.yCenterPosition += (originalData[1] - newData[1]) / self.scale

