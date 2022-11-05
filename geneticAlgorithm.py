from random import randint, uniform, choices
from solver import Solver
from collections import namedtuple
from chromosone import Chromosone
from multiprocessing import Pool
from typing import List, Tuple
from functions import f_vars
import api


api_key = "97b8ff47-ad44-4018-645e-08dabbf9e85f"

#map_name = "Suburbia"
map_name = "Fancyville"

response = api.map_info(api_key, map_name)

bag_type_cost = [1.7, 1.75, 6, 25, 200]
ChromosoneTuple = namedtuple('ChromosoneTuple', 'chromosone fitness')

class GA:
    def __init__(self) -> None:
        print(f"Map info: {response}")
        print(f"Map: {map_name}")
        self.population = []
    
# -------------------------------------------------------------------------
# -------------------------Main function-----------------------------------
# -------------------------------------------------------------------------
    
    def run_evolution(self, generation_limit: int=20, population_size: int=10, mutation_fraq: float=0.1, fine_mutation_rate: float = 0.5,  function: int = 4, verbose:int = 1) -> ChromosoneTuple:
        assert population_size % 4 == 0
        assert generation_limit % 10 == 0
        
        self.function = function
        self.verbose = verbose

        self.population = self.original_batch(population_size)

        for generation in range(generation_limit):
            
            random_mutation_rate = max(0, 1-generation/(mutation_fraq*generation_limit))

            # Next generation generation
            #if generation < generation_limit//10:
            #    next_generation = self.next_gen_v2()
            #else:
            next_generation = self.original_next_gen(random_mutation_rate, fine_mutation_rate)
            
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
        
        solver = Solver(response, result.chromosone.bag_type,
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
        game = api.submit_game(api_key, map_name, solution)
        print(game['visualizer'])
        
        return result
    
# -------------------------------------------------------------------------
# -------------------------Gen Population----------------------------------
# -------------------------------------------------------------------------

    def generate_chromosone(self) -> Chromosone:
        bag_type = randint(1,4)
        refund = randint(0,1)
        bag_price = uniform(bag_type_cost[bag_type], bag_type_cost[bag_type]*10)
        refund_amount = uniform(0, bag_price)

        k0 = uniform(f_vars[self.function][0][0], f_vars[self.function][0][1])
        k1 = uniform(f_vars[self.function][1][0], f_vars[self.function][1][1])
        k2 = uniform(f_vars[self.function][2][0], f_vars[self.function][2][1])
        k3 = uniform(f_vars[self.function][3][0], f_vars[self.function][3][1])
        k4 = uniform(f_vars[self.function][4][0], f_vars[self.function][4][1])
        k5 = uniform(f_vars[self.function][5][0], f_vars[self.function][5][1])
        
        return Chromosone(self.function, bag_type, refund, bag_price, refund_amount, k0, k1, k2, k3, k4, k5)
    
    def generate_population(self, size: int) -> List[ChromosoneTuple]:
        chrom_list = [self.generate_chromosone() for _ in range(size)]
        return self.get_fitness(chrom_list)
            
    def original_batch(self, population_size: int) -> List[ChromosoneTuple]:
        batch = sorted(
                self.generate_population(population_size),
                key=lambda chromosone: chromosone.fitness,
                reverse=True
            )
        return batch[0:population_size]

# -------------------------------------------------------------------------
# -------------------------Fitness-----------------------------------------
# -------------------------------------------------------------------------

    def fitness(self, c : Chromosone) -> List[ChromosoneTuple]:
        solver = Solver(response, c.bag_type, c.bag_price, c.refund_amount, c.refund, c.get_order)
        solution = solver.Solve(days=31)
        submit_game_response = api.submit_game(api_key, map_name, solution)
        return ChromosoneTuple(c, submit_game_response['score'])
    
    def get_fitness(self, chrom_list: List[Chromosone]) -> List[ChromosoneTuple]: 
        #return list(map(self.fitness, chrom_list))
        with Pool(processes=24) as pool:
            return pool.map(self.fitness, chrom_list)

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
    
    def mutation(self, c : Chromosone, random_mutation_rate: float, fine_mutation_rate: float) -> List[Chromosone]:
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
            c.k0 = uniform(f_vars[self.function][0][0], f_vars[self.function][0][1])
        elif (uniform(0,1) < fine_mutation_rate):
            c.k0 *= uniform(0.95,1.05)
            
        if(uniform(0,1 < random_mutation_rate)):
            c.k1 = uniform(f_vars[self.function][1][0], f_vars[self.function][1][1])
        elif (uniform(0,1) < fine_mutation_rate):
            c.k1 *= uniform(0.95,1.05)
        
        if(uniform(0,1 < random_mutation_rate)):
            c.k2 = uniform(f_vars[self.function][2][0], f_vars[self.function][2][1])
        elif (uniform(0,1) < fine_mutation_rate):
            c.k2 *= uniform(0.95,1.05)

        if(uniform(0,1 < random_mutation_rate)):
            c.k3 = uniform(f_vars[self.function][3][0], f_vars[self.function][3][1])
        elif (uniform(0,1) < fine_mutation_rate):
            c.k3 *= uniform(0.95,1.05)
            
        if(uniform(0,1 < random_mutation_rate)):
            c.k4 = uniform(f_vars[self.function][4][0], f_vars[self.function][4][1])
        elif (uniform(0,1) < fine_mutation_rate):
            c.k4 *= uniform(0.95,1.05)
        
        if(uniform(0,1 < random_mutation_rate)):
            c.k5 = uniform(f_vars[self.function][5][0], f_vars[self.function][5][1])
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
            c.k4 *= uniform(1-percent,1+percent)

        return c

# -------------------------------------------------------------------------
# -------------------------Selection process-------------------------------
# -------------------------------------------------------------------------

    def selection_pair(self) -> Tuple[ChromosoneTuple]:
        weights = [chromosone.fitness for chromosone in self.population]
        return choices(
            population = self.population,
            weights = [x + abs(min(weights)) for x in weights],
            k=2
        )
 
    def original_next_gen(self, random_mutation_rate: float, fine_mutation_rate: float) -> List[ChromosoneTuple]:
        next_generation = [c.chromosone for c in self.population[0:5]]
        next_generation = next_generation + [self.uniform_mutation(self.population[0].chromosone, 0.01), self.uniform_mutation(self.population[1].chromosone, 0.01)]

        for i in range(int(len(self.population)/2)-10):
            parent_a, parent_b = self.selection_pair()
            child_a, child_b = self.uniform_crossover(parent_a.chromosone, parent_b.chromosone)
            child_a = self.mutation(child_a, random_mutation_rate, fine_mutation_rate)
            child_b = self.mutation(child_b, random_mutation_rate, fine_mutation_rate)
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
        print(f"refund: {result.chromosone.refund}", end=", ")
        print(f"refund_amount: {result.chromosone.refund_amount}", end=", ")
        print(f"bag_type: {result.chromosone.bag_type + 1}", end=", ")
        
        print(f"k0: {result.chromosone.k0}", end=", ")
        print(f"k1: {result.chromosone.k1}", end=", ")
        print(f"k2: {result.chromosone.k2}", end=", ")
        print(f"k3: {result.chromosone.k3}", end=", ")
        print(f"k4: {result.chromosone.k4}", end=", ")
        print(f"k5: {result.chromosone.k5}")
        
# -------------------------------------------------------------------------
# -------------------------L33t--------------------------------------------
# -------------------------------------------------------------------------

    def L33t_fitness(self, c):
        solver = Solver(response, c.bag_type, c.bag_price, c.refund_amount, c.refund, c.get_order)
        solution = solver.Solve(days=31)
        submit_game_response = api.submit_game(api_key, map_name, solution)
        if submit_game_response['score'] == 1337:
            print(submit_game_response)
            assert False
        if submit_game_response['score'] < 1337:
            return submit_game_response['score']
        return -submit_game_response['score']+1337
    
    def L33t_original_next_gen(self, mutation_rate, generation, generation_limit):
        next_generation = self.population[0:2]
        next_generation = next_generation + [self.L33t_uniform_mutation(self.population[0].chromosone, 0.01), self.L33t_uniform_mutation(self.population[1].chromosone, 0.01)]

        for i in range(int(len(self.population)/2)-2):
            parents = self.selection_pair()
            child_a, child_b = self.uniform_crossover(parents[0].chromosone, parents[1].chromosone)
            child_a = self.mutation(child_a, mutation_rate, generation, generation_limit)
            child_b = self.mutation(child_b, mutation_rate, generation, generation_limit)
            next_generation += [ChromosoneTuple(child_a, self.L33t_fitness(child_a)), ChromosoneTuple(child_b, self.L33t_fitness(child_b))]
        
        return next_generation

    def L33t_next_gen_v2(self):
        top25 = self.population[0:len(self.population)//4] #First 25 percent of the next generation
        mini_mutated = [self.L33t_uniform_mutation(c.chromosone, 0.001) for c in top25] # Second 25 percent of the next generation
        fine_mutated = [self.L33t_uniform_mutation(c.chromosone, 0.01) for c in top25] # Third
        rough_mutated = [self.L33t_uniform_mutation(c.chromosone, 0.1) for c in top25]
        return top25 + mini_mutated + fine_mutated + rough_mutated

    def L33t_uniform_mutation(self, c: Chromosone, percent: float):
        c = Chromosone(*c.get_genes())
        i = randint(0,6)
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
        return ChromosoneTuple(c, self.L33t_fitness(c))