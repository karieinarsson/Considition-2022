from random import randint, uniform
import torch as th
import torch.nn as nn

bag_type_co2_production = [0, 3, 2.4, 3.6, 4.2, 6]
bag_type_co2_transport = [0, 3, 4.2, 1.8, 3.6, 12]
bag_type_resuable = [0, 0, 1, 5, 9, 12]
bag_type_wash_time = [0, 1, 2, 3, 5, 7]
bag_type_cost = [0, 1.7, 1.75, 6, 25, 200]

mutation_rate = 0.3
fine_mutation_rate = 0.5

init_chrom = dict(
    bag_type = randint(1,5),
    refund = randint(0,1),
    bag_price = lambda bag_type: uniform(bag_type_cost[bag_type], bag_type_cost[bag_type]*10),
    refund_amount = lambda bag_price: uniform(0, bag_price)
)

mutate_chrom = dict(
    bag_type = randint(1,5),
    refund = lambda refund: abs(refund-1),
    bag_price = lambda bag_price: uniform(0.95, 1.05) * bag_price,
    model = lambda v: uniform(0.95, 1.05) * v if uniform(0,1) < fine_mutation_rate else uniform(0,2),
    refund_amount = lambda refund_amount: uniform(0.95, 1.05) * refund_amount
)

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.nn = nn.Sequential(
            nn.Linear(5, 20),
            nn.ReLU(),
            nn.Linear(20, 10),
            nn.ReLU(),
            nn.Linear(10, 1),
            nn.ReLU()
        )

        def init_weights(m):
            if type(m) == nn.Linear:
                th.nn.init.uniform_(m.weight, a=-2, b=2.0)

        self.nn.apply(init_weights)


    def forward(self, x):
        return self.nn(x)


class Chromosone():
    # Genes:
    bag_type: int # Value from 0 to 4, selects which bag to use
    refund: bool # Decides which refund policy to use
    bag_price: float # Value from 0 to inf, price of the bag (not cost)
    refund_amount: float # Value from 0 to inf
    model: Model
    
    def __init__(self, bag_type=None, refund=None, bag_price=None, refund_amount=None, model=None, weights=None) -> None:
        self.bag_type = init_chrom["bag_type"] if bag_type is None else bag_type
        self.refund = init_chrom["refund"] if refund is None else refund
        self.bag_price = init_chrom["bag_price"](self.bag_type) if bag_price is None else bag_price
        self.refund_amount = init_chrom["refund_amount"](self.bag_price) if refund_amount is None else refund_amount
        self.model = Model() if model is None else model
        self.weights = self.get_params() if weights is None else weights

    def mutate(self):
        for gene, value in vars(self).items():
            if uniform(0,1) > mutation_rate:
                continue
            if gene == "bag_type":
                self.bag_type = mutate_chrom[gene]
            elif gene == "refund":
                self.refund = mutate_chrom[gene](value)
            elif gene == "bag_price":
                self.bag_price = mutate_chrom[gene](value)
            elif gene == "refund_amount":
                self.refund_amount = mutate_chrom[gene](value)
            elif gene == "model":
                params = []
                for w in self.get_params():
                    if uniform(0,1) > mutation_rate:
                        params.append(w)
                    else:
                        params.append(mutate_chrom[gene](w))
                self.set_params(params)
                    

    def get_genes(self):
        val = []
        for gene, value in vars(self).items():
            if gene != "model" and gene != "weights":
                val.append(value)
        return val

    def get_params(self):
        params = []
        with th.no_grad():  
                for idx, param in enumerate(self.model.parameters()):
                    if idx % 2 == 0:
                        params.append(param.data.flatten())
        return [float(i) for i in th.cat(params)]
        
    @th.no_grad()
    def _set_weights(self, m):
        if type(m) == nn.Linear:
            shape = m.weight.data.shape
            new_data = []
            for _ in m.weight.data.flatten():
                new_data.append(self.weights.pop())
            m.weight.data = th.tensor(new_data, dtype=float).reshape(shape)

    
    def set_params(self, w):
        self.weights = w
        self.model.nn.apply(self._set_weights)
        self.model.nn = self.model.nn.float()

    def get_order(self, day, _):
        order = int(self.model.forward(th.tensor([
                    self.bag_type,
                    #bag_type_co2_production[self.bag_type],
                    #bag_type_co2_transport[self.bag_type],
                    #bag_type_resuable[self.bag_type],
                    #bag_type_wash_time[self.bag_type],
                    self.refund, 
                    self.bag_price, 
                    self.refund_amount, 
                    day
                ])))
        return order
    