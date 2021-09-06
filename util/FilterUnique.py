
class FilterUnique:
    registros: dict[str, str] = dict()

    def __init__(self, get_key: lambda: str):
        self._get_key = get_key

    def __call__(self, row: list[str]) -> bool:
        registro = self._get_key(row)
        if registro in self.registros:
            return False
        else:
            self.registros[registro] = registro
            return True
