import datetime
from simulator.operation.Operation import Operation
from simulator.operation.Trade import Trade
from typing import Iterator
import peewee
from simulator.strategy.Strategy import Strategy
from datetime import date
from model.Pregao import Pregao
from model.Papel import Papel

class CoveredCallStrategy(Strategy):
    CALL = 'Call'
    DIAS_VENCIMENTO_INI: 40
    DIAS_VENCIMENTO_FIM: 45

    def __init__(self, name: str, underlying_asset: str, empresa: str, especificacao: str):
        super().__init__(name, underlying_asset)
        self.__empresa = empresa
        self.__especificacao = especificacao

    def get_quote(self, ticker: str, data_pregao: date) -> float:
        pregao: Pregao = Pregao.get(Pregao.papel.codigo == ticker and Pregao.data == data_pregao)
        return pregao.preco_fechamento

    def get_limit_date(self, data_pregao: date, limit: int) -> date:
        return data_pregao + datetime.timedelta(days=limit)

    def load_pregao(self, empresa: str, espec: str, tipo_mercado: str, data_pregao: date) -> Pregao:
        data_ini: date = self.get_limit_date(data_pregao, CoveredCallStrategy.DIAS_VENCIMENTO_INI)
        data_fim: date = self.get_limit_date(data_pregao, CoveredCallStrategy.DIAS_VENCIMENTO_FIM)
        quote: float = self.get_quote(self.__ticker, data_pregao)
        pregao = Pregao.select(Pregao).where(
            Pregao.papel.empresa.name == empresa and
            Pregao.papel.especificacao == espec and
            Pregao.papel.tipo_mercado == tipo_mercado and
            Pregao.data == data_pregao and
            Pregao.preco_exercicio > quote and # OTM
            Pregao.data_vencimento.between(data_ini, data_fim)
            ).order_by(Pregao.preco_exercicio, Pregao.data_vencimento).get()
        return pregao

    def has_operation(self, data_pregao: date) -> bool:
        pregao = self.load_pregao(self.__empresa, self.__especificacao, CoveredCallStrategy.CALL, data_pregao)
        if pregao != None:
            self.pregao = pregao
            return True
        return False

    def create_operation(self) -> Operation:
        pregao: Pregao = self.pregao
        operation: Operation = Operation('Covered Call - today {} ticker {} strike {} time {}'
            .format(pregao.data, pregao.papel.codigo, pregao.preco_exercicio, pregao.data_vencimento))
        operation.add_trade(pregao.papel.codigo, -1000)
        return operation