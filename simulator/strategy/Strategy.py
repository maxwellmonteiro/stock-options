from datetime import date
from simulator.operation.OperationPool import OperationPool
from simulator.operation.Operation import Operation

class Strategy:

    def __init__(self, name: str, ticker: str):
        self.__name = name
        self.__ticker = ticker

    @property
    def name(self) -> str:
        return self.__name

    @property
    def ticker(self) -> str:
        return self.__ticker

    def has_operation(self, data_pregao: date) -> bool:
        pass

    def can_close_operation(self, operation: Operation, data_pregao: date) -> bool:
        pass

    def create_operation(self, data_pregao: date) -> Operation:
        pass  

    def has_opened_operation(self) -> bool:
        operation: Operation = OperationPool.instance().find_by_strategy_state(self.name, Operation.STATE_OPENED)
        return operation != None

    def open_operation(self, data_pregao: date) -> Operation:
        if not self.has_opened_operation() and self.has_operation(data_pregao):
            operation: Operation = self.create_operation(data_pregao)
            operation.open(data_pregao)
            OperationPool.instance().add(operation)
            return operation
        return None

    def close_operation(self, operation: Operation, data_pregao: date):
        if self.can_close_operation(operation, data_pregao):
            operation.close(data_pregao)    