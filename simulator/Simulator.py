from datetime import date
from simulator.observer.OperationCloseObserver import OperationCloseObserver
from simulator.observer.OperationStartObserver import OperationStartObserver
from model.Pregao import Pregao
from util.Singleton import Singleton

@Singleton
class Simulator:

    def __init__(self, datas_pregoes: list[date]):
        self.__datas_pregoes = datas_pregoes
        self.__start_observers: list[OperationStartObserver] = list()
        self.__close_observers: list[OperationCloseObserver] = list()

    def subscribe(self, start_observer: OperationStartObserver):
        self.__start_observers.append(start_observer)

    def subscribe(self, close_observer: OperationCloseObserver):
        self.__close_observers.append(close_observer)

    def unsubscribe(self, start_observer: OperationStartObserver):
        self.__start_observers.remove(start_observer)

    def unsubscribe(self, close_observer: OperationCloseObserver):
        self.__close_observers.remove(close_observer)

    def run(self):
        for data_pregao in self.__datas_pregoes:
            self.process(data_pregao)

    def process(self, data_pregao: date):
        for observer in self.__start_observers:
            observer.publish(data_pregao)
        
        for observer in self.__close_observers:
            observer.publish(data_pregao)
