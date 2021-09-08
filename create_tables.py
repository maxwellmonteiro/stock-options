import peewee
from model.Empresa import Empresa
from model.Papel import Papel
from model.Pregao import Pregao
from model.Selic import Selic

if __name__ == '__main__':
    try:
        Empresa.create_table()
        print('Tabela "Empresa" criada com sucesso!')
        Papel.create_table()
        print('Tabela "Papel" criada com sucesso!')
        Pregao.create_table()
        print('Tabela "Pregao" criada com sucesso!')
        Selic.create_table()
        print('Tabela "Selic" criada com sucesso!')
    except peewee.OperationalError as e:
        print('Erro ao criar tabela {}'.format(e))