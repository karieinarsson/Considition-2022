from functions import function, func_param_dict, mutation_values_dict
from random import randint, uniform
from typing import List

bag_type_cost = [0, 1.7, 1.75, 6, 25, 200]

mutation_rate = 1/8

init_chrom = dict(
    bag_type        = randint(1,4),
    refund          = randint(0,1),
    bag_price       = lambda bag_type: uniform(bag_type_cost[bag_type], bag_type_cost[bag_type]*10),
    refund_amount   = lambda bag_price: uniform(0, bag_price),
    k               = lambda n_k: [uniform(func_param_dict["manual_function1"][k][0], func_param_dict["manual_function1"][k][1]) for k in range(n_k)]
)

mutate_chrom = dict(
    bag_type      = lambda bag_type, mutation_val: randint(1,5) if uniform(0,1) < mutation_rate else bag_type,
    refund        = lambda refund, mutation_val: abs(refund-1) if uniform(0,1) < mutation_rate else refund,
    bag_price     = lambda bag_price, mutation_val: uniform(1-mutation_val, 1+mutation_val) * bag_price if uniform(0,1) < mutation_rate else bag_price,
    refund_amount = lambda refund_amount, mutation_val: uniform(1-mutation_val, 1+mutation_val) * refund_amount if uniform(0,1) < mutation_rate else refund_amount,

    k             = lambda ks, mutation_val: [uniform(1-mutation_val*mutation_values_dict["manual_function1"]["k"][i], 1+mutation_val*mutation_values_dict["manual_function1"]["k"][i]) * k 
                                                if uniform(0,1) < mutation_rate else k for i, k in enumerate(ks)]
        )

class Chromosone():
    # Genes:
    function: int
    bag_type: int # Value from 0 to 4, selects which bag to use
    refund: bool # Decides which refund policy to use
    bag_price: float # Value from 0 to inf, price of the bag (not cost)
    refund_amount: float # Value from 0 to inf
    k: List[float]
    
    def __init__(self, bag_type=None, refund=None, bag_price=None, refund_amount=None, k=None) -> None:
        self.bag_type = init_chrom["bag_type"] if bag_type is None else bag_type
        self.refund = init_chrom["refund"] if refund is None else refund
        self.bag_price = init_chrom["bag_price"](self.bag_type) if bag_price is None else bag_price
        self.refund_amount = init_chrom["refund_amount"](self.bag_price) if refund_amount is None else refund_amount
        self.k = init_chrom["k"](len(func_param_dict["manual_function1"])) if k is None else k

    def mutate(self, mutation_val=0.05):
        for gene, value in vars(self).items():
            if gene == "k":
                self.__dict__[gene] = mutate_chrom[gene](value, mutation_val)
                continue
            self.__dict__[gene] = mutate_chrom[gene](value, mutation_val*mutation_values_dict["manual_function1"][gene])

    def random_mutate(self):
        if uniform(0, 1) < mutation_rate:
            self.bag_type = init_chrom["bag_type"]
        if uniform(0, 1) < mutation_rate:
            self.refund = init_chrom["refund"]
        if uniform(0, 1) < mutation_rate:
            self.bag_price = init_chrom["bag_price"](self.bag_type)
        if uniform(0, 1) < mutation_rate:
            self.refund_amount = init_chrom["refund_amount"](self.bag_price)
        if uniform(0, 1) < mutation_rate:
            self.k = init_chrom["k"](len(func_param_dict["manual_function1"]))
        

    def get_genes(self):
        val = []
        for _, value in vars(self).items():
            val.append(value)
        return val

    def get_order(self, day, days):
        x = day/days
        return function(x, self.k)
    