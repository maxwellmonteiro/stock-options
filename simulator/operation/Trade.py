from datetime import date

from simulator.strategy.Strategy import Strategy

class Trade:
    def __init__(self, ticker: str, size: int):
        self.__ticker: str = ticker
        self.__size: int = size
        self.__val_open: float = 0.0
        self.__val_close: float = 0.0
        self.__dt_open: date = None
        self.__dt_close: date = None

    def open(self, val_open: float):
        pass

    def close(self, val_close: float):
        pass

    def profit(self) -> float:
        pass