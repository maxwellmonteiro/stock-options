from enum import unique
import peewee
from model.BaseModel import BaseModel

class Selic(BaseModel):
    id = peewee.AutoField()
    data = peewee.DateField(unique=True)
    valor = peewee.FloatField()