from deap import base
from deap import creator
from deap import tools
import random
from fitness_game import Game
from ai import get_weights
import pygame
from config import *

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
display.fill(BACKGROUND_COLOR)


def fitnessTetris(individual):
    g = Game(display, individual)
    # print(individual)
    return g.score,


# константы задачи
LENGTH = 7  # длина хромосомы
# константы генетического алгоритма
POPULATION_SIZE = 20  # количество индивидуумов в популяции
P_CROSSOVER = 0.9  # вероятность скрещивания
P_MUTATION = 0.05  # вероятность мутации индивидуума
MAX_GENERATIONS = 50  # максимальное количество поколений

RANDOM_SEED = 10000  # рандомайзер для генерации значений для хромосом
random.seed(RANDOM_SEED)

toolbox = base.Toolbox()
toolbox.register("randomForList", random.randint, -1000, 1000)

creator.create("FitnessMax", base.Fitness, weights=(1.0, ))
creator.create("Individual", list, fitness=creator.FitnessMax)  # создание класса индивидов
toolbox.register("individualCreator", tools.initRepeat,  # создаем индивида
                 creator.Individual, toolbox.randomForList, LENGTH)
toolbox.register("populationCreator", tools.initRepeat,  # создаем популяцию
                 list, toolbox.individualCreator)
toolbox.register("evaluate", fitnessTetris)

toolbox.register("select", tools.selTournament, tournsize=3)  # отбор турниром
toolbox.register("mate", tools.cxOnePoint)  # мутация, пока что такЮ но вроде тоже норм
toolbox.register("mutate", tools.mutFlipBit, indpb=1.0 / LENGTH)  # мутация, и так пойдет


def main():
    # create initial population (generation 0):
    population = toolbox.populationCreator(n=POPULATION_SIZE)
    print(population)
    generationCounter = 0

    # calculate fitness tuple for each individual in the population:
    fitnessValues = list(map(toolbox.evaluate, population))
    print(list(zip(population, fitnessValues)))
    for individual, fitnessValue in zip(population, fitnessValues):
        print(individual.fitness)
        print(fitnessValue)
        individual.fitness.values = fitnessValue

    # extract fitness values from all individuals in population:
    fitnessValues = [individual.fitness.values[0] for individual in population]

    # initialize statistics accumulators:
    maxFitnessValues = []
    meanFitnessValues = []

    # main evolutionary loop:
    # stop if max fitness value reached the known max value
    # OR if number of generations exceeded the preset value:
    while generationCounter < MAX_GENERATIONS:
        # update counter:
        generationCounter = generationCounter + 1

        # apply the selection operator, to select the next generation's individuals:
        offspring = toolbox.select(population, len(population))
        # clone the selected individuals:
        offspring = list(map(toolbox.clone, offspring))

    # apply the crossover operator to pairs of offspring:
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < P_CROSSOVER:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < P_MUTATION:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # calculate fitness for the individuals with no previous calculated fitness value:
        freshIndividuals = [ind for ind in offspring if not ind.fitness.valid]
        freshFitnessValues = list(map(toolbox.evaluate, freshIndividuals))
        for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
            individual.fitness.values = fitnessValue

        # replace the current population with the offspring:
        population[:] = offspring

        # collect fitnessValues into a list, update statistics and print:
        fitnessValues = [ind.fitness.values[0] for ind in population]

        maxFitness = max(fitnessValues)
        meanFitness = sum(fitnessValues) / len(population)
        maxFitnessValues.append(maxFitness)
        meanFitnessValues.append(meanFitness)
        print("- Generation {}: Max Fitness = {}, Avg Fitness = {}".format(generationCounter, maxFitness, meanFitness))

        # find and print best individual:
        best_index = fitnessValues.index(max(fitnessValues))
        print("Best Individual = ", *population[best_index], "\n")

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
