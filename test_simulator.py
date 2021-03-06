from simulator.strategy.FirstItmDebitSpreadCall import FirstItmDebitSpreadCall
from simulator.strategy.BlackScholesCreditSpreadCall import BlackScholesCreditSpreadCall
from simulator.util.VolatilityHandler import VolatilityHandler
from simulator.observer.VolatilityObserver import VolatilityObserver
from simulator.strategy.FirstOtmCreditSpreadCall import FirstOtmCreditSpreadCall
from simulator.strategy.FivePercenteOtmCoveredCall import FivePercenteOtmCoveredCall
from simulator.observer.OperationStartObserver import OperationStartObserver
from peewee import fn
from datetime import date
from simulator.Simulator import Simulator
from simulator.strategy.FirstOtmCoveredCall import FirstOtmCoveredCall
from model.Pregao import Pregao
from simulator.operation.OperationPool import OperationPool

TICKER = 'VALE3'
EMPRESA = 'VALE'
TIPO = 'ON'

query = Pregao.select(fn.Distinct(Pregao.data)).order_by(Pregao.data)
pregoes: list[date] = list()
for row in query:
    pregoes.append(row.data)
simulator: Simulator = Simulator.instance()
#start_observer = OperationStartObserver(FirstOtmCoveredCall('Covered Call 1st OTM Petr4', 'PETR4', 'PETR', 'PN'))
#start_observer = OperationStartObserver(FivePercenteOtmCoveredCall('Covered Call 5% OTM Petr4', 'PETR4', 'PETR', 'PN'))
#start_observer = OperationStartObserver(FirstOtmCreditSpreadCall('Credit Spread Call 1st OTM Petr4', 'PETR4', 'PETR', 'PN'))
#start_observer = OperationStartObserver(BlackScholesCreditSpreadCall('Credit Spread Call Black&Scholes OTM Petr4', TICKER, EMPRESA, TIPO))
start_observer = OperationStartObserver(FirstItmDebitSpreadCall('Debit Spread Call 1st OTM Petr4', TICKER, EMPRESA, TIPO))
simulator.subscribe(start_observer)

volatility_handler: VolatilityHandler = VolatilityHandler.instance()
volatility_handler.set_ticker(TICKER)
volatility_observer = VolatilityObserver(volatility_handler)
simulator.subscribe(volatility_observer)

simulator.run(pregoes)

operations = OperationPool.instance().get_operations()
for operation in operations:
    print(repr(operation))

print('Total profit: {:.2f}'.format(OperationPool.instance().profit()))
print('Total operations: {}'.format(len(OperationPool.instance().get_closed())))
print('Profit ratio: {:.2f}'.format(OperationPool.instance().get_profit_ratio()))
print('Profit factor: {:.2f}'.format(OperationPool.instance().get_profit_factor()))
