from peewee import fn
from datetime import date
from model.Empresa import Empresa
from model.Pregao import Pregao
from model.Papel import Papel
from simulator.operation.Operation import Operation
from simulator.strategy.CoveredCallStrategy import CoveredCallStrategy

class DebitSpreadStrategy(CoveredCallStrategy):

    MIN_SPREAD = 1
    MAX_SPREAD = 2
    
    def get_long_end(self, pregao: Pregao) -> Pregao:
        query = Pregao.select().join(Papel).where(
            (Papel.empresa == pregao.papel.empresa) &
            (Papel.tipo_mercado == pregao.papel.tipo_mercado) &
            (Papel.especificacao == pregao.papel.especificacao) &
            (Pregao.data == pregao.data) &
            (Pregao.data_vencimento == pregao.data_vencimento) &
            (Pregao.preco_exercicio.between(pregao.preco_exercicio - DebitSpreadStrategy.MAX_SPREAD, pregao.preco_exercicio - DebitSpreadStrategy.MIN_SPREAD))
        ).order_by(Pregao.preco_exercicio.desc())
        return query.first()

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
            ).order_by(Pregao.preco_exercicio.desc())
        pregao: Pregao = query.first()
        return pregao

    def create_operation(self, data_pregao: date) -> Operation:
        pregao: Pregao = self.pregao
        pregao_long_end: Pregao = self.get_long_end(pregao)
        if pregao and pregao_long_end:
            operation: Operation = Operation(self, 
                '{}@{} : +{} strike: {} -{} strike: {}'.format(self.name, self.get_quote(self.ticker, data_pregao), pregao_long_end.papel.codigo, pregao_long_end.preco_exercicio, pregao.papel.codigo, pregao.preco_exercicio),
                self.ticker)
            operation.add_trade(pregao_long_end, -1 * self.get_size()) 
            operation.add_trade(pregao, self.get_size())               
            return operation
        return None

    def can_close_by_loss(self, pregao: Pregao, operation: Operation) -> bool:
        return False

    def can_close_by_profit(self, pregao: Pregao) -> bool:
        return False

    def can_close_by_time(self, data_pregao: date, operation: Operation) -> bool:
        ticker = operation.get_trades()[0].ticker
        data_vencimento: date = operation.pregoes[0].data_vencimento
        dias_vencimento = Pregao.select(fn.Count(Pregao.data)).join(Papel).where(
            (Papel.codigo == ticker) & (Pregao.data.between(data_pregao, data_vencimento))
            ).scalar()
        return dias_vencimento <= 2