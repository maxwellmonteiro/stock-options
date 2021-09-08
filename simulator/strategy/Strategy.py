from datetime import date
from simulator.operation.Operation import Operation

class Strategy:

    def __init__(self, name: str):
        self.__name = name

    def has_operation(self, data_pregao: date) -> bool:
        pass

    def can_close_operation(self, data_pregao: date) -> bool:
        pass

    def create_operation(self) -> Operation:
        pass    

    def run(self):
        pass

    def open(self):
        pass

    def close(self):
        pass