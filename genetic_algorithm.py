from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import numpy
import random
import tsp
import elitism
from fitness_game import Game
import matplotlib.pyplot as plt
from ai import get_weights
import pygame
from config import *

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
display.fill(BACKGROUND_COLOR)


def fitnessTetris(individual):
    g = Game(display, individual)
    return g.count_of_broken_lines,


LENGTH = 7

POPULATION_SIZE = 50
P_CROSSOVER = 0.95
P_MUTATION = 0.10
MAX_GENERATIONS = 15
HALL_OF_FAME_SIZE = 7

# RANDOM_SEED = 20000
# random.seed(RANDOM_SEED)

toolbox = base.Toolbox()
toolbox.register("randomForList", random.randint, -1000, 1000)

creator.create("FitnessMax", base.Fitness, weights=(1.0, ))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox.register("individualCreator", tools.initRepeat,
                 creator.Individual, toolbox.randomForList, LENGTH)
toolbox.register("populationCreator", tools.initRepeat,
                 list, toolbox.individualCreator)
toolbox.register("evaluate", fitnessTetris)

toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=-100, up=100, indpb=1.0/LENGTH)

def main():
    # create initial population (generation 0):
    population = toolbox.populationCreator(n=POPULATION_SIZE)

    # prepare the statistics object:
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", numpy.max)
    stats.register("avg", numpy.mean)

    # define the hall-of-fame object:
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    # perform the Genetic Algorithm flow with hof feature added:
    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

    best = hof.items[0]
    print("-- Best Ever Individual = ", best)
    print("-- Best Ever Fitness = ", best.fitness.values[0])

    # extract statistics:
    maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")

    # plot statistics:
    plt.plot(maxFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Max / Average Fitness')
    plt.title('Max and Average Fitness over Generations')

    plt.show()


if __name__ == '__main__':
    main()

# def get_weights():
#     HEIGHT = 100
#     CLEARS = 6000
#     HOLES = -2000
#     BLOCKADES = -900
#     BLOCK = 300
#     WALL = 200
#     FLOOR = 1050
#     WEIGHTS = [HEIGHT, CLEARS, HOLES, BLOCKADES, BLOCK, WALL, FLOOR]
#     # calculate weights with genetic algorithm
#     return WEIGHTS
