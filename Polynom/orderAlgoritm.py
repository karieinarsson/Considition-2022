from solution import Solution
from collections import namedtuple
from random import randint, uniform
from multiprocessing import Pool

import queue
import api

Chrom = namedtuple('Chrom', 'array fitness')
ChromosoneTuple = namedtuple('ChromosoneTuple', 'chromosone fitness')

class OA:
    def __init__(self, map_name) -> None:
        self.api_key = "97b8ff47-ad44-4018-645e-08dabbf9e85f"
        self.map_name = map_name
        self.response = api.map_info(self.api_key, self.map_name)
        self.days = 31 if self.map_name == "Suburbia" or self.map_name == "Fancyville" else 365

# -------------------------------------------------------------------------
# -------------------------Fit function------------------------------------
# -------------------------------------------------------------------------

    def fit(self, c, population_size=60, generations=50, mutation_rate=0.5, verbose=1):
        self.mutation_rate = mutation_rate

        best_orders = [c.chromosone.get_order(day, self.days) for day in range(self.days)]

        solution = Solution(recycle_refund_choice = c.chromosone.refund,
                                bag_price = c.chromosone.bag_price, 
                                refund_amount = c.chromosone.refund_amount,
                                bag_type = c.chromosone.bag_type)
        solution.add_map_name(self.map_name)

        population = [best_orders] + [self.mutate(best_orders) for _ in range(population_size-1)]
        population = self.get_fitness(population, solution)

        q = queue.Queue(5)

        for gen in range(generations):
            population = [population[0].array] + [self.mutate(population[0].array) for _ in range(population_size-1)]
            population = self.get_fitness(population, solution)
            if verbose:
                print(f"Top score for generation {gen} is {population[0].fitness}")

            if q.full() and q.get() == population[0].fitness: return population[0]
            q.put(population[0].fitness)
        
        solution.orders = population[0].array
        return solution, population[0].fitness

# -------------------------------------------------------------------------
# -------------------------Fitness-----------------------------------------
# -------------------------------------------------------------------------

    def fitness(self, params):
        orders, solution = params
        solution.orders = orders
        submit_game_response = api.submit_game(self.api_key, self.map_name, solution)
        return Chrom(orders, submit_game_response['score'])

    def get_fitness(self, chrom_list, solution):
        with Pool(processes=60) as pool:
            population = pool.map(self.fitness, zip(chrom_list, [solution for _ in range(len(chrom_list))]))
            return sorted(population, key=lambda c: c.fitness, reverse=True)

# -------------------------------------------------------------------------
# -------------------------Mutation----------------------------------------
# -------------------------------------------------------------------------

    def mutate(self, orders):
        ord = [max(0, order + randint(-2,2)) if uniform(0,1) < self.mutation_rate else order for order in orders]
        return ord