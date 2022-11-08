from chromosone import Chromosone
from solver import Solver
import api

from multiprocessing import Pool
from typing import List, Tuple
from random import randint, uniform, choices
from collections import namedtuple
import queue

api_key = "97b8ff47-ad44-4018-645e-08dabbf9e85f"
ChromosoneTuple = namedtuple('ChromosoneTuple', 'chromosone fitness')

class GA:
    def __init__(self, 
            map_name: str = "Fancyville",
        ) -> None:
        self.map_name = map_name
        self.response = api.map_info(api_key, self.map_name)
        self.days = 31 if self.map_name == "Suburbia" or self.map_name == "Fancyville" else 365

    
# -------------------------------------------------------------------------
# -------------------------Fit function------------------------------------
# -------------------------------------------------------------------------
    
    def fit(self,
            generation_limit: int=20, 
            population_size: int=10, 
            verbose: int = 1, 
        ) -> List[ChromosoneTuple]:

        assert population_size > 4, "Population size under 4"

        population =  self.original_batch(population_size)

        q = queue.Queue(5)

        for generation in range(generation_limit):

            assert population_size == len(population), "Population size changed!"

            random_mutation = 0.8 - generation / generation_limit

            # Next generation generation
            if generation/generation_limit > 0.9:
                next_generation = self.next_gen_v2(population_size, population)
            else:
                next_generation = self.original_next_gen(population, random_mutation)

            population = next_generation

            # Prints for feedback after each generation
            if verbose == 1:
                for each in next_generation: print(each.fitness)
                print("-----------------------------")

            
            if verbose > 0:
                print(f"Generation {generation}")
                max_chromosone = max(next_generation, key=lambda chromosone: chromosone.fitness)
                self.print_status(max_chromosone)

            population = sorted(
                    population,
                    key=lambda c: c.fitness,
                    reverse=True
                )
            
            if q.full() and q.get(block=False) == population[0].fitness: return population[0]
            q.put(population[0].fitness)
        
        # Prints for when algorithm is done

        result = population[0]


        solver = Solver(self.response, result.chromosone.bag_type,
                        result.chromosone.bag_price,
                        result.chromosone.refund_amount,
                        result.chromosone.refund,
                        result.chromosone.get_order)
        solution = solver.Solve(days=self.days)
        
        game = api.submit_game(api_key, self.map_name, solution)
        if verbose > 0:
            print("-----------------------------")
            print("Final Score")
            self.print_status(result)
            print(game['visualizer'])
        
        return population[0]
    
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

    def fitness(self, c : Chromosone) -> List[ChromosoneTuple]:
        solver = Solver(self.response, c.bag_type, c.bag_price, c.refund_amount, c.refund, c.get_order)
        solution = solver.Solve(days=self.days)
        submit_game_response = api.submit_game(api_key, self.map_name, solution)
        return ChromosoneTuple(c, submit_game_response['score'])
    
    def get_fitness(self, chrom_list: List[Chromosone]) -> List[ChromosoneTuple]:
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
        return [childA, childB]
        
    def uniform_mutation(self, c: Chromosone, percent: float) -> List[Chromosone]:
        C = Chromosone(*c.get_genes())
        C.mutate(percent)
        return C

# -------------------------------------------------------------------------
# -------------------------Selection process-------------------------------
# -------------------------------------------------------------------------

    def selection_pair(self, weights, population) -> Tuple[ChromosoneTuple]:
        return choices(
            population = population,
            weights = [x + abs(min(weights)) for x in weights],
            k=2
        )
 
    def original_next_gen(self, population, random_mutation) -> List[ChromosoneTuple]:
        weights = [chromosone.fitness for chromosone in population]
        top_n = 2
        top_n_ct = population[0:top_n]
        next_generation = [self.uniform_mutation(c.chromosone, 0.001) for c in top_n_ct]

        for _ in range((len(population)-top_n*2)//2):
            parent_a, parent_b = self.selection_pair(weights, population)
            child_a, child_b = self.uniform_crossover(parent_a.chromosone, parent_b.chromosone)
            if uniform(0,1) < random_mutation:
                child_a.random_mutate()
                child_b.random_mutate()
            else:
                child_a.mutate(1)
                child_b.mutate(1)
            next_generation += [child_a, child_b]

        return top_n_ct + self.get_fitness(next_generation)
            
    def next_gen_v2(self, population_size, population) -> List[ChromosoneTuple]:
        c = population[0]
        top25 = [self.uniform_mutation(c.chromosone, 0.001) for _ in range(population_size//4)] #First 25 percent of the next generation
        mini_tune = [self.uniform_mutation(c.chromosone, 0.01) for _ in range(population_size//4)] # Second 25 percent of the next generation
        fine_tune = [self.uniform_mutation(c.chromosone, 0.1) for _ in range(population_size//4)] # Third
        rough_tune = [self.uniform_mutation(c.chromosone, 1) for _ in range((population_size//4)-1)]
        return [c] + self.get_fitness(top25 + mini_tune + fine_tune + rough_tune)
        

# -------------------------------------------------------------------------
# -------------------------Prints------------------------------------------
# -------------------------------------------------------------------------

    def print_status(self, result) -> None:
        print(f"Top score is {result.fitness}")

        print(f"bag price: {result.chromosone.bag_price}", end=", ")
        print(f"refund: {result.chromosone.refund}", end=", ")
        print(f"refund_amount: {result.chromosone.refund_amount}", end=", ")
        print(f"bag_type: {result.chromosone.bag_type}", end=", ")
        
        for i, k in enumerate(result.chromosone.k):
            print(f"k{i}: {k}", end=", ")
        print("")