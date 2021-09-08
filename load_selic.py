import urllib
import json
from urllib import request
from peewee import IntegrityError, fn
from datetime import date, datetime, timedelta
from model.Selic import Selic

def inserir_selic(data: date, valor: float):
    try:
        selic = Selic.create(data=data, valor=valor)
        selic.save()
    except IntegrityError:
        pass

DEFAULT_DATA_INI = '01/01/2009'
COD_SELIC_ANUALIZADA = 1178
BCB_URL = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados?formato=json&dataInicial={data_ini}&dataFinal={data_fim}'

max_data: date = Selic.select(fn.MAX(Selic.data)).scalar()
data_ini: date = datetime.strptime(DEFAULT_DATA_INI, '%d/%m/%Y').date()
if max_data != None:
    data_ini = max_data + timedelta(days=1)    
data_fim = date.today()

url = BCB_URL.format(cod=COD_SELIC_ANUALIZADA, data_ini=data_ini.strftime('%d/%m/%Y'), data_fim=data_fim.strftime('%d/%m/%Y'))
response = request.urlopen(url)
json = json.loads(response.read())

for row in json:
    data: date = datetime.strptime(row['data'], '%d/%m/%Y').date()
    valor: float = round(float(row['valor']) * 0.01, 4)
    inserir_selic(data, valor)