from datetime import date
from simulator.strategy.Strategy import Strategy

from model.Pregao import Pregao
from simulator.observer.OperationCloseObserver import OperationCloseObserver
from simulator.observer.Observer import Observer
from simulator.operation.Operation import Operation
from simulator.operation.OperationPool import OperationPool
from simulator.Simulator import Simulator


class OperationStartObserver(Observer):
    
    def __init__(self, strategy: Strategy):
        super().__init__()    
        self.__strategy: Strategy = strategy
        self.__operation_pool: OperationPool = OperationPool.instance()

    def create_operation_close_observer(self, operation: Operation) -> OperationCloseObserver:
        return OperationCloseObserver(operation, self.__strategy)

    def has_operation(self, data_pregao: date):
        return self.__strategy.has_operation(date)

    def create_operation(self, data_pregao: date) -> Operation:
        return self.__strategy.create_operation(data_pregao)

    def publish(self, data_pregao: date):
        if self.has_operation(data_pregao):
            operation = self.create_operation(data_pregao)
            operation.open(data_pregao)
            self._simulator.subscribe(self.create_operation_close_observer(operation))
            self.__operation_pool.add(operation)
