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
    return g.score


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
toolbox.register("randomForList", random.randint, range(-6000, 6000))

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)  # создание класса индивидов
toolbox.register("individualCreator", tools.initRepeat,  # создаем индивида
                 creator.Individual, toolbox.randomForList, LENGTH)
toolbox.register("populationCreator", tools.initRepeat,  # создаем популяцию
                 list, toolbox.individualCreator)
toolbox.register("evaluate", fitnessTetris)

toolbox.register("select", tools.selTournament, tournsize=3)  # отбор турниром
toolbox.register("mate", tools.cxOnePoint)  # мутация, пока что такЮ но вроде тоже норм
toolbox.register("mutate", tools.mutFlipBit, indpb=1.0 / LENGTH)  # мутация, и так пойдет

# возвращаем скор(кол-во линий)
weights = open('weights.txt', 'rt').read().split('\n')
s = ''
for i in range(100):
    g = list(map(int, weights[i].split()))
    score = fitnessTetris(g)
    s += f'{weights[i]} {score}\n'
f = open('results.txt', 'wt')
f.write(s)
f.close()
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


_COUNT_OF_GAMES = 5
for generation in range(MAX_GENERATIONS):
    scores = []
    for _ in range(_COUNT_OF_GAMES):
        pass
    # юзаем га и находим веса (get_weights())
