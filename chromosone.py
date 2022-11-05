from functions import funcs

class Chromosone():
    # Genes:
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
    
    def __init__(self, f, bag_type, refund, bag_price, refund_amount, k0, k1, k2, k3, k4, k5) -> None:
        self.f = f
        self.bag_type = bag_type
        self.refund = refund
        self.bag_price = bag_price
        self.refund_amount = refund_amount
        self.k0 = k0
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.k4 = k4
        self.k5 = k5    

    def get_genes(self):
        val = []
        for _, value in vars(self).items():
            val.append(value)
        return val

    def get_order(self, day, days):
        x = day/days
        return funcs[self.f](x, self.k0, self.k1, self.k2, self.k3, self.k4, self.k5)
