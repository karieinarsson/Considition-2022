from chromosone import Chromosone
from solver import Solver
import api

import aiohttp
import asyncio

import json
from typing import List, Tuple
from math import copysign
from random import randint, choices
from collections import namedtuple
from multiprocessing import Pool

api_key = "97b8ff47-ad44-4018-645e-08dabbf9e85f"
base_api_path = "https://api.considition.com/api/game/"

bag_type_cost = [0, 1.7, 1.75, 6, 25, 200]
ChromosoneTuple = namedtuple('ChromosoneTuple', 'chromosone fitness')

class GA:
    def __init__(self) -> None:
        self.population = []
    
# -------------------------------------------------------------------------
# -------------------------Main function-----------------------------------
# -------------------------------------------------------------------------
    
    def run_evolution(self, 
            generation_limit: int=20, 
            population_size: int=10, 
            verbose: int = 1, 
            map_name: str = "Fancyville"
        ) -> ChromosoneTuple:

        self.map_name = map_name
        self.verbose = verbose
        self.response = api.map_info(api_key, self.map_name)
        
        self.population = self.original_batch(population_size)

        for generation in range(generation_limit):

            if population_size != len(self.population):
                print(len(self.population))
                assert False

            # Next generation generation

            next_generation = self.original_next_gen()

            self.population = next_generation

            # Prints for feedback after each generation
            if self.verbose == 1:
                for each in next_generation: print(each.fitness)
                print("-----------------------------")

            
            if self.verbose > 0:
                print(f"Generation {generation}")
                max_chromosone = max(next_generation, key=lambda chromosone: chromosone.fitness)
                self.print_status(max_chromosone)

            self.population = sorted(
                    self.population,
                    key=lambda c: c.fitness,
                    reverse=True
                )
        
        # Prints for when algorithm is done

        result = self.population[0]

        solver = Solver(self.response, result.chromosone.bag_type,
                        result.chromosone.bag_price,
                        result.chromosone.refund_amount,
                        result.chromosone.refund,
                        result.chromosone.get_order)
        solution = solver.Solve(days=31)
        if self.verbose == 1:
            print(self.population)
        
        print("-----------------------------")
        print("Final Score")
        if verbose > 0:
            self.verbose = 1
            self.print_status(result)
        game = api.submit_game(api_key, self.map_name, solution)
        print(game['visualizer'])
        
        return result
    
# -------------------------------------------------------------------------
# -------------------------Gen Population----------------------------------
# -------------------------------------------------------------------------
    
    def generate_population(self, size: int) -> List[ChromosoneTuple]:
        chrom_list = [Chromosone() for _ in range(size)]
        return self.get_fitness(chrom_list)
            
    def original_batch(self, population_size: int) -> List[ChromosoneTuple]:
        pop = self.generate_population(population_size*5)
        batch = sorted(
                pop,
                key=lambda chromosone: chromosone.fitness,
                reverse=True
            )
        return batch[0:population_size]

# -------------------------------------------------------------------------
# -------------------------Fitness-----------------------------------------
# -------------------------------------------------------------------------

    async def fast_submit_all_games(self, chromosones):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for c in chromosones:
                task = asyncio.ensure_future(self.fast_submit_game(session, c))
                tasks.append(task)
            chrom_tuples = await asyncio.gather(*tasks, return_exceptions=True)
            return chrom_tuples

    async def fast_submit_game(self, session, c):
        solver = Solver(self.response, c.bag_type, c.bag_price, c.refund_amount, c.refund, c.get_order)
        solution = solver.Solve(days=31)
        solution.add_map_name(self.map_name)
        status_code = 0
        while status_code != 200:
            async with session.post(
                                base_api_path + "submit", 
                                headers={"x-api-key": api_key}, 
                                json=json.loads(solution.toJSON())
                            ) as response:
                result = await response.json()
                status_code = response.status
                if status_code == 200:
                    score = result["score"]
                    if type(score) == int:
                        return ChromosoneTuple(c, score)

    def fitness(self, c : Chromosone) -> List[ChromosoneTuple]:
        solver = Solver(self.response, c.bag_type, c.bag_price, c.refund_amount, c.refund, c.get_order)
        solution = solver.Solve(days=31)
        submit_game_response = api.submit_game(api_key, self.map_name, solution)
        return ChromosoneTuple(c, submit_game_response['score'])
    
    def get_fitness(self, chrom_list: List[Chromosone]) -> List[ChromosoneTuple]:
        #return asyncio.get_event_loop().run_until_complete(self.fast_submit_all_games(chrom_list)) 
        with Pool(processes=60) as pool:
            return pool.map(self.fitness, list(chrom_list))

# -------------------------------------------------------------------------
# -------------------------Mutation----------------------------------------
# -------------------------------------------------------------------------
       
    def uniform_crossover(self, a: Chromosone , b: Chromosone) -> Tuple[Chromosone]:        
        A = a.get_genes()
        B = b.get_genes()

        for i in range(len(A)):
            if randint(0,1):
                A[i], B[i] = B[i], A[i]
        
        childA = Chromosone(*A)
        childB = Chromosone(*B)

        paramsA = childA.get_params()
        paramsB = childB.get_params()

        for i in range(len(paramsA)):
            if randint(0,1):
                paramsA[i], paramsB[i] = paramsB[i], paramsA[i]

        childA.set_params(paramsA)
        childB.set_params(paramsB)

        return [childA, childB]
        
    def uniform_mutation(self, c: Chromosone, percent: float) -> List[Chromosone]:
        C = Chromosone(*c.get_genes())
        C.set_params(c.get_params())
        C.mutate()
        return C

# -------------------------------------------------------------------------
# -------------------------Selection process-------------------------------
# -------------------------------------------------------------------------

    def selection_pair(self, weights) -> Tuple[ChromosoneTuple]:
        return choices(
            population = self.population,
            weights = [x + abs(min(weights)) for x in weights],
            k=2
        )
 
    def original_next_gen(self) -> List[ChromosoneTuple]:
        weights = list(map(lambda n: n**2 * copysign(1,n) , [chromosone.fitness for chromosone in self.population]))
        top_n = 5
        top_n_ct = self.population[0:top_n]
        next_generation = [self.uniform_mutation(c.chromosone, 0.05) for c in top_n_ct]

        for _ in range((len(self.population)-top_n*2)//2):
            parent_a, parent_b = self.selection_pair(weights)
            child_a, child_b = self.uniform_crossover(parent_a.chromosone, parent_b.chromosone)
            child_a.mutate()
            child_b.mutate()
            next_generation += [child_a, child_b]

        return top_n_ct + self.get_fitness(next_generation)

# -------------------------------------------------------------------------
# -------------------------Prints------------------------------------------
# -------------------------------------------------------------------------

    def print_status(self, result) -> None:
        print(f"Top score is {result.fitness}")

        print(f"bag price: {result.chromosone.bag_price}", end=", ")
        print(f"refund: {result.chromosone.refund}", end=", ")
        print(f"refund_amount: {result.chromosone.refund_amount}", end=", ")
        print(f"bag_type: {result.chromosone.bag_type}")
