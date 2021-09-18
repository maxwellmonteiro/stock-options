from datetime import date, timedelta
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

    def is_over_valued(self, pregao: Pregao):
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

    def has_operation(self, data_pregao: date) -> bool:
        pregao = self.get_candidate_operations(self._empresa, self._especificacao, CoveredCallStrategy.CALL, data_pregao)

        if pregao != None and self.is_over_valued(pregao):
            self.pregao = pregao
            return True
        return False
