from datetime import date
from model.Pregao import Pregao
from simulator.operation.Trade import Trade

class Operation:
    STATE_CREATED = 0
    STATE_OPENED = 1
    STATE_CLOSED = 2

    def __init__(self, name: str):
        self.__name = name
        self.__trades: dict[str, Trade] = dict()
        self.state = Operation.STATE_CREATED

    @property
    def state(self):
        return self.__state

    def add_trade(self, ticker: str, size: int):
        self.__trades[ticker] = Trade(ticker, size)

    def load_pregao(self, ticker: str, data_pregao: date):
        pregao: Pregao = Pregao.get(Pregao.papel.codigo == ticker and Pregao.data == data_pregao)
        return pregao

    def open(self, data_pregao: date):
        self.__state = Operation.STATE_OPENED
        for trade in self.__trades:
            pregao: Pregao = self.load_pregao(trade.ticker, data_pregao)
            trade.open(data_pregao, pregao.preco_fechamento)

    def close(self, data_pregao: date):
        self.__state = Operation.STATE_CLOSED
        for trade in self.__trades:
            pregao: Pregao = self.load_pregao(trade.ticker, data_pregao)
            trade.close(data_pregao, pregao.preco_fechamento)

    