from peewee import Model
from database.Database import Database

class BaseModel(Model):
    class Meta:
        database = Database.instance().get_db()
