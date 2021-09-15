from datetime import date
from functools import reduce
from model.Papel import Papel

from peewee import prefetch
from model.Pregao import Pregao
from simulator.operation.Trade import Trade

class Operation:
    STATE_CREATED = 0
    STATE_OPENED = 1
    STATE_CLOSED = 2
    STATE_INVALIDATED = 3

    def __init__(self, strategy, name: str, pregao: Pregao):
        self.__strategy = strategy
        self.__name = name
        self.__pregao = pregao
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

    @property
    def pregao(self) -> Pregao:
        return self.__pregao

    def closed(self) -> bool:
        return self.state == Operation.STATE_CLOSED

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

    def close_safe(self, data_pregao: date, trade: Trade, pregao: Pregao):
        if pregao != None:
            trade.close(data_pregao, pregao.preco_fechamento)
        else: 
            trade.close(data_pregao, trade.open_val)
            self.__state = Operation.STATE_INVALIDATED
            print('{} invalidated'.format(trade.ticker))

    def close(self, data_pregao: date):
        self.__state = Operation.STATE_CLOSED
        for trade in self.__trades.values():
            pregao: Pregao = self.load_pregao(trade.ticker, data_pregao)
            self.close_safe(data_pregao, trade, pregao)


    def profit(self) -> float:
        profit: float = 0.0
        if self.closed:
            profits = map(lambda t: t.profit(), self.get_trades())
            profit = reduce(lambda t, s: t + s, profits, 0)
        return profit

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Operation):
            other: Operation = o
            o_tickers = list(map(lambda t: t.ticker, other.get_trades()))
            s_tickers = list(map(lambda t: t.ticker, self.get_trades()))
            return all(t in o_tickers for t in s_tickers) and self.strategy == other.strategy
        return False

    def __repr__(self) -> str:
        if self.closed():
            str_trades: str = ''
            for trade in self.get_trades():
                str_trades += repr(trade) + '\n'
            return '{}\n{}profit: {:.2f}\n'.format(self.__name, str_trades, self.profit())
        return ''

    