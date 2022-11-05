import math

f_vars = [
    [[0, 1000], [0, 1000], [-10000, 0],   [0, 10],    [0, 0],   [0, 0]],
    [[0, 1000], [0, 1000], [-10000, 0],   [0, 10],    [0, 10],  [0, 0]],
    [[-100, 100], [-100, 100], [-100, 100],     [0, 100],   [0, 6.3], [0, 100]],
    [[0, 10],   [0, 10],   [-1000, 1000], [0, 10],    [0, 10],  [-1000, 1000]],
    [[0, 1000], [0, 1000], [-10000, 0],   [0, 0],     [0, 0],   [0, 0]],
    [[0, 1000], [0, 1000], [-10000, 0],   [0, 10000], [0, 0],   [0, 0]]
]

def poly_cos0(x, k0, k1, k2, k3, k4, k5):
    return int(max(0, (k0 + k1*x + k2*x**2) * math.cos(k3*x)))

def poly_cos1(x, k0, k1, k2, k3, k4, k5):
    return int(max(0, (k0 + k1*x + k2*x**2) * math.cos(k3*x + k4)))

def poly_cos2(x, k0, k1, k2, k3, k4, k5):
    return int(max(0, (1 + k0*x + k1*x**2 + k2*x**3) * k5 * math.cos(k3*x + k4)))

def poly_cos3(x, k0, k1, k2, k3, k4, k5):
    return int(max(0, k0 * math.cos(k1*x + k2) + k5 * math.cos(k3*x + k4)))

def poly_pow2(x, k0, k1, k2, k3, k4, k5):
    return int(max(0, k0 + k1*x + k2*x**2))

def poly_pow3(x, k0, k1, k2, k3, k4, k5):
    return int(max(0, k0 + k1*x + k2*x**2 + k3*x**3))

funcs = [poly_cos0, poly_cos1, poly_cos2, poly_cos3, poly_pow2, poly_pow3]