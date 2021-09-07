from model.Pregao import Pregao
from peewee import DoesNotExist, IntegrityError
from util.CotacaoHistoricaReader import CotacaoHistoricaReader as chr
from util.Filter import Filter
from model.Papel import Papel

def inserir_pregao(cod_papel, data, preco_fechamento, negocios, preco_exercicio, data_vencimento):    
    try:
        papel = Papel.get(Papel.codigo == cod_papel)
        pregao = Pregao.create(papel=papel, data=data, preco_fechamento=preco_fechamento, 
            negocios=negocios, preco_exercicio=preco_exercicio, data_vencimento=data_vencimento
        )
        pregao.save()
    except DoesNotExist:
        print('Papel {} não existe'.format(papel))
    except IntegrityError:
        # pregao already exists, do nothing
        pass

PATH = 'data/COTAHIST_A2021.TXT'
filter = lambda r: Filter.filter_mercados(r) and Filter.filter_fii(r) and Filter.filter_empresa(r)
reader = chr(PATH, filter)

rows = reader.get_rows()
for row in rows:    
    inserir_pregao(chr.get_cod_papel(row), chr.get_data_pregao(row), chr.get_preco_fechamento(row), 
        chr.get_negocios(row), chr.get_preco_exercicio(row), chr.get_data_vencimento(row)
    )