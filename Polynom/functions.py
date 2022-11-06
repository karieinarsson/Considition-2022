import math

f_vars = [
    [[0, 1000], [0, 1000], [-10000, 0],   [0, 10],    [0, 0],   [0, 0]],
    [[0, 1000], [0, 1000], [-10000, 0],   [0, 10],    [0, 10],  [0, 0]],
    [[-100, 100], [-100, 100], [-100, 100],     [0, 100],   [0, 6.3], [0, 100]],
    [[0, 10],   [0, 10],   [-1000, 1000], [0, 10],    [0, 10],  [-1000, 1000]],
    [[0, 1000], [-1000, 1000], [0, 3.15],   [0, 500],     [0, 0],   [0, 0]],
    [[0, 1000], [-1000, 1000], [0, 3.15],   [0, 500],     [-1000, 1000],   [-1000, 1000]]
]

def func0(x, k0, k1, k2, k3, k4, k5):
    return int(max(0, (k0 + k1*x + k2*x**2) * math.cos(k3*x)))

def func1(x, k0, k1, k2, k3, k4, k5):
    return int(max(0, (k0 + k1*x + k2*x**2) * math.cos(k3*x + k4)))

def func2(x, k0, k1, k2, k3, k4, k5):
    return int(max(0, (1 + k0*x + k1*x**2 + k2*x**3) * k5 * math.cos(k3*x + k4)))

def func3(x, k0, k1, k2, k3, k4, k5):
    return int(max(0, k0 * math.cos(k1*x + k2) + k5 * math.cos(k3*x + k4)))

def func4(x, k0, k1, k2, k3, k4, k5):
    return int(max(0, min(k0, k1*math.tan(k2*x + k3))))

def func5(x, k0, k1, k2, k3, k4, k5):
    return int(max(0,min(k0 + k4*x + k5*x**2, max(0, k1*math.tan(k2*x + k3)))))

funcs = [func0, func1, func2, func3, func4, func5]