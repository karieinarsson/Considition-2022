from geneticAlgorithm import GA
import time

#map_name = "Suburbia"
map_name = "Fancyville"

def main():
	ga = GA()
	print("Starting game...")
	s = time.time()
	ga.run_evolution(
		generation_limit=40, 
		population_size=20,  
		verbose=1, 
		map_name=map_name
	)
	min, sec = divmod(time.time()-s, 60)
	print(f"Total time: {round(min, 1)}m:{round(sec, 1)}s")

if __name__ == "__main__":
	main()