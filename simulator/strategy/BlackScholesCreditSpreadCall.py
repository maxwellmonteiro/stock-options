from datetime import date, timedelta
from model.Papel import Papel
from simulator.strategy.CoveredCallStrategy import CoveredCallStrategy
from model.Pregao import Pregao
from simulator.strategy.CreditSpreadStrategy import CreditSpreadStrategy
from peewee import Expression
from simulator.util.VolatilityHandler import VolatilityHandler
from blackscholes.VollibCall import VollibCall
from model.Selic import Selic

class BlackScholesCreditSpreadCall(CreditSpreadStrategy):
    DIAS_VENCIMENTO_INI = 20
    DIAS_VENCIMENTO_FIM = 30

    def get_data_ini_limit(self, data_pregao: date) -> date:
        return data_pregao + timedelta(days=BlackScholesCreditSpreadCall.DIAS_VENCIMENTO_INI)

    def get_data_fim_limit(self, data_pregao: date) -> date:
        return data_pregao + timedelta(days=BlackScholesCreditSpreadCall.DIAS_VENCIMENTO_FIM)

    def get_quote_expression(self, quote: float) -> Expression:
        return Pregao.preco_exercicio > (quote * 1.01)

    def is_over_valued(self, pregao: Pregao) -> bool:
        vh: VolatilityHandler = VolatilityHandler.instance()
        v: float = vh.get_volatility()
        if v != None:
            s: float = self.get_quote(self.ticker, pregao.data)
            k: float = pregao.preco_exercicio
            r: float = Selic.get(Selic.data == pregao.data).valor
            dias: int = (pregao.data_vencimento - pregao.data).days
            vollib_call: VollibCall = VollibCall(s, k, r, dias, v)
            if pregao.preco_fechamento > vollib_call.price():
                return True
        return False

    def is_under_valued(self, pregao: Pregao) -> bool:
        vh: VolatilityHandler = VolatilityHandler.instance()
        v: float = vh.get_volatility()
        if v != None:
            s: float = self.get_quote(self.ticker, pregao.data)
            k: float = pregao.preco_exercicio
            r: float = Selic.get(Selic.data == pregao.data).valor
            dias: int = (pregao.data_vencimento - pregao.data).days
            vollib_call: VollibCall = VollibCall(s, k, r, dias, v)
            if pregao.preco_fechamento < vollib_call.price():
                return True
        return False

    def has_operation(self, data_pregao: date) -> bool:
        pregao = self.get_candidate_operations(self._empresa, self._especificacao, CoveredCallStrategy.CALL, data_pregao)

        if pregao != None and self.is_over_valued(pregao):
            self.pregao = pregao
            return True
        return False

    def get_long_end(self, pregao: Pregao) -> Pregao:
        query = Pregao.select().join(Papel).where(
            (Papel.empresa == pregao.papel.empresa) &
            (Papel.tipo_mercado == pregao.papel.tipo_mercado) &
            (Papel.especificacao == pregao.papel.especificacao) &
            (Pregao.data == pregao.data) &
            (Pregao.data_vencimento == pregao.data_vencimento) &
            (Pregao.preco_exercicio.between(pregao.preco_exercicio + CreditSpreadStrategy.MIN_SPREAD, pregao.preco_exercicio + CreditSpreadStrategy.MAX_SPREAD))
        ).order_by(Pregao.preco_exercicio)
        pregao: Pregao = next((p for p in query if self.is_under_valued(p)), None)
        return pregao
