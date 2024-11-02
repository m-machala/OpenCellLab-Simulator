from packages.base_classes.CellBrain import CellBrain
from packages.Simple2D.environments.Simple2DEnvironment import Simple2DEnvironment

class TestCell(CellBrain):
    def run(self):
        topCell = TestCell(self._environment)
        bottomCell = TestCell(self._environment)
        leftCell = TestCell(self._environment)
        rightCell = TestCell(self._environment)

        self._environment.spawnCell(0, -1, topCell)
        self._environment.spawnCell(0, 1, bottomCell)
        self._environment.spawnCell(-1, 0, leftCell)
        self._environment.spawnCell(1, 0, rightCell)

        self._environment.deleteCurrentCell()
        