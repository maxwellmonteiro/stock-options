from datetime import date
from simulator.observer.Observer import Observer
from util.Singleton import Singleton

@Singleton
class Simulator:

    def __init__(self):
        self.__operation_observers: list[Observer] = list()
        self.__to_be_appended: list[Observer] = list()
        self.__to_be_removed: list[Observer] = list()

    def subscribe(self, observer: Observer):
        self.__to_be_appended.append(observer)

    def unsubscribe(self, observer: Observer):
        self.__to_be_removed.append(observer)

    def _update_observers(self):
        for observer in self.__to_be_appended:
            self.__operation_observers.append(observer)
        for observer in self.__to_be_removed:
            self.__operation_observers.remove(observer)
        self.__to_be_appended.clear()
        self.__to_be_removed.clear()

    def run(self, datas_pregoes: list[date]):
        self._update_observers()
        for data_pregao in datas_pregoes:
            self.process(data_pregao)

    def process(self, data_pregao: date):
        for observer in self.__operation_observers:
            observer.publish(data_pregao)
        self._update_observers()
