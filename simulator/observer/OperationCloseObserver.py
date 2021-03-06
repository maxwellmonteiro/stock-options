from datetime import date
from simulator.strategy.Strategy import Strategy
from simulator.operation.Operation import Operation
from simulator.observer.Observer import Observer
import simulator.Simulator as S

class OperationCloseObserver(Observer):
    
    def __init__(self, operation: Operation, strategy: Strategy):
        self.__strategy: Strategy = strategy
        self.__operation: Operation = operation

    def publish(self, data_pregao: date):        
        self.__strategy.close_operation(self.__operation, data_pregao)
        if not self.__operation.opened():
            S.Simulator.instance().unsubscribe(self)

    
