from util.Singleton import Singleton
from simulator.operation.Operation import Operation

@Singleton
class OperationPool:
    
    def __init__(self):
        self.__operations: list[Operation] = list()

    def add(self, operation: Operation):
        self.__operations.append(operation)