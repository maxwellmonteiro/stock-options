from simulator.util.VolatilityHandler import VolatilityHandler
from simulator.observer.Observer import Observer
from datetime import date

class VolatilityObserver(Observer):

    def __init__(self, volatility_handler: VolatilityHandler):
        self.__volatility_handler: VolatilityHandler = volatility_handler

    def publish(self, data_pregao: date):
        self.__volatility_handler.add_volatility(data_pregao)
    

