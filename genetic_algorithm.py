from deap import base
from deap import creator
from deap import tools
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
    population = toolbox.populationCreator(n=POPULATION_SIZE)
    print(population)
    generationCounter = 0

    fitnessValues = list(map(toolbox.evaluate, population))
    print(list(zip(population, fitnessValues)))
    for individual, fitnessValue in zip(population, fitnessValues):
        print(individual.fitness)
        print(fitnessValue)
        individual.fitness.values = fitnessValue

    fitnessValues = [individual.fitness.values[0] for individual in population]

    maxFitnessValues = []
    meanFitnessValues = []


    while generationCounter < MAX_GENERATIONS:
        generationCounter = generationCounter + 1

        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < P_CROSSOVER:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < P_MUTATION:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        freshIndividuals = [ind for ind in offspring if not ind.fitness.valid]
        freshFitnessValues = list(map(toolbox.evaluate, freshIndividuals))
        for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
            individual.fitness.values = fitnessValue

        population[:] = offspring

        fitnessValues = [ind.fitness.values[0] for ind in population]

        maxFitness = max(fitnessValues)
        meanFitness = sum(fitnessValues) / len(population)
        maxFitnessValues.append(maxFitness)
        meanFitnessValues.append(meanFitness)
        print("- Generation {}: Max Fitness = {}, Avg Fitness = {}".format(generationCounter, maxFitness, meanFitness))

        best_index = fitnessValues.index(max(fitnessValues))
        print("Best Individual = ", *population[best_index], "\n")

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
