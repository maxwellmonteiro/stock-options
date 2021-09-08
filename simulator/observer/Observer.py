from datetime import date
from simulator.Simulator import Simulator

class Observer:

    def __init__(self):
        self._simulator: Simulator = Simulator.instance()

    def publish(self, data_pregao: date):
        pass
