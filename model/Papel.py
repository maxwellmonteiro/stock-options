import peewee
from model.Empresa import Empresa
from model.BaseModel import BaseModel

class Papel(BaseModel):
    VISTA = 'Vista'
    CALL = 'Call'
    PUT = 'Put'

    id = peewee.AutoField()
    empresa = peewee.ForeignKeyField(Empresa, backref='papeis', constraint_name='fk_papel_empresa')
    codigo = peewee.CharField(unique=True, max_length=12)
    tipo_mercado = peewee.CharField(max_length=10)
    especificacao = peewee.CharField(max_length=4)

    @classmethod
    def get_tipo_mercado(cls, cod: str):
        if cod == '010':
            return Papel.VISTA
        elif cod == '070':
            return Papel.CALL
        elif cod == '080':
            return Papel.PUT
