from util.FilterUnique import FilterUnique
from util.CotacaoHistoricaReader import CotacaoHistoricaReader

class Filter:

    @classmethod
    def filter_mercados(cls, row: list[str]) -> bool:
        TIPOS_MERCADOS = ['010', '070', '080', '012', '013'] # vista, call, put
        #tipo_mercados = ['012', '013'] # exercicio call, put
        return CotacaoHistoricaReader.get_tipo_mercado(row) in TIPOS_MERCADOS

    @classmethod
    def filter_fii(cls, row: list[str]) -> bool:
        empresa = CotacaoHistoricaReader.get_empresa(row)
        return empresa[0:4] != 'FII '

    @classmethod
    def filter_liquidez(cls, row: list[str]) -> bool:
        return CotacaoHistoricaReader.get_negocios(row) > 100
    
    @classmethod
    def filter_empresa(cls, row: list[str]) -> bool:
        empresas = ['PETROBRAS', 'PETR', 'PETRE']
        return CotacaoHistoricaReader.get_empresa(row) in empresas

    @classmethod
    def filter_unique(cls, get_key: lambda: str) -> bool:
        return FilterUnique(get_key)