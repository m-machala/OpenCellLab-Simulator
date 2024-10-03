from CellExecutor import CellExecutor
from base_classes.base.Environment import Environment
from base_classes.base.Cell import Cell
from base_classes.base.CellBrain import CellBrain
from base_classes.base.CellData import CellData


environment = Environment()
cell = Cell(CellData(), CellBrain(environment))
executor = CellExecutor([cell])
environment.setExecutor(executor)

executor.cycleCells()
print("----------------")
executor.cycleCells()
print("----------------")
executor.cycleCells()
print("----------------")