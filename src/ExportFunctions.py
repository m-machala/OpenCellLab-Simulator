from enum import Enum

class ControlElement(Enum):
    # no additional arguments. function does not need input variables
    BUTTON = 1
    # one additional argument: time between function activations in ms. function does not need input variables
    REPEATINGBUTTON = 2
    # group name as an additional argument. determined which other buttons turn off once this button gets pressed. function does not need input variables
    RADIOBUTTON = 3
    # no additional arguments. function does not need input variables
    CHECKBOX = 4
    # three additional arguments: bottom value, top value, starting value. all have to be whole numbers. the bottom value has to be lower than the top value
    # function needs one input variable (it will only receive integers)
    SLIDER = 5
    # same as slider
    SPINBOX = 6

class ExportFunction():
    def __init__(self, functionReference, name, controlElement, additionalArguments = []):
        self.functionReference = functionReference
        self.name = name
        self.controlElement = controlElement
        self.additionalArguments = additionalArguments