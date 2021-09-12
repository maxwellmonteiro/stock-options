from peewee import fn
from datetime import date
from simulator.Simulator import Simulator
from simulator.observer.OperationStartObserver import OperationStartObserver
from simulator.strategy.FirstOtmCoveredCall import FirstOtmCoveredCall
from model.Pregao import Pregao

query = Pregao.select(fn.Distinct(Pregao.data)).order_by(Pregao.data)
pregoes: list[date] = list()
for row in query:
    pregoes.append(row.data)
simulator: Simulator = Simulator(pregoes)
start_observer: OperationStartObserver
start_observer = OperationStartObserver(FirstOtmCoveredCall('Covered Call Petr4', 'PETR4', 'PETR', 'PN'))
simulator.subscribe(start_observer)
simulator.run()