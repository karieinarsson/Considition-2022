from geneticAlgorithm import GA
from multiprocessing import Pool
import time

def main():
	ga = GA()
	# dummy test
	#ga.run_evolution(generation_limit=20, population_size=12, mutation_rate=0.25, function=2, verbose=2)
	#assert False
	print("Starting game...")
	s = time.time()
	ga.run_evolution(generation_limit=100, population_size=500, mutation_fraq=1, function=2, verbose=2)
	print(f"Total time: {time.time()-s}")

if __name__ == "__main__":
	main()