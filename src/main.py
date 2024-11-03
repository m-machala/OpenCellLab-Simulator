from packages.Simple2D.environments.Simple2DEnvironment.Simple2DEnvironment import Simple2DEnvironment
from packages.Simple2D.environments.Simple2DEnvironment.cellPacks.Pattern import Pattern
from packages.base_classes.Cell import Cell
from packages.Simple2D.Simple2DRenderer import Simple2DRenderer
from CellExecutor import CellExecutor

environment = Simple2DEnvironment()

firstCellBrain = Pattern(environment)
firstCell = Cell(firstCellBrain)
firstCell.cellData["xPosition"] = 0
firstCell.cellData["yPosition"] = 0
firstCell.cellData["color"] = Pattern.COLOR


executor = CellExecutor(environment, [firstCell])
environment.setExecutor(executor)

renderer = Simple2DRenderer(20, 20)
frameCounter = 0

image = renderer.render(executor.cellList)
image.save("./tmp/" + str(frameCounter) + ".png")

for frameCounter in range(1, 10):
    executor.cycleCells()
    image = renderer.render(executor.cellList)
    image.save("./tmp/" + str(frameCounter) + ".png")