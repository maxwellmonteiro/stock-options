from datetime import date
from model.Papel import Papel

from peewee import prefetch
from model.Pregao import Pregao
from simulator.operation.Trade import Trade

class Operation:
    STATE_CREATED = 0
    STATE_OPENED = 1
    STATE_CLOSED = 2

    def __init__(self, strategy, name: str):
        self.__strategy = strategy
        self.__name = name
        self.__trades: dict[str, Trade] = dict()
        self.__state = Operation.STATE_CREATED

    @property
    def strategy(self):
        return self.__strategy

    @property
    def name(self) -> str:
        return self.__name

    @property
    def state(self) -> int:
        return self.__state

    def get_trades(self) -> list[Trade]:        
        return list(self.__trades.values())

    def add_trade(self, ticker: str, size: int):
        self.__trades[ticker] = Trade(ticker, size)

    def load_pregao(self, ticker: str, data_pregao: date):
        pregao: Pregao = Pregao.select().join(Papel).where((Papel.codigo == ticker) & (Pregao.data == data_pregao)).first()
        return pregao

    def open(self, data_pregao: date):
        self.__state = Operation.STATE_OPENED
        for trade in self.__trades.values():
            pregao: Pregao = self.load_pregao(trade.ticker, data_pregao)
            trade.open(data_pregao, pregao.preco_fechamento)

    def close(self, data_pregao: date):
        self.__state = Operation.STATE_CLOSED
        for trade in self.__trades.values():
            pregao: Pregao = self.load_pregao(trade.ticker, data_pregao)
            trade.close(data_pregao, pregao.preco_fechamento)

    