from blackscholes.HistoricalVolatility import HistoricalVolatility
from util.Singleton import Singleton
from datetime import date
from model.Pregao import Pregao
from model.Papel import Papel

@Singleton
class VolatilityHandler:
    MIN_SAMPLE = 60

    def __init__(self):
        self.__historical_volatility = HistoricalVolatility([])

    def set_ticker(self, ticker: str):
        self.__ticker = ticker

    def get_volatility(self) -> float:
        if len(self.__historical_volatility.quotes) >= self.MIN_SAMPLE:
            return self.__historical_volatility.calc()
        return None

    def add_volatility(self, data_pregao: date):
        pregao: Pregao = Pregao.select().join(Papel).where(
            (Papel.codigo == self.__ticker) &
            (Pregao.data == data_pregao)
        ).first()
        if pregao != None:
            self.__historical_volatility.add_quote(pregao.preco_fechamento)