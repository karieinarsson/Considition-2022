from random import randint, uniform, choices
from solver import Solver
from collections import namedtuple
from chromosone import Chromosone
from multiprocessing import Pool
from typing import List, Tuple
from functions import f_vars
from math import copysign
import api
import time

api_key = "97b8ff47-ad44-4018-645e-08dabbf9e85f"

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
            mutation_fraq: float=0.1, 
            fine_mutation_rate: float = 0.5, 
            verbose: int = 1, 
            function: int = 0,
            map_name: str = "Fancyville"
        ) -> ChromosoneTuple:

        assert population_size % 4 == 0

        self.map_name = map_name
        self.verbose = verbose
        self.function = function
        self.response = api.map_info(api_key, self.map_name)
        
        self.population = self.original_batch(population_size)

        for generation in range(generation_limit):

            if population_size != len(self.population):
                print(len(self.population))
                assert False

            self.random_mutation_rate = max(0, 0.5-generation/(mutation_fraq*generation_limit))
            self.fine_mutation_rate = max(fine_mutation_rate, 1-self.random_mutation_rate)

            # Next generation generation
            if generation/generation_limit > 0.9:
                next_generation = self.next_gen_v2()
            else:
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
        chrom_list = [Chromosone(self.function) for _ in range(size)]
        
        return self.get_fitness(chrom_list)
            
    def original_batch(self, population_size: int) -> List[ChromosoneTuple]:
        batch = sorted(
                self.generate_population(population_size*10),
                key=lambda chromosone: chromosone.fitness,
                reverse=True
            )
        return batch[0:population_size]

# -------------------------------------------------------------------------
# -------------------------Fitness-----------------------------------------
# -------------------------------------------------------------------------

    def fitness(self, c : Chromosone) -> List[ChromosoneTuple]:
        solver = Solver(self.response, c.bag_type, c.bag_price, c.refund_amount, c.refund, c.get_order)
        solution = solver.Solve(days=31)
        submit_game_response = api.submit_game(api_key, self.map_name, solution)
        return ChromosoneTuple(c, submit_game_response['score'])
    
    def get_fitness(self, chrom_list: List[Chromosone]) -> List[ChromosoneTuple]: 
        with Pool(processes=24) as pool:
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
        return [childA, childB]
    
    def mutation(self, c : Chromosone, random_mutation_rate: float, fine_mutation_rate: float) -> Chromosone:
        if(uniform(0,1) < random_mutation_rate):
            c.bag_type = randint(1,4)
    
        if(uniform(0,1) > random_mutation_rate):
            c.refund = abs(c.refund-1)
        
        if(uniform(0,1) < random_mutation_rate):
            c.bag_price = uniform(bag_type_cost[c.bag_type], bag_type_cost[c.bag_type]*20)
        elif (uniform(0,1) < fine_mutation_rate):
            c.bag_price *= uniform(0.95,1.05)
        
        if(uniform(0,1) < random_mutation_rate):
            c.refund_amount = uniform(0, c.bag_price)
        elif (uniform(0,1) < fine_mutation_rate):
            c.refund_amount *= uniform(0.95, 1.05)
            
        if(uniform(0,1 < random_mutation_rate)):
            c.k0 = uniform(f_vars[c.function][0][0], f_vars[c.function][0][1])
        elif (uniform(0,1) < fine_mutation_rate):
            c.k0 *= uniform(0.95,1.05)
            
        if(uniform(0,1 < random_mutation_rate)):
            c.k1 = uniform(f_vars[c.function][1][0], f_vars[c.function][1][1])
        elif (uniform(0,1) < fine_mutation_rate):
            c.k1 *= uniform(0.95,1.05)
        
        if(uniform(0,1 < random_mutation_rate)):
            c.k2 = uniform(f_vars[c.function][2][0], f_vars[c.function][2][1])
        elif (uniform(0,1) < fine_mutation_rate):
            c.k2 *= uniform(0.95,1.05)

        if(uniform(0,1 < random_mutation_rate)):
            c.k3 = uniform(f_vars[c.function][3][0], f_vars[c.function][3][1])
        elif (uniform(0,1) < fine_mutation_rate):
            c.k3 *= uniform(0.95,1.05)
            
        if(uniform(0,1 < random_mutation_rate)):
            c.k4 = uniform(f_vars[c.function][4][0], f_vars[c.function][4][1])
        elif (uniform(0,1) < fine_mutation_rate):
            c.k4 *= uniform(0.95,1.05)
        
        if(uniform(0,1 < random_mutation_rate)):
            c.k5 = uniform(f_vars[c.function][5][0], f_vars[c.function][5][1])
        elif (uniform(0,1) < fine_mutation_rate):
            c.k5 *= uniform(0.95,1.05)
            
        return c
        
    def uniform_mutation(self, c: Chromosone, percent: float) -> List[Chromosone]:
        c = Chromosone(*c.get_genes())
        i = randint(0,7)
        if i == 0:
            c.bag_price *= uniform(1-percent,1+percent)
        elif i == 1:
            c.refund_amount *= uniform(1-percent,1+percent)
        elif i == 2:
            c.k0 *= uniform(1-percent,1+percent)
        elif i == 3:
            c.k1 *= uniform(1-percent,1+percent)
        elif i == 4:
            c.k2 *= uniform(1-percent,1+percent)
        elif i == 5:
            c.k3 *= uniform(1-percent,1+percent)
        elif i == 6:
            c.k4 *= uniform(1-percent,1+percent)
        elif i == 7:
            c.k5 *= uniform(1-percent,1+percent)
        

        return c

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
        next_generation = [c.chromosone for c in self.population[0:top_n]]
        next_generation += [self.uniform_mutation(c, 0.05) for c in next_generation]

        for _ in range((len(self.population)-len(next_generation))//2):
            parent_a, parent_b = self.selection_pair(weights)
            child_a, child_b = self.uniform_crossover(parent_a.chromosone, parent_b.chromosone)
            child_a = self.mutation(child_a, self.random_mutation_rate, self.fine_mutation_rate)
            child_b = self.mutation(child_b, self.random_mutation_rate, self.fine_mutation_rate)
            next_generation += [child_a, child_b]

        return self.get_fitness(next_generation)
            
    def next_gen_v2(self) -> List[ChromosoneTuple]:
        top25 = [c.chromosone for c in self.population[0:len(self.population)//4]] #First 25 percent of the next generation
        mini_tune = [self.uniform_mutation(c, 0.001) for c in top25] # Second 25 percent of the next generation
        fine_tune = [self.uniform_mutation(c, 0.01) for c in top25] # Third
        rough_tune = [self.uniform_mutation(c, 0.1) for c in top25]
        return self.get_fitness(top25 + mini_tune + fine_tune + rough_tune)

# -------------------------------------------------------------------------
# -------------------------Prints------------------------------------------
# -------------------------------------------------------------------------

    def print_status(self, result) -> None:
        print(f"Top score is {result.fitness}")

        print(f"bag price: {result.chromosone.bag_price}", end=", ")
        print(f"function: {result.chromosone.function}", end=", ")
        print(f"refund: {result.chromosone.refund}", end=", ")
        print(f"refund_amount: {result.chromosone.refund_amount}", end=", ")
        print(f"bag_type: {result.chromosone.bag_type}", end=", ")
        
        print(f"k0: {result.chromosone.k0}", end=", ")
        print(f"k1: {result.chromosone.k1}", end=", ")
        print(f"k2: {result.chromosone.k2}", end=", ")
        print(f"k3: {result.chromosone.k3}", end=", ")
        print(f"k4: {result.chromosone.k4}", end=", ")
        print(f"k5: {result.chromosone.k5}")
