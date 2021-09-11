from datetime import date

class Trade:
    def __init__(self, ticker: str, size: int):
        self.ticker: str = ticker
        self.__size: int = size
        self.__val_open: float = None
        self.__val_close: float = None
        self.__dt_open: date = None
        self.__dt_close: date = None

    @property
    def ticker(self) -> str:
        return self.__ticker

    def open(self, data_pregao, val: float):
        self.__dt_open = data_pregao
        self.__val_open = val

    def close(self, data_pregao: date, val: float):
        self.__dt_close = data_pregao
        self.__val_close = val

    def profit(self) -> float:
        return (self.__val_close - self.__val_open) * self.__size