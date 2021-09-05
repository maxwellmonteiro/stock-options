from scipy import stats
from math import log
from math import sqrt

class BlackScholes:
    __QTD_DIAS_ANO = 252

    def __init__(self, s, k, r, dias, v):
        self.s = s # preco acao
        self.k = k # strike opcao
        self.r = r # taxa juros livre de risco
        self.t = dias / BlackScholes.__QTD_DIAS_ANO # tempo proporcional a 252 ou 365
        self.v = v # volatilidade
        self.__d1 = self._d1()
        self.__d2 = self._d2()

    def _d1(self) -> float:
        sigma_square = self.v * self.v
        n = log(self.s / self.k) + (self.r + sigma_square / 2.0) * self.t
        d = self.v * sqrt(self.t)
        return n / d

    def _d2(self) -> float:
        return self.d1() - self.v * sqrt(self.t)

    # standard normal cumulative distribution
    def cdf(self, v: float) -> float:
        return stats.norm.cdf(v)

    # standard normal probability density function
    def pdf(self, v: float) -> float:
        return stats.norm.pdf(v)

    def d1(self) -> float:
        return self.__d1

    def d2(self) -> float:
        return self.__d2

    def price(self) -> float:
        pass

    def premio(self) -> float:
        pass

    def delta(self) -> float:
        pass

    def gamma(self) -> float:
        pass

    def theta(self) -> float:
        pass

    def vega(self) -> float:
        pass

    def rho(self) -> float:
        pass