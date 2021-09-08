from peewee import fn
from array import array
from datetime import date
from blackscholes.VollibCall import VollibCall
from model.Papel import Papel
from model.Pregao import Pregao
from model.Selic import Selic
from blackscholes.HistoricalVolatility import HistoricalVolatility

max_data: date = Selic.select(fn.MAX(Selic.data)).scalar()
selic: Selic = Selic.get(Selic.data == max_data)
quotes: array = array('f', [])
query = Pregao.select(Pregao.preco_fechamento).join(Papel).where(Papel.codigo == 'PETR4').order_by(Pregao.data)
for row in query:
    quotes.append(row.preco_fechamento)
hv = HistoricalVolatility(quotes)
print('Volatilidade Historica: {}'.format(hv.calc()))
call = VollibCall(26.46, 26.10, selic.valor, 11, hv.calc())
print('PETRI278: price = {} delta = {} gamma = {} theta = {}'.format(call.price(), call.delta(), call.gamma(), call.theta()))

