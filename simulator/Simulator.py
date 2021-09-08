from datetime import date
from simulator.observer.OperationCloseObserver import OperationCloseObserver
from simulator.observer.OperationStartObserver import OperationStartObserver
from model.Pregao import Pregao
from util.Singleton import Singleton

@Singleton
class Simulator:

    def __init__(self, datas_pregoes: list[date]):
        self.datas_pregoes = datas_pregoes
        self.strategy_observers: list[OperationStartObserver] = list()
        self.managment_observers: list[OperationCloseObserver] = list()

    def subscribe(self, strategy_observer: OperationStartObserver):
        self.strategy_observers.append(strategy_observer)

    def subscribe(self, managment_observer: OperationCloseObserver):
        self.managment_observers.append(managment_observer)

    def unsubscribe(self, strategy_observer: OperationStartObserver):
        self.strategy_observers.remove(strategy_observer)

    def unsubscribe(self, managment_observer: OperationCloseObserver):
        self.managment_observers.remove(managment_observer)

    def run(self):
        for pregao in self.pregoes:
            self.process(pregao)

    def process(self, pregao: Pregao):
        for strategy in self.strategy_observers:
            strategy.publish(pregao)
        
        for managment in self.managment_observers:
            managment.publish(pregao)
