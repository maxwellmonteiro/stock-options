from peewee import DoesNotExist, IntegrityError
from model.Empresa import Empresa
from util.FilterUnique import FilterUnique
from util.CotacaoHistoricaReader import CotacaoHistoricaReader
from model.Papel import Papel
import re

def filter_mercados(row: list[str]) -> bool:
    tipo_mercados = ['010', '070', '080'] # vista, call, put
    #tipo_mercados = ['012', '013'] # exercicio call, put
    return CotacaoHistoricaReader.get_tipo_mercado(row) in tipo_mercados

def filter_fii(row: list[str]) -> bool:
    empresa = CotacaoHistoricaReader.get_empresa(row)
    return empresa[0:4] != 'FII '

def filter_liquidez(row: list[str]) -> bool:
    return CotacaoHistoricaReader.get_negocios(row) > 100

def filter_empresa(row: list[str]) -> bool:
    empresas = ['PETROBRAS', 'PETR', 'PETRE']
    return CotacaoHistoricaReader.get_empresa(row) in empresas

def inserir_papel(empresa, codigo, tipo, especificacao):    
    try:
        empresa = Empresa.get(Empresa.nome == empresa)
        papel = Papel.create(empresa=empresa, codigo=codigo, tipo_mercado=tipo, especificacao=especificacao)
        papel.save()
    except DoesNotExist:
        print('Empresa {} não existe'.format(empresa))
    except IntegrityError:
        # papel already exists, do nothing
        None

PATH = 'data/COTAHIST_A2021.TXT'
filter_unique_papel = FilterUnique(lambda r: CotacaoHistoricaReader.get_cod_papel(r))
filter = lambda r: filter_mercados(r) and filter_fii(r) and filter_empresa(r) and filter_unique_papel(r)
reader = CotacaoHistoricaReader(PATH, filter)

rows = reader.get_rows()
for row in rows:
    tipo_mercado: str = Papel.get_tipo_mercado(CotacaoHistoricaReader.get_tipo_mercado(row))    
    inserir_papel(CotacaoHistoricaReader.get_empresa(row), CotacaoHistoricaReader.get_cod_papel(row), 
        tipo_mercado, CotacaoHistoricaReader.get_especificacao(row))