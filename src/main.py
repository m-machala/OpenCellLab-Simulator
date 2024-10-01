from Executor import Executor
from base_classes.base.Environment import Environment

executor = Executor()
environment = Environment()
executor.setEnvironment(environment)

executor.cycleCells()