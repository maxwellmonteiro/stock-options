from simulator.observer.OperationStartObserver import OperationStartObserver
from peewee import fn
from datetime import date
from simulator.Simulator import Simulator
from simulator.strategy.FirstOtmCoveredCall import FirstOtmCoveredCall
from model.Pregao import Pregao
from simulator.operation.OperationPool import OperationPool

query = Pregao.select(fn.Distinct(Pregao.data)).order_by(Pregao.data)
pregoes: list[date] = list()
for row in query:
    pregoes.append(row.data)
simulator: Simulator = Simulator.instance()
start_observer = OperationStartObserver(FirstOtmCoveredCall('Covered Call 1st OTM Petr4', 'PETR4', 'PETR', 'PN'))
simulator.subscribe(start_observer)
simulator.run(pregoes)

operations = OperationPool.instance().get_operations()
for operation in operations:
    print(repr(operation))