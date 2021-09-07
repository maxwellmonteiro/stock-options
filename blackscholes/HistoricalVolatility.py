import math
from array import array
from scipy import stats

class HistoricalVolatility:

    def __init__(self, quotes: array):
        self.quotes = quotes
        self.ln_ratios: array = array('f', [])
        previous: float = None
        for s in quotes:
            if (previous != None):
                self.ln_ratios.append(math.log(s / previous))
            previous = s

    def add_quote(self, quote: float):        
        length = len(self.quotes)
        previous = self.quotes[length - 1] if length > 0 else None
        if previous != None:
            self.ln_ratios.append(math.log(quote / previous))
        self.quotes.append(quote)

    def calc(self):
        if len(self.ln_ratios) > 0:
            return stats.tstd(self.ln_ratios) * math.sqrt(252)
        return None


