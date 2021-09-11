from datetime import date
from typing import overload
from simulator.observer.OperationCloseObserver import OperationCloseObserver
from simulator.observer.OperationStartObserver import OperationStartObserver
from multipledispatch import dispatch

class Simulator:

    def __init__(self, datas_pregoes: list[date]):
        self.__datas_pregoes = datas_pregoes
        self.__start_observers: list[OperationStartObserver] = list()
        self.__close_observers: list[OperationCloseObserver] = list()

    @dispatch(OperationStartObserver)
    def subscribe(self, start_observer: OperationStartObserver):
        self.__start_observers.append(start_observer)

    @dispatch(OperationCloseObserver)
    def subscribe(self, close_observer: OperationCloseObserver):
        self.__close_observers.append(close_observer)

    @dispatch(OperationStartObserver)
    def unsubscribe(self, start_observer: OperationStartObserver):
        self.__start_observers.remove(start_observer)

    @dispatch(OperationCloseObserver)
    def unsubscribe(self, close_observer: OperationCloseObserver):
        self.__close_observers.remove(close_observer)

    def run(self):
        for data_pregao in self.__datas_pregoes:
            self.process(data_pregao)

    def process(self, data_pregao: date):
        for observer in self.__start_observers:
            close_observer: OperationCloseObserver = observer.publish(data_pregao)
            if close_observer != None:
                self.subscribe(close_observer)
        
        for observer in self.__close_observers:
            unsubscribe: bool = observer.publish(data_pregao)
            if unsubscribe:
                self.unsubscribe(observer)
