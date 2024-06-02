from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import numpy
import random
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
    return g.score,


LENGTH = 7

POPULATION_SIZE = 20
P_CROSSOVER = 0.9
P_MUTATION = 0.05
MAX_GENERATIONS = 5
HALL_OF_FAME_SIZE = 10

RANDOM_SEED = 10000
random.seed(RANDOM_SEED)

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
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutUniformInt, low=-100, up=100, indpb=P_MUTATION)

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

    # print Hall of Fame info:
    print("Hall of Fame Individuals = ", *hof.items, sep="\n")
    print("Best Ever Individual = ", hof.items[0])

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
