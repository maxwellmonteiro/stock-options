import csv
import re
from datetime import date, datetime

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
    def get_data_pregao(cls, row: list[str]) -> date:
        string: str = row[0]
        if string[0:2] == '01':
            value: date = datetime.strptime(string[2:(2 + 8)].strip(), '%Y%m%d').date()
            return value
        return None

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
            value = string[27:(27 + 12)].strip()
            return re.sub(r'(/EDJ)|(/ATZ)|(/ERJ)|(/ER)|(/EDB)|(/EDR)|(/EJS)|(/AT)|(/EJ)|(/ED)|(/EB)|(/EX)|(/EC)|( FM)', '', value).strip()
        return None

    @classmethod
    def get_tipo_mercado(cls, row: list[str]) -> str:
        string: str = row[0]
        if string[0:2] == '01':
            return string[24:(24 + 3)].strip()
        return None

    @classmethod
    def get_especificacao(cls, row: list[str]) -> str:
        string: str = row[0]
        if string[0:2] == '01':
            return string[39:(39 + 3)].strip()
        return None

    @classmethod
    def get_preco_fechamento(cls, row: list[str]) -> float:
        string: str = row[0]
        if string[0:2] == '01':
            value: float = float(string[108:(108 + 11)].strip())
            value = value / 100
            return value
        return None

    @classmethod
    def get_negocios(cls, row: list[str]) -> int:
        string: str = row[0]
        if string[0:2] == '01':
            value: int = int(string[152:(152 + 18)].strip())           
            return value
        return None

    @classmethod
    def get_preco_exercicio(cls, row: list[str]) -> float:
        string: str = row[0]
        if string[0:2] == '01':
            value: float = float(string[188:(188 + 11)].strip())
            value = value / 100
            return value
        return None

    @classmethod
    def get_data_vencimento(cls, row: list[str]) -> date:
        string: str = row[0]
        if string[0:2] == '01':
            value: date = datetime.strptime(string[201:(201 + 8)].strip(), '%Y%m%d').date()
            return value
        return None