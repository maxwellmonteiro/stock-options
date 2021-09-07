from util.Filter import Filter
from util.FilterUnique import FilterUnique
from util.CotacaoHistoricaReader import CotacaoHistoricaReader as chr
from model.Empresa import Empresa

def inserir_empresa(nome):
    query = Empresa.select().where(Empresa.nome == nome)
    if not query.exists():
        empresa = Empresa.create(nome=nome)

PATH = 'data/COTAHIST_A2021.TXT'
filter_unique_empresa = Filter.filter_unique(lambda r: chr.get_empresa(r))
filter = lambda r: Filter.filter_mercados(r) and Filter.filter_fii(r) and filter_unique_empresa(r)
reader = chr(PATH, filter)

rows = reader.get_rows()
for row in rows:    
    inserir_empresa(chr.get_empresa(row))
