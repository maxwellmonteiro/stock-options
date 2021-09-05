import csv
from datetime import datetime

class CotacaoHistoricaReader:   
    def __init__(self, path: str, filter_lambda: lambda:bool):    
        csvfile = open(path, newline='', encoding='ISO-8859-1') 
        reader = csv.reader(csvfile)
        if filter is not None:
            filtered = filter(filter_lambda, reader)
        self._rows = filtered

    def get_row(self, num: int):
        return self._rows[num]

    def get_rows(self):
        return self._rows

    @classmethod
    def get_cod_papel(cls, row: list[str]) -> str:
        string: str = row[0]
        if string[0:2] == '01':
            return string[12:(12 + 12)].strip()
        return None

    @classmethod
    def get_empresa(cls, row: list[str]) -> str:
        string: str = row[0]
        if string[0:2] == '01':
            return string[27:(27 + 12)].strip()
        return None

    @classmethod
    def get_tipo_mercado(cls, row: list[str]) -> str:
        string: str = row[0]
        if string[0:2] == '01':
            return string[24:(24 + 3)].strip()
        return None