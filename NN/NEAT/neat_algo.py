import os
import neat
from solver import Solver
import api

api_key = "97b8ff47-ad44-4018-645e-08dabbf9e85f"
base_api_path = "https://api.considition.com/api/game/"
map_name = "Fancyville"
response = api.map_info(api_key, map_name)

def fitness(genome, config):
    net = neat.nn.FeedForwardNetwork(genome, config)
    
    solver = Solver(response, c.bag_type, c.bag_price, c.refund_amount, c.refund,   )
    solution = solver.Solve(days=31)
    submit_game_response = api.submit_game(api_key, map_name, solution)
    return submit_game_response['score']


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_file)
    
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter)
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run()