
import peewee
from model.BaseModel import BaseModel

class Empresa(BaseModel):
    id = peewee.AutoField()
    nome = peewee.CharField(unique=True, max_length=12)

