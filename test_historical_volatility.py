from array import array
from model.Papel import Papel
from model.Pregao import Pregao
from blackscholes.HistoricalVolatility import HistoricalVolatility

quotes: array = array('f', [])
query = Pregao.select(Pregao.preco_fechamento).join(Papel).where(Papel.codigo == 'VALE3').order_by(Pregao.data)
for row in query:
    quotes.append(row.preco_fechamento)
hv = HistoricalVolatility(quotes)
print(hv.calc())
hv.add_quote(26.46)
print(hv.calc())
