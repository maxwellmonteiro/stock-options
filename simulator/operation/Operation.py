from datetime import date
from simulator.operation.Trade import Trade

class Operation:
    def __init__(self, name: str):
        self.__name = name
        self.__trades: list[Trade] = list()

    def add_trade(self, ticker: str, size: int):
        self.__trades.append(Trade(ticker, size))

    def open(self, data_pregao: date):
        pass

    def close(self, data_pregao: date):
        pass

    