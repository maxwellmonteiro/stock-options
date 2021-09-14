from datetime import date
from simulator.strategy.Strategy import Strategy

from simulator.observer.OperationCloseObserver import OperationCloseObserver
from simulator.observer.Observer import Observer
from simulator.operation.Operation import Operation
import simulator.Simulator as S

class OperationStartObserver(Observer):
    
    def __init__(self, strategy: Strategy):
        self.__strategy: Strategy = strategy

    def create_operation_close_observer(self, operation: Operation) -> OperationCloseObserver:
        return OperationCloseObserver(operation, self.__strategy)

    def publish(self, data_pregao: date):
        operation: Operation = self.__strategy.open_operation(data_pregao)
        if operation != None:            
            close_observer: OperationCloseObserver = self.create_operation_close_observer(operation)
            S.Simulator.instance().subscribe(close_observer)