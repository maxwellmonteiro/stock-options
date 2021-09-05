import peewee
from model.Empresa import Empresa
from model.BaseModel import BaseModel

class Papel(BaseModel):
    id = peewee.AutoField()
    empresa = peewee.ForeignKeyField(Empresa, backref='papeis', constraint_name='fk_papel_empresa')
    codigo = peewee.CharField(unique=True, max_length=12)
    bdi = peewee.CharField(max_length=2)