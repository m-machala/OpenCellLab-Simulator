from base_classes.CellBrain import CellBrain

class WhiteWall(CellBrain):
    COLOR = (255, 255, 255)

    def __init__(self, environment):
        super().__init__(environment)

    def run(self):
        pass
        
class GrayWall(CellBrain):
    COLOR = (127, 127, 127)

    def __init__(self, environment):
        super().__init__(environment)

    def run(self):
        pass