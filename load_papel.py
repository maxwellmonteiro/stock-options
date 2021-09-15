import sys
from peewee import DoesNotExist, IntegrityError
from util.CotacaoHistoricaReader import CotacaoHistoricaReader as chr
from util.Filter import Filter
from model.Empresa import Empresa
from model.Papel import Papel

def inserir_papel(empresa, codigo, tipo, especificacao):    
    try:
        empresa = Empresa.get(Empresa.nome == empresa)
        papel = Papel.create(empresa=empresa, codigo=codigo, tipo_mercado=tipo, especificacao=especificacao)
        papel.save()
    except DoesNotExist:
        print('Empresa {} não existe'.format(empresa))
    except IntegrityError:
        # papel already exists, do nothing
        pass

PATH = sys.argv[1] #'data/COTAHIST_A2020.TXT'
print('PATH: {}'.format(PATH))
filter_unique_papel = Filter.filter_unique(lambda r: chr.get_cod_papel(r))
filter = lambda r: Filter.filter_mercados(r) and Filter.filter_fii(r) and Filter.filter_empresa(r) and filter_unique_papel(r)
reader = chr(PATH, filter)

rows = reader.get_rows()
for row in rows:
    tipo_mercado: str = Papel.get_tipo_mercado(chr.get_tipo_mercado(row))    
    inserir_papel(chr.get_empresa(row), chr.get_cod_papel(row), 
        tipo_mercado, chr.get_especificacao(row))