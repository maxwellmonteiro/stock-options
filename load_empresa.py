from util.CotacaoHistoricaReader import CotacaoHistoricaReader
from model.Empresa import Empresa

class FilterUniqueEmpresa:
    empresas: dict[str, str] = dict()
    def __call__(self, row: list[str]) -> bool:
        empresa = CotacaoHistoricaReader.get_empresa(row)
        if empresa in self.empresas:
            return False
        else:
            self.empresas[empresa] = empresa
            return True

def filter_mercados(row: list[str]) -> bool:
    tipo_mercados = ['010', '070', '080'] # vista, call, put
    return CotacaoHistoricaReader.get_tipo_mercado(row) in tipo_mercados

def inserir_empresa(nome):
    query = Empresa.select().where(Empresa.nome == nome)
    if not query.exists():
        empresa = Empresa.create(nome=nome)

PATH = 'data/COTAHIST_A2021.TXT'
filter_unique_empresa = FilterUniqueEmpresa()
filter = lambda r: filter_mercados(r) and filter_unique_empresa(r)
reader = CotacaoHistoricaReader(PATH, filter)

rows = reader.get_rows()
for row in rows:    
    print(CotacaoHistoricaReader.get_empresa(row))
