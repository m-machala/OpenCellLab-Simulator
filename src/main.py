from packages.Simple2D.environments.Simple2DEnvironment.Simple2DEnvironment import Simple2DEnvironment
from packages.Simple2D.environments.Simple2DEnvironment.cellPacks.Pattern import Pattern
from packages.base_classes.Cell import Cell
from packages.Simple2D.Simple2DRenderer import Simple2DRenderer
from CellExecutor import CellExecutor
import ModuleFinder

found = ModuleFinder.findPackageJSONs(".\\tmp")
renderer = ModuleFinder.filterJSONsByType(found, "renderer")[0]
environment = ModuleFinder.filterJSONsByType(found, "environment")[0]
cellPack = ModuleFinder.filterJSONsByType(found, "cell")[0]

loadedRenderer = ModuleFinder.loadRenderer(renderer)
loadedEnvironment = ModuleFinder.loadEnvironment(environment)
loadedCellPack = ModuleFinder.loadCellPack(cellPack)

print(loadedRenderer)
print(loadedEnvironment)
print(loadedCellPack)

print(loadedCellPack[0].COLOR)
