from BlackScholes import BlackScholes
from math import log
from math import sqrt
from math import exp
from math import pi


class Call(BlackScholes):

    def delta(self) -> float:
        return self.cdf(self.d1())

    def gamma(self) -> float:
        return self.pdf(self.d1()) / (self.s * self.v * sqrt(self.t))

    def theta(self) -> float:
        n = self.s * self.pdf(self.d1()) * self.v
        d = 2.0 * sqrt(self.t)
        termo_1 = -1 * (n / d)
        termo_2 = (self.r * self.k * exp(-self.r * self.t)) * self.cdf(self.d2())
        return (termo_1 - termo_2) / 365.0

    def vega(self) -> float:
        return (self.s * self.pdf(self.d1()) * sqrt(self.t)) * 0.01

    def rho(self) -> float:
        return (self.k * self.t * exp(-self.r * self.t) * self.cdf(self.d2())) * 0.01
