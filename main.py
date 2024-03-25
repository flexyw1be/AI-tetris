import pygame
import copy
from config import *
from random import *


class Figure:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.type = self.get_type()
        self.color = COLORS[self.type]
        self.rotation = 0
        self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])

    def get_type(self):
        return randint(0, len(FIGURES) - 1)

    def move_x(self):
        self.y += 1
        for i in range(len(self.cords)):
            # print(self.cords)
            self.cords[i] = 10 * self.y + copy.deepcopy(FIGURES[self.type][self.rotation][i])

    def move_right(self):
        self.rotation = self.rotation + 1
        if self.rotation > len(FIGURES[self.type]) - 1:
            self.rotation = 0
        # self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])

    def move_left(self):
        self.rotation = self.rotation - 1
        if self.rotation < 0:
            self.rotation = len(FIGURES[self.type]) - 1
        # self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])

    def check(self):
        pass
        # TODO:
        # сделать проверку, можно ли походить в определенную клетку


pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI-Tetris')
pygame.display.set_icon(ICON)
display.fill(BACKGROUND_COLOR)

game_over = False
clock = pygame.time.Clock()

fps = 5

clock.tick(fps)

f = Figure(0, 0)

while not game_over:
    display.fill(BACKGROUND_COLOR)
    f.move_x()
    for i in range(20):
        for j in range(10):
            if i * 10 + j in f.cords:
                # print(i, j)
                pygame.draw.rect(display, f.color, pygame.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(display, GRID_COLOR,
                                 pygame.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                f.move_right()
            if event.key == pygame.K_DOWN:
                f.move_left()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()

# TODO:
# 1) рисовать сетку каждый проход цикла
# 2) обработать коллизии (останавливать фигуры, удалять столбцы)
# 3) показывать следующую фигуру
# 4) начислять очки, изменять скорость
# 5) подкрутить sql
# 6) сделать меню и HUD


# 7) добавить искуственный интеллект!!!!

# extra:
# - добавить музыку
# - добавить режим на время
# - написать свой рандомайзер
# - отображать засуху
