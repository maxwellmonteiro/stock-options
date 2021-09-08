from datetime import date
from simulator.strategy.Strategy import Strategy
from simulator.Simulator import Simulator
from simulator.operation.Operation import Operation
from simulator.observer.Observer import Observer

class OperationCloseObserver(Observer):
    
    def __init__(self, operation: Operation, strategy: Strategy):
        super().__init__()
        self.__strategy: Strategy = strategy
        self.__operation: Operation = operation

    def can_close_operation(self, data_pregao: date) -> bool:
        return self.__strategy.can_close_operation(data_pregao)

    def publish(self, data_pregao: date):
        if self.can_close_operation():
            self.__operation.close(data_pregao)            
            self._simulator.unsubscribe(self)

    
