from game import Game
from config import *

import pygame

if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('AI-Tetris')
    pygame.display.set_icon(ICON)
    display.fill(BACKGROUND_COLOR)
    g = Game(display)


# TODO:
# -до конца реализовать подсчет штрафа
# -реализовать подсчет очков
# -подготовить базу для ген. алгоритма (запись в файл, автоматические бекапы)
# -написать ген. алгоритм, для упорядочивания весов


# extra:
# - добавить музыку +
# - добавить режим на время
# - написать свой рандомайзер
# - отображать засуху
# - подкрутить sql

# 1 линия - 1000 очков
# 2 линии - 2000 очков
# 3 линии - 6000 очков
# 4 линии - 24000 очков
