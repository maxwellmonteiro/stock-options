from re import findall
from util.Singleton import Singleton
from simulator.operation.Operation import Operation

@Singleton
class OperationPool:
    
    def __init__(self):
        self.__operations: list[Operation] = list()

    def add(self, operation: Operation):
        self.__operations.append(operation)

    def find_opened(self, operation: Operation) -> Operation:
        return next((o for o in self.__operations if o == operation and not o.closed()), None)

    def get_operations(self) -> list[Operation]:
        return self.__operations

    def get_opened(self) -> list[Operation]:
        return list(filter(lambda o: not o.closed(), OperationPool.instance().get_operations()))
