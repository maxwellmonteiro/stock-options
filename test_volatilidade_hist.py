from util.CotacaoHistoricaReader import CotacaoHistoricaReader

PATH = 'data/COTAHIST_A2021.TXT'

filter = lambda r: CotacaoHistoricaReader.get_cod_papel(r) == 'PETR4'
reader = CotacaoHistoricaReader(PATH, filter)

rows = reader.get_rows()
for row in rows:
    print(row)