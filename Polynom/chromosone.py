from functions import funcs, f_vars
from random import randint, uniform

bag_type_cost = [0, 1.7, 1.75, 6, 25, 200]
init_chrom = dict(
    bag_type = randint(1,4),
    refund = randint(0,1),
    bag_price = lambda bag_type: uniform(bag_type_cost[bag_type], bag_type_cost[bag_type]*10),
    refund_amount = lambda bag_price: uniform(0, bag_price),
    k0 = lambda f: uniform(f_vars[f][0][0], f_vars[f][0][1]),
    k1 = lambda f: uniform(f_vars[f][1][0], f_vars[f][1][1]),
    k2 = lambda f: uniform(f_vars[f][2][0], f_vars[f][2][1]),
    k3 = lambda f: uniform(f_vars[f][3][0], f_vars[f][3][1]),
    k4 = lambda f: uniform(f_vars[f][4][0], f_vars[f][4][1]),
    k5 = lambda f: uniform(f_vars[f][5][0], f_vars[f][5][1])
)


class Chromosone():
    # Genes:
    function: int
    bag_type: int # Value from 0 to 4, selects which bag to use
    refund: bool # Decides which refund policy to use
    bag_price: float # Value from 0 to inf, price of the bag (not cost)
    refund_amount: float # Value from 0 to inf

    k0: float
    k1: float
    k2: float
    k3: float
    k4: float
    k5: float
    
    def __init__(self, function , bag_type=None, refund=None, bag_price=None, refund_amount=None, k0=None, k1=None, k2=None, k3=None, k4=None, k5=None) -> None:
        self.function = function
        if bag_type is None:
            self.bag_type = init_chrom["bag_type"]
        else:
            self.bag_type = bag_type
        if refund is None:
            self.refund = init_chrom["refund"]
        else:
            self.refund = refund
        if bag_price is None:
            self.bag_price = init_chrom["bag_price"](self.bag_type)
        else:
            self.bag_price = bag_price
        if refund_amount is None:
            self.refund_amount = init_chrom["refund_amount"](self.bag_price)
        else:
            self.refund_amount = refund_amount
        if k0 is None:
            self.k0 = init_chrom["k0"](function)
        else:
            self.k0 = k0
        if k1 is None:
            self.k1 = init_chrom["k1"](function)
        else:
            self.k1 = k1
        if k2 is None:
            self.k2 = init_chrom["k2"](function)
        else:
            self.k2 = k2
        if k3 is None:
            self.k3 = init_chrom["k3"](function)
        else:
            self.k3 = k3
        if k4 is None:
            self.k4 = init_chrom["k4"](function)
        else:
            self.k4 = k4
        if k5 is None:
            self.k5 = init_chrom["k5"](function)
        else:
            self.k5 = k5

    def get_genes(self):
        val = []
        for _, value in vars(self).items():
            val.append(value)
        return val

    def get_order(self, day, days):
        x = day/days
        return funcs[self.function](x, self.k0, self.k1, self.k2, self.k3, self.k4, self.k5)
    