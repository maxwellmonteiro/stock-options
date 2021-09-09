from datetime import date
from simulator.operation.Trade import Trade

class Operation:
    STATE_CREATED = 0
    STATE_OPENED = 1
    STATE_CLOSED = 2

    def __init__(self, name: str):
        self.__name = name
        self.__trades: list[Trade] = list()
        self.state = Operation.STATE_CREATED

    @property
    def state(self):
        return self.__state

    def add_trade(self, ticker: str, size: int):
        self.__trades.append(Trade(ticker, size))

    def open(self, data_pregao: date):
        self.__state = Operation.STATE_OPENED
        pass

    def close(self, data_pregao: date):
        self.__state = Operation.STATE_CLOSED
        pass

    