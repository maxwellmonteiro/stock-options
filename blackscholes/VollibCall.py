from BlackScholes import BlackScholes
from py_vollib.black_scholes.greeks.analytical import delta, gamma, theta, vega, rho, d1, d2
from py_vollib.black_scholes import black_scholes

class VollibCall(BlackScholes):

    def _d1(self) -> float:
        return d1(self.s, self.k, self.t, self.r, self.v)

    def _d2(self) -> float:
        return d2(self.s, self.k, self.t, self.r, self.v)

    def price(self) -> float:
        return black_scholes('c', self.s, self.k, self.t, self. r, self.v)

    def delta(self) -> float:
        return delta('c', self.s, self.k, self.t, self.r, self.v)

    def gamma(self) -> float:
        return gamma('c', self.s, self.k, self.t, self.r, self.v)

    def theta(self) -> float:
        return theta('c', self.s, self.k, self.t, self.r, self.v)

    def vega(self) -> float:
        return vega('c', self.s, self.k, self.t, self.r, self.v)
    
    def rho(self) -> float:
        return rho('c', self.s, self.k, self.t, self.r, self.v)