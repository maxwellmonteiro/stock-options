from util.FilterUnique import FilterUnique
from util.CotacaoHistoricaReader import CotacaoHistoricaReader
from model.Empresa import Empresa

def filter_mercados(row: list[str]) -> bool:
    tipo_mercados = ['010', '070', '080'] # vista, call, put
    return CotacaoHistoricaReader.get_tipo_mercado(row) in tipo_mercados

def filter_fii(row: list[str]) -> bool:
    empresa = CotacaoHistoricaReader.get_empresa(row)
    return empresa[0:4] != 'FII '

def inserir_empresa(nome):
    query = Empresa.select().where(Empresa.nome == nome)
    if not query.exists():
        empresa = Empresa.create(nome=nome)

PATH = 'data/COTAHIST_A2021.TXT'
filter_unique_empresa = FilterUnique(lambda r: CotacaoHistoricaReader.get_empresa(r))
filter = lambda r: filter_mercados(r) and filter_fii(r) and filter_unique_empresa(r)
reader = CotacaoHistoricaReader(PATH, filter)

rows = reader.get_rows()
for row in rows:    
    inserir_empresa(CotacaoHistoricaReader.get_empresa(row))
