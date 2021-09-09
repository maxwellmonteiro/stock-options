from datetime import date
from simulator.operation.OperationPool import OperationPool
from simulator.operation.Operation import Operation

class Strategy:

    def __init__(self, name: str):
        self.__name = name

    def has_operation(self, data_pregao: date) -> bool:
        pass

    def can_close_operation(self, operation: Operation, data_pregao: date) -> bool:
        pass

    def create_operation(self) -> Operation:
        pass    

    def open_operation(self, data_pregao: date) -> Operation:
        if self.has_operation(data_pregao):
            operation: Operation = self.create_operation(data_pregao)
            operation.open(data_pregao)
            OperationPool.instance().add(operation)
            return operation
        return None

    def close_operation(self, operation: Operation, data_pregao: date):
        if self.can_close_operation(operation, data_pregao):
            operation.close(data_pregao)    