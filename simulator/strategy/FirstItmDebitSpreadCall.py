from datetime import date, timedelta
from model.Pregao import Pregao
from simulator.strategy.DebitSpreadStrategy import DebitSpreadStrategy
from peewee import Expression

class FirstItmDebitSpreadCall(DebitSpreadStrategy):
    DIAS_VENCIMENTO_INI = 20
    DIAS_VENCIMENTO_FIM = 30

    def get_data_ini_limit(self, data_pregao: date) -> date:
        return data_pregao + timedelta(days=FirstItmDebitSpreadCall.DIAS_VENCIMENTO_INI)

    def get_data_fim_limit(self, data_pregao: date) -> date:
        return data_pregao + timedelta(days=FirstItmDebitSpreadCall.DIAS_VENCIMENTO_FIM)

    def get_quote_expression(self, quote: float) -> Expression:
        return Pregao.preco_exercicio < (quote * (1 - 0.00))
