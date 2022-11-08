from geneticAlgorithm import GA
from orderAlgoritm import OA
from collections import namedtuple
import math
import time
from sys import argv

api_key = "97b8ff47-ad44-4018-645e-08dabbf9e85f"
Chrom = namedtuple('Chrom', 'array fitness')
ChromosoneTuple = namedtuple('ChromosoneTuple', 'chromosone fitness')

def main():
	# argv: map, batches, ga_generations, oa_mutation_rate

	# Map stuff
	map = int(argv[1])
	maps = ["Suburbia", "Fancyville", "Farmville", "Mountana", "Pleasure Ville", "Scy Scrape City"]
	map_name = maps[map]

	max_time = [30, 30, 30, 30, 30, 30]

	population_size = 60 #Around 60
	
	# Genetic algoritm vars
	batches = int(argv[2])  #Around 10 to 30 ish
	ga_generations = int(argv[3]) #Around 10
	verbose = 2

	# Order algoritm vars
	oa_mutation_rate = float(argv[4]) #0.5

	start_time = time.time()
	max_time = max_time[map] * 0.5 * 60
	print("Starting genetic algoritm")
	genetic_algo = GA(map_name)
	
	best_chromosone = ChromosoneTuple(None, -math.inf)
	for batch in range(batches):
		print(f"Batch {batch+1} out of {batches}")
		chromosone = genetic_algo.fit(
			generation_limit=ga_generations,
			population_size=population_size,  
			verbose=verbose
		)
		
		best_chromosone = chromosone if chromosone.fitness > best_chromosone.fitness else best_chromosone
		if start_time - time.time() > max_time:
			print("Time limit exceeded, going to order_algo")
			break

	print("Starting order algoritm")
	order_algo = OA(map_name)
	orders = order_algo.fit(
		best_chromosone, 
		population_size=population_size, 
		mutation_rate=oa_mutation_rate,
		verbose=verbose
	)
	print(orders)
	print(f"parameters: Bag_type:{best_chromosone.chromosone.bag_type}, Bag_price: {best_chromosone.chromosone.bag_price}, Refund_amount: {best_chromosone.chromosone.refund_amount}, Refund policy: {best_chromosone.chromosone.refund}")

	
if __name__ == "__main__":
	main()