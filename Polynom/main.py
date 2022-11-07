from geneticAlgorithm import GA
from multiprocessing import Pool
import time

map_name = "Suburbia"
#map_name = "Fancyville"

def main():
	ga = GA()
	print("Starting game...")
	s = time.time()
	ga.run_evolution(
		generation_limit=50, 
		population_size=100, 
		verbose=1, 
		map_name=map_name
	)
	min, sec = divmod(time.time()-s, 60)
	print(f"Total time: {round(min, 0)}m:{round(sec, 0)}s")

if __name__ == "__main__":
	main()