import pygame
import copy
from config import *
from random import *


def draw_grid(x, y):
    pygame.draw.rect(display, GRID_COLOR,
                     pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE), 1)


def draw_figure(x, y, color):
    pygame.draw.rect(display, color, pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(display, GRID_COLOR,
                     pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE), 2)


class Figure:
    s = 'жопа'

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.type = self.get_type()
        self.color = COLORS[self.type]
        self.rotation = 0
        self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])
        self.islife = True

    def get_type(self):
        return randint(0, len(FIGURES) - 1)

    def move_y(self):
        if not self.check(0, 1):
            return
        self.y += 1
        for i in range(len(self.cords)):
            # print(self.cords)
            self.cords[i] = 10 * self.y + self.x + copy.deepcopy(FIGURES[self.type][self.rotation][i])

    def rotate_right(self):
        self.rotation = self.rotation + 1
        if self.rotation > len(FIGURES[self.type]) - 1:
            self.rotation = 0
        # self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])

    def rotate_left(self):
        self.rotation = self.rotation - 1
        if self.rotation < 0:
            self.rotation = len(FIGURES[self.type]) - 1
        # self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])

    def check(self, x, y):
        for i in self.cords:
            if i % WIDTH_SIZE + x >= WIDTH_SIZE or i % WIDTH_SIZE + x < 0:
                return False
            if (i // WIDTH_SIZE + y) // HEIGHT_SIZE >= 1:
                self.add_block(list_of_blocks, i)
                self.islife = False
                return False
        return True

        # TODO:
        # сделать проверку, можно ли походить в определенную клетку

    def move_left(self):
        if not self.check(-1, 0):
            return
        self.x -= 1

    def move_right(self):
        if not self.check(1, 0):
            return
        self.x += 1

    def add_block(self, lst: [int], block: int):
        lst.add(block)
        return lst

    def __str__(self):
        return f'{self.cords}'


pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI-Tetris')
pygame.display.set_icon(ICON)
display.fill(BACKGROUND_COLOR)

list_of_blocks = set()

game_over = False
clock = pygame.time.Clock()

fps = 3

clock.tick(fps)

f = Figure(0, 0)

while not game_over:
    display.fill(BACKGROUND_COLOR)
    f.move_y()
    for i in range(20):
        for j in range(10):
            draw_grid(j, i)
            if i * 10 + j in f.cords:
                draw_figure(j, i, f.color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                f.rotate_right()
            if event.key == pygame.K_DOWN:
                f.rotate_left()
            if event.key == pygame.K_LEFT:
                f.move_left()
            if event.key == pygame.K_RIGHT:
                f.move_right()
    if not f.islife:
        f.__del__()
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
