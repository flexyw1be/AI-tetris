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
# 1) реализовать подсчет штрафа
# 2) написать ген. алгоритм, для упорядочивания весов


# extra:
# - добавить музыку
# - добавить режим на время
# - написать свой рандомайзер
# - отображать засуху
# - подкрутить sql
