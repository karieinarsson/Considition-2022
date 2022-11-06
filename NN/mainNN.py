from geneticAlgorithmNN import GA
import time

#map_name = "Suburbia"
map_name = "Fancyville"

def main():
	ga = GA()
	# dummy test
	#ga.run_evolution(generation_limit=20, population_size=12, function = 2, mutation_fraq=0.5, verbose=2)
	#assert False
	#print("Starting game...")
	s = time.time()
	ga.run_evolution(
		generation_limit=50, 
		population_size=50,  
		verbose=1, 
		map_name=map_name
	)
	print(f"Total time: {(time.time()-s)/60} minutes")

if __name__ == "__main__":
	main()