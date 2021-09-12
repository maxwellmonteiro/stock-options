import datetime
from model.Empresa import Empresa
from model.Papel import Papel

from peewee import Expression
from simulator.operation.Operation import Operation
from simulator.operation.Trade import Trade
from simulator.strategy.Strategy import Strategy
from datetime import date, timedelta
from model.Pregao import Pregao
from pandas.tseries.offsets import BDay

class CoveredCallStrategy(Strategy):
    CALL = 'Call'
    SIZE = -1000

    def __init__(self, name: str, underlying_asset: str, empresa: str, especificacao: str):
        super().__init__(name, underlying_asset)
        self.__empresa = empresa
        self.__especificacao = especificacao

    def get_quote(self, ticker: str, data_pregao: date) -> float:
        pregao: Pregao = Pregao.get(Pregao.papel.codigo == ticker and Pregao.data == data_pregao)
        return pregao.preco_fechamento

    def get_size(self) -> int:
        return CoveredCallStrategy.SIZE

    def get_data_ini_limit(self, data_pregao: date) -> date:
        pass

    def get_data_fim_limit(self, data_pregao: date) -> date:
        pass

    def get_quote_expression(self, quote: float) -> Expression:
        pass

    def get_candidate_operations(self, empresa: str, espec: str, tipo_mercado: str, data_pregao: date) -> Pregao:
        data_ini: date = self.get_data_ini_limit(data_pregao)
        data_fim: date = self.get_data_fim_limit(data_pregao)
        quote: float = self.get_quote(self.ticker, data_pregao)
        query = Pregao.select().join(Papel).join(Empresa).where(
            (Empresa.nome == empresa) &
            (Papel.especificacao == espec) &
            (Papel.tipo_mercado == tipo_mercado) &
            (Pregao.data == data_pregao) &
            self.get_quote_expression(quote) &
            Pregao.data_vencimento.between(data_ini, data_fim)
            ).order_by(Pregao.preco_exercicio, Pregao.data_vencimento)
        pregao: Pregao = query.first()
        return pregao

    def has_operation(self, data_pregao: date) -> bool:
        pregao = self.get_candidate_operations(self.__empresa, self.__especificacao, CoveredCallStrategy.CALL, data_pregao)
        if pregao != None:
            self.pregao = pregao
            return True
        return False

    def create_operation(self, data_pregao: date) -> Operation:
        pregao: Pregao = self.pregao
        operation: Operation = Operation(self, 'Covered Call - date {} ticker {} strike {} exercise {}'
            .format(data_pregao, pregao.papel.codigo, pregao.preco_exercicio, pregao.data_vencimento))
        operation.add_trade(pregao.papel.codigo, self.get_size())
        return operation

    def can_close_operation(self, operation: Operation, data_pregao: date) -> bool:
        trades: list[Trade] = operation.get_trades()
        pregao: Pregao = Pregao.select().join(Papel).where((Papel.codigo == trades[0].ticker) & (Pregao.data == data_pregao)).first()
        return data_pregao >= (pregao.data_vencimento - BDay(1))