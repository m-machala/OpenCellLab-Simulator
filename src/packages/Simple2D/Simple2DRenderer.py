from PIL import Image
from packages.base_classes.Renderer import Renderer

class Simple2DRenderer(Renderer):
    def __init__(self, outputResolutionW, outputResolutionH):
        super().__init__(outputResolutionW, outputResolutionH)
        self.scale = 1
        self.xCenterPosition = 0
        self.yCenterPosition = 0

        self.exportFunctions = [
            ("Move Up", self.moveUp),
            ("Move Down", self.moveDown),
            ("Move Left", self.moveLeft),
            ("Move Right", self.moveRight)#,
            #("Zoom In", self.zoomIn),
            #("Zoom out", self.zoomOut)
            ]

    def render(self, simple2DCellList):
        for cell in simple2DCellList:
            print(cell.cellBrain)
        print("----------")
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