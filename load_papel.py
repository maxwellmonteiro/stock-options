from peewee import DoesNotExist
from model.Empresa import Empresa
from util.FilterUnique import FilterUnique
from util.CotacaoHistoricaReader import CotacaoHistoricaReader
from model.Papel import Papel
import re

def filter_mercados(row: list[str]) -> bool:
    tipo_mercados = ['010', '070', '080'] # vista, call, put
    #tipo_mercados = ['012', '013'] # exercicio call, put
    return CotacaoHistoricaReader.get_tipo_mercado(row) in tipo_mercados

def inserir_papel(empresa, codigo, tipo, especificacao):    
    query = Papel.select().where(Papel.codigo == codigo)
    if not query.exists():
        try:
            empresa = Empresa.get(Empresa.nome == empresa)
            papel = Papel.create(empresa=empresa, codigo=codigo, tipo_mercado=tipo, especificacao=especificacao)
            papel.save()
        except DoesNotExist:
            print('Empresa {} não existe'.format(empresa))


PATH = 'data/COTAHIST_A2021.TXT'
filter_unique_papel = FilterUnique(lambda r: CotacaoHistoricaReader.get_cod_papel(r))
filter = lambda r: filter_mercados(r) and filter_unique_papel(r)
reader = CotacaoHistoricaReader(PATH, filter)

rows = reader.get_rows()
for row in rows:
    tipo_mercado: str = Papel.get_tipo_mercado(CotacaoHistoricaReader.get_tipo_mercado(row))    
    inserir_papel(CotacaoHistoricaReader.get_empresa(row), CotacaoHistoricaReader.get_cod_papel(row), 
        tipo_mercado, CotacaoHistoricaReader.get_especificacao(row))