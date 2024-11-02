from packages.Simple2D.environments.Simple2DEnvironment.Simple2DEnvironment import Simple2DEnvironment
from packages.Simple2D.environments.Simple2DEnvironment.cellPacks.TestCell import TestCell
from packages.base_classes.Cell import Cell
from packages.Simple2D.Simple2DRenderer import Simple2DRenderer
from CellExecutor import CellExecutor

environment = Simple2DEnvironment()

firstCellBrain = TestCell(environment)
firstCell = Cell(firstCellBrain)
firstCell.cellData["color"] = (0, 255, 128)
firstCell.cellData["xPosition"] = 0
firstCell.cellData["yPosition"] = 0

executor = CellExecutor(environment, [firstCell])
environment.setExecutor(executor)

renderer = Simple2DRenderer(20, 20)
frameCounter = 0

image = renderer.render(executor.cellList)
image.save("./" + str(frameCounter) + ".png")

while True:
    frameCounter += 1
    inp = input()
    if inp == "exit":
        break
    executor.cycleCells()
    image = renderer.render(executor.cellList)
    image.save("./" + str(frameCounter) + ".png")
