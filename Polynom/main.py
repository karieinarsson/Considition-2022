from geneticAlgorithm import GA
from orderAlgoritm import OA
from collections import namedtuple
import math

api_key = "97b8ff47-ad44-4018-645e-08dabbf9e85f"
Chrom = namedtuple('Chrom', 'array fitness')
ChromosoneTuple = namedtuple('ChromosoneTuple', 'chromosone fitness')

def main():

	# Map stuff
	maps = ["Suburbia", "Fancyville", "Farmville", "Mountana Ville", "Pleasure Ville", "Scy Scrape City"]
	map_name = maps[1]

	# Genetic algoritm vars
	batches = 1
	ga_population_size = 10
	ga_generations = 1
	verbose = 2

	# Order algoritm vars
	oa_population_size = 2
	oa_generations = 5
	oa_mutation_rate = 0.5

	
	print("Starting genetic algoritm")
	genetic_algo = GA(map_name)
	best_chromosone = ChromosoneTuple(None, -math.inf)
	for batch in range(batches):
		print(f"Batch {batch+1} out of {batches}")
		chromosone = genetic_algo.fit(
			generation_limit=ga_generations,
			population_size=ga_population_size,  
			verbose=verbose
		)
		best_chromosone = chromosone if chromosone.fitness > best_chromosone.fitness else best_chromosone

	print("Starting order algoritm")
	order_algo = OA(map_name)
	solution = order_algo.fit(
		best_chromosone, 
		population_size=oa_population_size, 
		generations=oa_generations,
		mutation_rate=oa_mutation_rate,
		verbose=verbose
	)
	print(solution)
	
if __name__ == "__main__":
	main()