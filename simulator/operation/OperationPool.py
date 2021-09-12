from re import findall
from util.Singleton import Singleton
from simulator.operation.Operation import Operation

@Singleton
class OperationPool:
    
    def __init__(self):
        self.__operations: list[Operation] = list()

    def add(self, operation: Operation):
        self.__operations.append(operation)

    def find_by_strategy_state(self, strategy: str, state: int) -> Operation:        
        return next((o for o in self.__operations if o.strategy.name == strategy and o.state == state), None)