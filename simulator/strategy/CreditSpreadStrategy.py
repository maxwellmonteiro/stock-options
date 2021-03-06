from datetime import date
from model.Pregao import Pregao
from model.Papel import Papel
from simulator.operation.Operation import Operation
from simulator.strategy.CoveredCallStrategy import CoveredCallStrategy

class CreditSpreadStrategy(CoveredCallStrategy):

    MIN_SPREAD = 1
    MAX_SPREAD = 2
    
    def get_long_end(self, pregao: Pregao) -> Pregao:
        query = Pregao.select().join(Papel).where(
            (Papel.empresa == pregao.papel.empresa) &
            (Papel.tipo_mercado == pregao.papel.tipo_mercado) &
            (Papel.especificacao == pregao.papel.especificacao) &
            (Pregao.data == pregao.data) &
            (Pregao.data_vencimento == pregao.data_vencimento) &
            (Pregao.preco_exercicio.between(pregao.preco_exercicio + CreditSpreadStrategy.MIN_SPREAD, pregao.preco_exercicio + CreditSpreadStrategy.MAX_SPREAD))
        ).order_by(Pregao.preco_exercicio)
        return query.first()

    def create_operation(self, data_pregao: date) -> Operation:
        pregao: Pregao = self.pregao
        pregao_long_end: Pregao = self.get_long_end(pregao)
        if pregao and pregao_long_end:
            operation: Operation = Operation(self, 
                '{}@{} : -{} strike: {} +{} strike: {}'.format(self.name, self.get_quote(self.ticker, data_pregao),pregao.papel.codigo, pregao.preco_exercicio, pregao_long_end.papel.codigo, pregao_long_end.preco_exercicio),
                self.ticker)
            operation.add_trade(pregao, self.get_size())
            operation.add_trade(pregao_long_end, -1 * self.get_size())    
            return operation
        return None

    def can_close_by_loss(self, pregao: Pregao, operation: Operation) -> bool:
        return False

    def can_close_by_profit(self, pregao: Pregao) -> bool:
        return False