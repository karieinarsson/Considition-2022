from solution import Solution
from collections import namedtuple
from random import randint, uniform
from multiprocessing import Pool
from collections import deque

import json
import aiohttp
import asyncio

import queue
import api

Chrom = namedtuple('Chrom', 'array fitness')
ChromosoneTuple = namedtuple('ChromosoneTuple', 'chromosone fitness')
api_key = "97b8ff47-ad44-4018-645e-08dabbf9e85f"
base_api_path = "https://api.considition.com/api/game/"

class OA:
    def __init__(self, map_name) -> None:
        self.api_key = "97b8ff47-ad44-4018-645e-08dabbf9e85f"
        self.map_name = map_name
        self.response = api.map_info(self.api_key, self.map_name)
        self.days = 31 if self.map_name == "Suburbia" or self.map_name == "Fancyville" else 365

# -------------------------------------------------------------------------
# -------------------------Fit function------------------------------------
# -------------------------------------------------------------------------

    def fit(self, c, population_size=60, mutation_rate=0.5, verbose=1):
        self.mutation_rate = mutation_rate

        best_orders = [c.chromosone.get_order(day, self.days) for day in range(self.days)]

        print(best_orders)

        solution = Solution(recycle_refund_choice = c.chromosone.refund,
                                bag_price = c.chromosone.bag_price, 
                                refund_amount = c.chromosone.refund_amount,
                                bag_type = c.chromosone.bag_type)
        solution.add_map_name(self.map_name)

        population = [best_orders] + [self.mutate(best_orders) for _ in range(population_size-1)]
        population = self.get_fitness(population, solution)

        q = queue.Queue(15)

        gen = 0 
        while True:
            population = [population[0].array] + [self.mutate(population[0].array) for _ in range(population_size-1)]
            population = self.get_fitness(population, solution)
            if verbose:
                gen += 1
                print(f"Top score for generation {gen} is {population[0].fitness}")
                print(f"{population[0].array}")

            if q.full() and q.get() == population[0].fitness: return population[0]
            q.put(population[0].fitness)
            self.mutation_rate = max(0.1,mutation_rate-gen*mutation_rate/30)

# -------------------------------------------------------------------------
# -------------------------Fitness-----------------------------------------
# -------------------------------------------------------------------------

    async def fast_submit_all_games(self, orders_list, solution):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for orders in orders_list:
                task = asyncio.ensure_future(self.fast_submit_game(session, orders, solution))
                tasks.append(task)
            chrom_tuples = await asyncio.gather(*tasks, return_exceptions=True)
            return chrom_tuples

    async def fast_submit_game(self, session, orders, solution):
        solution.orders = orders
        status_code = 0
        while status_code != 200:
            async with session.post(
                                base_api_path + "submit", 
                                headers={"x-api-key": api_key}, 
                                json=json.loads(solution.toJSON())
                            ) as response:
                status_code = response.status
                if response.status != 200:
                    print("You've been gnomed!!", end=" ")
                    continue
                result = await response.json()

                if status_code == 200:
                    return Chrom(orders, result['score'])

    def get_fitness(self, chrom_list, solution):
        population = asyncio.get_event_loop().run_until_complete(self.fast_submit_all_games(chrom_list, solution))
        return sorted(population, key=lambda c: c.fitness, reverse=True)

    def fitness(self, orders, solution):
        solution.orders = orders
        submit_game_response = api.submit_game(self.api_key, self.map_name, solution)
        return Chrom(orders, submit_game_response['score'])


# -------------------------------------------------------------------------
# -------------------------Mutation----------------------------------------
# -------------------------------------------------------------------------

    def mutate(self, orders):
        ord = [max(0, order + randint(-1,1)) if uniform(0,1) < self.mutation_rate else order for order in orders]
        for i in range(1, len(orders)):
            if(uniform(0,1) < self.mutation_rate):
                steal_amount = randint(-5,5)
                if(ord[i-1] - steal_amount > 0 and ord[i] + steal_amount > 0):
                    ord[i-1] -= steal_amount
                    ord[i] += steal_amount
        return ord
    
