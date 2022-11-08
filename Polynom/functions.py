import math

function_vars = [
    [0, 1000],      [0, 1000],      [-10000, 0],   [0, 10],                                     # f0
    [0, 1000],      [0, 1000],      [-10000, 0],   [0, 10],     [0, 10],                        # f1
    [-100, 100],    [-100, 100],    [-100, 100],   [0, 100],    [0, 6.3],       [0, 100],       # f2 is good
    [0, 10],        [0, 10],        [-1000, 1000], [0, 10],     [0, 10],        [-1000, 1000],  # f3 is good
    [0, 1000],      [-1000, 1000],  [0, 3.15],     [0, 500],                                    # f4 
    [0, 1000],      [-1000, 1000],  [0, 3.15],     [0, 500],    [-1000, 1000],  [-1000, 1000],   # f5 is good
    [-20,0], [50, 500] , [-50,0] , [0, 200], [0.5, 20], [0, 10], [0.1, 50], [-math.pi, math.pi] #manual func
]

func_param_dict = dict(manual_function1 = [[-20,0], [50, 500] , [-50,0] , [0, 200]],
                       manual_function2 = [[-20,0], [50, 500] , [-50,0] , [0, 200], [0.5, 20], [0, 10], [0.1, 50], [-math.pi, math.pi]] )
mutation_values_dict = dict(manual_function1 = dict(k = [0.005, 0.05, 0.1, 0.01],
                                                    bag_price = 0.05,
                                                    refund_amount = 0.05,
                                                    bag_type = 0,
                                                    refund = 0
                                                    ),
                            manual_function2 = dict(k = [0.005, 0.05, 0.1, 0.01, 0.1, 0.1, 0.1, 0.1],
                                                    bag_price = 0.05,
                                                    refund_amount = 0.05,
                                                    bag_type = 0,
                                                    refund = 0
                                                    ))

def function(x, k):
    _, val = manual_function1(x,k)
    return int(val)
    order = 0
    for func in funcs:
        k, val = func(x, k)
        order += max(-1000000, min(1000000, val))
    return max(0, int(order))

def func0(x, k):
    num_k = 4
    k, res = k[0:num_k], k[num_k:]
    return res, (k[0] + k[1]*x + k[2]*x**2) * math.cos(k[3]*x)

def func1(x, k):    
    num_k = 5
    k, res = k[0:num_k], k[num_k:]
    return res, (k[0] + k[1]*x + k[2]*x**2) * math.cos(k[3]*x + k[4])

def func2(x, k):
    num_k = 6
    k, res = k[0:num_k], k[num_k:]
    return res, (1 + k[0]*x + k[1]*x**2 + k[2]*x**3) * k[5] * math.cos(k[3]*x + k[4])

def func3(x, k):
    num_k = 6
    k, res = k[0:num_k], k[num_k:]
    return res, k[0] * math.cos(k[1]*x + k[2]) + k[5] * math.cos(k[3]*x + k[4])

def func4(x, k):
    num_k = 4
    k, res = k[0:num_k], k[num_k:]
    return res, min(k[0], k[1]*math.tan(k[2]*x + k[3]))

def func5(x, k):
    num_k = 6
    k, res = k[0:num_k], k[num_k:]
    return res, min(k[0] + k[4]*x + k[5]*x**2, max(0, k[1]*math.tan(k[2]*x + k[3])))

def func5(x, k):
    num_k = 6
    k, res = k[0:num_k], k[num_k:]
    return res, min(k[0] + k[4]*math.cos(k[5]*x), max(0, k[1]*math.tan(k[2]*x + k[3])))


def manual_function1(x, k):
    num_k = 4
    k, res = k[0:num_k], k[num_k:]
    return res, max(0,min(
        (k[0]*k[1]*x) % k[1], 
        max(0, k[2]*math.tan(k[3]*x + math.pi/2))
        ))

def manual_function2(x, k):
    num_k = 8
    k, res = k[0:num_k], k[num_k:]
    return res, max(0,min(
        (k[0]*k[1]*x) % k[1], 
        max(0, k[2]*math.tan(k[3]*x + math.pi/2))
        )*(k[4]+k[5]*math.cos(k[6]*x + k[7]))) 

funcs = [func0, func1, func2, func3, func4, func5]