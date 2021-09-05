from util.CotacaoHistoricaReader import CotacaoHistoricaReader

class FilterUniqueEmpresa:
    empresas: dict[str, str] = dict()
    def __call__(self, row: list[str]) -> bool:
        empresa = CotacaoHistoricaReader.get_empresa(row)
        if empresa in self.empresas:
            return False
        else:
            self.empresas[empresa] = empresa
            return True

def filter_mercado_vista(row: list[str]) -> bool:
    return CotacaoHistoricaReader.get_tipo_mercado(row) == '010'

PATH = 'data/COTAHIST_A2021.TXT'
filter_unique_empresa = FilterUniqueEmpresa()
filter = lambda r: filter_unique_empresa(r) and filter_mercado_vista(r)
reader = CotacaoHistoricaReader(PATH, filter)

rows = reader.get_rows()
for row in rows:
    print(CotacaoHistoricaReader.get_empresa(row))
