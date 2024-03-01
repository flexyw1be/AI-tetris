import pygame
import copy
from config import *
from random import *


class Figure:  # класс фигуры

    def __init__(self):
        self.vy, self.vx = 1, 0  # написать get_speed
        self.type, self.cords, self.moves, self.color = [], [], [], 0
        self.get_figure()

    def get_random_shape(self):  # написать какой то крутой алгос
        return randint(0, len(TETRIMINOS) - 1)

    def set_speed(self):
        self.vy, self.vx = 1, 0

    def get_figure(self):
        self.set_speed()
        self.type = self.get_random_shape()
        self.cords = copy.deepcopy(TETRIMINOS[self.type])
        self.moves = copy.deepcopy(MOVES[self.type])
        self.color = copy.deepcopy(COLORS[self.type])

    def copy_figure(self, figure):
        self.set_speed()
        self.type = figure.type
        self.cords = figure.cords
        self.moves = figure.moves
        self.color = figure.color
        self.move(-10, -3)

    def update(self, figures, next_figure, count):
        if any([cord[1] >= 19 for cord in self.cords]):
            if figures:
                figures.extend(self.cords)
            else:
                figures = copy.deepcopy(self.cords)
            self.copy_figure(next_figure)
            next_figure = Figure()
            next_figure.move(10, 3)
            count += 1
            # self.get_figure()
            return figures, next_figure, count

        self.draw_figure()
        self.move(self.vx, self.vy)

        return figures, next_figure, count

    def draw_figure(self):
        for x, y in self.cords:
            pygame.draw.rect(display, self.color[0],
                             pygame.Rect(x * BLOCK_SIZE + 100, y * BLOCK_SIZE + 20, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(display, self.color[1],
                             pygame.Rect(x * BLOCK_SIZE + 100, y * BLOCK_SIZE + 20, BLOCK_SIZE, BLOCK_SIZE), 4)

    def move(self, vx, vy):
        for i in range(len(self.cords)):
            self.cords[i][1] += vy
            self.cords[i][0] += vx
        self.set_speed()

    def rotate(self):
        for i in range(len(self.cords)):
            self.cords[i][0] += self.moves[i][0]
            self.cords[i][1] += self.moves[i][1]
        for i in range(len(self.cords)):
            self.moves[i] = [-1 * self.moves[i][0], -1 * self.moves[i][1]]
        print(self.moves)


import time


# поле 20*10

class Game:  # класс игровой доски
    def __init__(self):
        self.figures = []
        self.count = 1
        self.score = 0

    def draw_grid(self):
        display.fill(BACKGROUND_COLOR)
        text = font.render(str(self.count), False, 'black')
        display.blit(text, (545, 50))
        for x in range(100, 100 + 10 * BLOCK_SIZE, BLOCK_SIZE):
            for y in range(20, 20 + BLOCK_SIZE * 20, BLOCK_SIZE):
                pygame.draw.rect(display, GRID_COLOR, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

        for x in range(100 + 13 * BLOCK_SIZE, 100 + 13 * BLOCK_SIZE + BLOCK_SIZE * 4, BLOCK_SIZE):
            for y in range(20 + BLOCK_SIZE * 2, 20 + BLOCK_SIZE * 2 + BLOCK_SIZE * 4, BLOCK_SIZE):
                pygame.draw.rect(display, GRID_COLOR, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_blocks(self):
        for x, y in self.figures:
            pygame.draw.rect(display, BLOCKS_COLOR,
                             pygame.Rect(x * BLOCK_SIZE + 100, y * BLOCK_SIZE + 20, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(display, BLOCKS_GRID_COLOR,
                             pygame.Rect(x * BLOCK_SIZE + 100, y * BLOCK_SIZE + 20, BLOCK_SIZE, BLOCK_SIZE), 4)


pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))  # задаем размеры окна
pygame.display.update()
pygame.display.set_caption('AI-Tetris')
pygame.display.set_icon(ICON)
# Добавляем название игры.
# pygame.font.SysFont('arial', 24)
font = pygame.font.SysFont('serif', 24)

game_over = False  # Создаём переменную, которая поможет нам контролировать
g = Game()
f = Figure()
next_figure = Figure()
print(g.figures)
next_figure.move(10, 3)
next_figure.draw_figure()
clock = pygame.time.Clock()
g.draw_grid()
# clock.tick(20)
while not game_over:  # основной цикл игры
    g.draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                f.vx = -1
            elif event.key == pygame.K_RIGHT:
                f.vx = 1
            elif event.key == pygame.K_UP:
                f.rotate()
            elif event.key == pygame.K_DOWN:
                f.rotate()
    g.figures, next_figure, g.count = f.update(g.figures, next_figure, g.count)
    # f.update()
    next_figure.draw_figure()
    g.draw_blocks()
    pygame.display.flip()
    clock.tick(5)
pygame.quit()
