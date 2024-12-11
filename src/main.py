from packages.Simple2D.environments.Simple2DEnvironment.Simple2DEnvironment import Simple2DEnvironment
from packages.Simple2D.environments.Simple2DEnvironment.cellPacks.Pattern import Pattern
from packages.base_classes.Cell import Cell
from packages.Simple2D.Simple2DRenderer import Simple2DRenderer
from CellExecutor import CellExecutor
import ModuleFinder

found = ModuleFinder.findPackageJSONs(".\\tmp")
print(found)