from blackscholes.Call import Call
from blackscholes.VollibCall import VollibCall

# s, k, r, dias, v = 14.06, 14.00, 0.1325, 10, 0.2000
s, k, r, dias, v = 27.34, 26.25, 0.02, 31, 0.4803

call = Call(s, k, r, dias, v)
print('Price: ', call.price())
print('d1: ', call.d1())
print('d2: ', call.d2())
print('Delta.: ', call.delta())
print('Gamma.: ', call.gamma())
print('Theta.: ', call.theta())
print('Vega..: ', call.vega())
print('Rho...: ', call.rho())
print('')

call = VollibCall(s, k, r, dias, v)
print('Price: ', call.price())
print('d1: ', call.d1())
print('d2: ', call.d2())
print('Delta.: ', call.delta())
print('Gamma.: ', call.gamma())
print('Theta.: ', call.theta())
print('Vega..: ', call.vega())
print('Rho...: ', call.rho())
print('')

