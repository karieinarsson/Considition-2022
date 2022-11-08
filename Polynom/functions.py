import math

#För fancyville (31dagar, 10 population) körde vi:
#   k0 = [-20,0], k1=[50,500], k2=[-50,0], k3 = [0,200]

#k1 ish upp till  2000
#k0 är bra
#k2 är bra
# k3 0:500
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
    return int(manual_function1(x,k))

def manual_function1(x, k):
    return max(0,min(
        (k[0]*k[1]*x) % k[1], 
        max(0, k[2]*math.tan(k[3]*x + math.pi/2))
        ))

def manual_function2(x, k):
    return max(0,min(
        (k[0]*k[1]*x) % k[1], 
        max(0, k[2]*math.tan(k[3]*x + math.pi/2))
        )*(k[4]+k[5]*math.cos(k[6]*x + k[7]))) 