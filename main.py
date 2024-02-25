import pygame
import copy
from config import *
from random import *


def get_figure():
    pass


class Figure:  # класс фигуры
    def __init__(self):
        self.vy, self.vx = 1, 0
        self.cords = copy.deepcopy(TETRIMINOS[randint(0, 1)])

    def update(self, figures):
        print(TETRIMINOS)
        if any([cord[1] >= 19 for cord in self.cords]):
            if figures:
                figures.extend(self.cords)
            else:
                figures = copy.deepcopy(self.cords)
            self.cords = copy.deepcopy(TETRIMINOS[randint(0, 1)])
            return figures


        for x, y in self.cords:
            pygame.draw.rect(display, '#CD5C5C',
                             pygame.Rect(x * BLOCK_SIZE + 100, y * BLOCK_SIZE + 20, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(display, 'DarkRed',
                             pygame.Rect(x * BLOCK_SIZE + 100, y * BLOCK_SIZE + 20, BLOCK_SIZE, BLOCK_SIZE), 4)

        for i in range(len(self.cords)):
            self.cords[i][1] += self.vy
            self.cords[i][0] += self.vx
        self.vx = 0

        return figures


# поле 20*10

class Game:  # класс игровой доски
    def __init__(self):
        self.figures = []

    def draw_grid(self):
        display.fill('white')
        for x in range(100, 100 + 10 * BLOCK_SIZE, BLOCK_SIZE):
            for y in range(20, 20 + BLOCK_SIZE * 20, BLOCK_SIZE):
                pygame.draw.rect(display, 'black', pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_blocks(self):
        if not self.figures:
            return
        for x, y in self.figures:
            pygame.draw.rect(display, 'grey',
                             pygame.Rect(x * BLOCK_SIZE + 100, y * BLOCK_SIZE + 20, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(display, 'DarkGrey',
                             pygame.Rect(x * BLOCK_SIZE + 100, y * BLOCK_SIZE + 20, BLOCK_SIZE, BLOCK_SIZE), 2)


pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))  # задаем размеры окна
pygame.display.update()
pygame.display.set_caption('Tetris')  # Добавляем название игры.

game_over = False  # Создаём переменную, которая поможет нам контролировать
g = Game()
f = Figure()
print(g.figures)
clock = pygame.time.Clock()
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
    g.figures = f.update(g.figures)
    # f.update()
    g.draw_blocks()
    pygame.display.flip()
    clock.tick(5)
pygame.quit()
