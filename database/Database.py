from util.Singleton import Singleton
import peewee

@Singleton
class Database:
    _USER = 'bolsa'
    _PASSWD = '123456'
    _HOST = 'localhost'
    _DB = 'bolsa'

    def __init__(self):
        self._db = peewee.MySQLDatabase(
            self._DB, 
            user=self._USER, 
            password=self._PASSWD, 
            host=self._HOST, 
            port=3306
        )
        pass

    def get_db(self):
        return self._db

