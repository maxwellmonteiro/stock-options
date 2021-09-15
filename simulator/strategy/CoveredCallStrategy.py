from simulator.operation.OperationPool import OperationPool
from model.Empresa import Empresa
from model.Papel import Papel

from peewee import Expression, fn
from simulator.operation.Operation import Operation
from simulator.operation.Trade import Trade
from simulator.strategy.Strategy import Strategy
from datetime import date
from model.Pregao import Pregao
from pandas.tseries.offsets import BDay

class CoveredCallStrategy(Strategy):
    CALL = 'Call'
    SIZE = -1000
    INFINITY = 999999
    MIN_VOLUME = 1000

    def __init__(self, name: str, underlying_asset: str, empresa: str, especificacao: str):
        super().__init__(name, underlying_asset)
        self.__empresa = empresa
        self.__especificacao = especificacao

    def get_quote(self, ticker: str, data_pregao: date) -> float:
        query = Pregao.select().join(Papel).where((Papel.codigo == ticker) & (Pregao.data == data_pregao))
        pregao: Pregao = query.first()
        if pregao != None:
            return pregao.preco_fechamento
        return CoveredCallStrategy.INFINITY

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
            (Pregao.negocios >= CoveredCallStrategy.MIN_VOLUME) &
            self.get_quote_expression(quote) &
            Pregao.data_vencimento.between(data_ini, data_fim)
            ).order_by(Pregao.preco_exercicio)
        pregao: Pregao = query.first()
        return pregao

    def has_operation(self, data_pregao: date) -> bool:
        pregao = self.get_candidate_operations(self.__empresa, self.__especificacao, CoveredCallStrategy.CALL, data_pregao)
        if pregao != None:
            self.pregao = pregao
            return True
        return False

    def has_opened_operation(self, operation: Operation) -> bool:
        operations: list[Operation] = OperationPool.instance().get_opened()
        o = next((o for o in operations if o.pregao.data_vencimento == operation.pregao.data_vencimento), None)
        return o != None

    def create_operation(self, data_pregao: date) -> Operation:
        pregao: Pregao = self.pregao
        operation: Operation = Operation(self, 
            '{} - underlying asset: {}@{} date: {} ticker: {} strike: {} exercise: {}'.format(self.name, self.ticker, self.get_quote(self.ticker, data_pregao), data_pregao, pregao.papel.codigo, pregao.preco_exercicio, pregao.data_vencimento),
            pregao)
        operation.add_trade(pregao.papel.codigo, self.get_size())
        return operation

    def can_close_by_time(self, data_pregao: date, operation: Operation) -> bool:
        ticker = operation.get_trades()[0].ticker
        data_vencimento: date = operation.pregao.data_vencimento
        dias_vencimento = Pregao.select(fn.Count(Pregao.data)).join(Papel).where(
            (Papel.codigo == ticker) & (Pregao.data.between(data_pregao, data_vencimento))
            ).scalar()
        return dias_vencimento <= 1

    def can_close_by_loss(self, pregao: Pregao, operation: Operation) -> bool:
        trades: list[Trade] = operation.get_trades()
        return pregao != None and pregao.preco_fechamento >= (2 * trades[0].open_val)

    def can_close_by_profit(self, pregao: Pregao) -> bool:        
        return pregao != None and pregao.preco_fechamento == 0.01

    def can_close_fail_safe(self, data_pregao: date, operation: Operation) -> bool:
        trades: list[Trade] = operation.get_trades()
        return data_pregao > self.get_data_fim_limit(trades[0].open_dt)


    def can_close_operation(self, operation: Operation, data_pregao: date) -> bool:
        trades: list[Trade] = operation.get_trades()
        pregao: Pregao = Pregao.select().join(Papel).where((Papel.codigo == trades[0].ticker) & (Pregao.data == data_pregao)).first()
        
        return (
            self.can_close_by_profit(pregao) or 
            self.can_close_by_time(data_pregao, operation) or 
          #  self.can_close_by_loss(pregao, operation) or
            self.can_close_fail_safe(data_pregao, operation)
            )