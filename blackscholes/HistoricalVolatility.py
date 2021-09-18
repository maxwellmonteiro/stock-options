import math
from array import array
from scipy import stats

class HistoricalVolatility:

    DAYS = 252

    def __init__(self, quotes: array):
        self._quotes = quotes
        self._ln_ratios: array = array('f', [])
        previous: float = None
        for s in quotes:
            if (previous != None):
                self.ln_ratios.append(math.log(s / previous))
            previous = s
    @property
    def quotes(self):
        return self._quotes

    def add_quote(self, quote: float):        
        length = len(self._quotes)
        previous = self._quotes[length - 1] if length > 0 else None
        if previous != None:
            self._ln_ratios.append(math.log(quote / previous))
        self._quotes.append(quote)
        if length > HistoricalVolatility.DAYS:
            self._quotes.pop(0)

    def calc(self):
        if len(self._ln_ratios) > 0:
            return stats.tstd(self._ln_ratios) * math.sqrt(HistoricalVolatility.DAYS)
        return None


