from peewee import Expression
from simulator.operation.Operation import Operation
from simulator.strategy.CoveredCallStrategy import CoveredCallStrategy
from datetime import date, timedelta
from model.Pregao import Pregao

class FirstOtmCoveredCall(CoveredCallStrategy):
    DIAS_VENCIMENTO_INI = 40
    DIAS_VENCIMENTO_FIM = 45

    def get_data_ini_limit(self, data_pregao: date) -> date:
        return data_pregao + timedelta(days=FirstOtmCoveredCall.DIAS_VENCIMENTO_INI)

    def get_data_fim_limit(self, data_pregao: date) -> date:
        return data_pregao + timedelta(days=FirstOtmCoveredCall.DIAS_VENCIMENTO_FIM)

    def get_quote_expression(self, quote: float) -> Expression:
        return Pregao.preco_exercicio > (quote * 1)
