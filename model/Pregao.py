from enum import unique
import peewee
from model.Papel import Papel
from model.BaseModel import BaseModel

class Pregao(BaseModel):

    id = peewee.AutoField()
    papel: Papel = peewee.ForeignKeyField(Papel, backref='pregoes', constraint_name='fk_pregao_papel')
    data = peewee.DateField()
    preco_fechamento = peewee.FloatField()
    negocios = peewee.IntegerField()
    preco_exercicio = peewee.FloatField()
    data_vencimento = peewee.DateField()

    class Meta:
        indexes = (
            (('papel', 'data'), True),
        )