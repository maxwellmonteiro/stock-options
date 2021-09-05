from BlackScholes import BlackScholes
from math import log
from math import sqrt
from math import exp
from math import pi

class Put(BlackScholes):

    def premio(self) -> float:
        return self.k * exp(-self.r * self.t) * self.normsdist(
            -(log(self.s / self.k) + (self.r + ((self.v ** 2) / 2)) * self.t)
            / (self.v * sqrt(self.t)) - self.v * sqrt(self.t)
        ) - self.s * self.normsdist(
            -(log(self.s / self.k) + (self.r + ((self.v ** 2) / 2)) * self.t)
            / (self.v * sqrt(self.t))
        )

    def delta(self) -> float:
        return self.normsdist(
            (log(self.s / self.k) + (self.r + ((self.v ** 2) / 2)) * self.t)
            / (self.v *sqrt(self.t))
        ) - 1

    def gamma(self) -> float:
        return (exp(-(
            (log(self.s / self.k) + (self.r + ((self.v ** 2) / 2)) * self.t)
            / (self.v * sqrt(self.t)) ** 2
        ) / 2) / sqrt(2 * pi)) / (self.s * self.v * sqrt(self.t))

    def theta(self) -> float:
        return -(
            self.s * (
                exp(-(
                    (log(self.s / self.k) + (self.r + ((self.v ** 2) / 2)) * self.t) 
                    / (self.v * sqrt(self.t)) ** 2
                ) / 2) / sqrt(2 * pi)
            ) * self.v
        ) / (2 * sqrt(self.t)) + (
            self.r * self.k *exp(-self.r * self.t) * self.normsdist(
                -(log(self.s / self.k) + (self.r + ((self.v ** 2) / 2)) * self.t)
                / (self.v *sqrt(self.t)) - self.v * sqrt(self.t)
            )
        )

    def vega(self) -> float:
        return self.s * (
            exp(-(
                (log(self.s / self.k) + (self.r + ((self.v ** 2) / 2)) * self.t)
                / (self.v * sqrt(self.t)) ** 2
            ) / 2)
            / sqrt(2 * pi)) * sqrt(self.t)

    def rho(self) -> float:
        return -self.k * self.t * exp(-self.r * self.t) * self.normsdist(
            -(log(self.s / self.k) + (self.r + ((self.v ** 2) / 2)) * self.t)
            / (self.v * sqrt(self.t)) - self.v * sqrt(self.t)
        )

put = Put(14.06, 14.00, 0.1325, 10, 0.2000)
print('Premio: ', put.premio())
print('Delta.: ', put.delta())
print('Gamma.: ', put.gamma())
print('Theta.: ', put.theta())
print('Vega..: ', put.vega())
print('Rho...: ', put.rho())
