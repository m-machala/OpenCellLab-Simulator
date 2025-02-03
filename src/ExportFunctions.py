from enum import Enum

class ControlElement(Enum):
    BUTTON = 1
    RADIALBUTTON = 2
    CHECKBOX = 3
    SLIDER = 4
    SPINBOX = 5

class ExportFunction():
    def __init__(self, functionReference, name, controlElement, additionalArguments = []):
        self.functionReference = functionReference
        self.name = name
        self.controlElement = controlElement
        self.additionalArguments = additionalArguments