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
    def is_header(cls, row: str):
        return row[0:2] == '00'

    @classmethod
    def is_body(cls, row: str):
        return row[0:2] == '01'

    @classmethod
    def is_trailer(cls, row: str):
        return row[0:2] == '99'

    @classmethod
    def get_str(cls, row: list[str], begin: int, len: int) -> str:
        string: str = row[0]
        if CotacaoHistoricaReader.is_body(string):
            return string[begin:(begin + len)].strip()
        return None

    @classmethod
    def get_int(cls, row: list[str], begin: int, len: int) -> int:
        string: str = row[0]
        if CotacaoHistoricaReader.is_body(string):
            return int(string[begin:(begin + len)])
        return None
    
    @classmethod
    def get_float(cls, row: list[str], begin: int, len: int) -> float:
        string: str = row[0]
        if CotacaoHistoricaReader.is_body(string):
            return float(string[begin:(begin + len)]) / 100
        return None

    @classmethod
    def get_date(cls, row: list[str], begin: int, len: int) -> date:
        string: str = row[0]
        if CotacaoHistoricaReader.is_body(string):
            return datetime.strptime(string[begin:(begin + len)], '%Y%m%d').date()
        return None

    @classmethod
    def get_data_pregao(cls, row: list[str]) -> date:
        return CotacaoHistoricaReader.get_date(row, 2, 8)

    @classmethod
    def get_cod_papel(cls, row: list[str]) -> str:
        return CotacaoHistoricaReader.get_str(row, 12, 12)

    @classmethod
    def get_empresa(cls, row: list[str]) -> str:
        value = CotacaoHistoricaReader.get_str(row, 27, 12)
        return re.sub(
            r'(/EDJ)|(/ATZ)|(/ERJ)|(/EDB)|(/EDR)|(/EJS)|(/EBG)|(/ER)|(/AT)|(/EJ)|(/ED)|(/EB)|(/EX)|(/EC)|(/ES)|( FM)',
            '', value
        ).strip()

    @classmethod
    def get_tipo_mercado(cls, row: list[str]) -> str:
        return CotacaoHistoricaReader.get_str(row, 24, 3)

    @classmethod
    def get_especificacao(cls, row: list[str]) -> str:
        return CotacaoHistoricaReader.get_str(row, 39, 3)

    @classmethod
    def get_preco_fechamento(cls, row: list[str]) -> float:
        return CotacaoHistoricaReader.get_float(row, 108, 13)

    @classmethod
    def get_negocios(cls, row: list[str]) -> int:
        return CotacaoHistoricaReader.get_int(row, 152, 18)

    @classmethod
    def get_preco_exercicio(cls, row: list[str]) -> float:
        return CotacaoHistoricaReader.get_float(row, 188, 13)

    @classmethod
    def get_data_vencimento(cls, row: list[str]) -> date:
        return CotacaoHistoricaReader.get_date(row, 202, 8)