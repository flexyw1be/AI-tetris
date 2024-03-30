import pygame
import copy
from config import *
from random import *
import peewee


class Menu():
    def __init__(self) -> None:
        pass


class HUD():
    def __init__(self) -> None:
        pass


def draw_grid(x: int, y: int) -> None:
    pygame.draw.rect(display, GRID_COLOR,
                     pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE), 1)


def draw_new_grid() -> None:
    pygame.draw.rect(display, GRID_COLOR,
                     pygame.Rect(LEFT + 11 * BLOCK_SIZE, 1 * BLOCK_SIZE + TOP, BLOCK_SIZE * 4, BLOCK_SIZE * 4), 2)


def draw_figure(x: int, y: int, color: str) -> None:
    pygame.draw.rect(display, color, pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(display, GRID_COLOR,
                     pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE), 2)


def draw_blocks(x: int, y: int) -> None:
    pygame.draw.rect(display, BLOCKS_COLOR,
                     pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(display, GRID_COLOR,
                     pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE), 2)


class Figure:

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        self.type = self.get_type()
        self.color = COLORS[self.type]
        self.rotation = randint(0, len(FIGURES[self.type]) - 1)
        self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])
        self.islife = True

    def get_type(self) -> int:
        return randint(0, len(FIGURES) - 1)

    def move_y(self):
        if not self.check(0, 1):
            return
        self.y += 1
        self.update()

    def rotate_right(self) -> None:
        self.rotation = self.rotation + 1
        if self.rotation > len(FIGURES[self.type]) - 1:
            self.rotation = 0
        self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])
        self.update()

    def update(self) -> None:
        for i in range(len(self.cords)):
            # print(self.cords)
            self.cords[i] = 10 * self.y + self.x + copy.deepcopy(FIGURES[self.type][self.rotation][i])

    def rotate_left(self) -> None:
        self.rotation = self.rotation - 1
        if self.rotation < 0:
            self.rotation = len(FIGURES[self.type]) - 1
        self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])
        self.update()

    def check(self, x: int, y: int) -> bool:
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
        self.update()

    def move_right(self):
        if not self.check(1, 0):
            return
        self.x += 1
        self.update()

    def add_block(self, lst: int, block: int) -> set:
        lst.add(block)
        return lst

    def __str__(self) -> list:
        return f'{self.cords}'


pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI-Tetris')
pygame.display.set_icon(ICON)
display.fill(BACKGROUND_COLOR)

list_of_blocks = set()

game_over = False
clock = pygame.time.Clock()

fps = 30

score = 0

clock.tick(fps)
g = 1.75
f = Figure(0, 0)
next_figure = Figure(0, 0)
counter = 0
dryness = 0 if f.type == 0 else 1
# g = 20

pressing_down = False
while not game_over:
    display.fill(BACKGROUND_COLOR)
    counter += 1
    if counter > 100000:
        counter = 0
    for i in range(20):
        for j in range(10):
            draw_grid(j, i)
            if i * 10 + j in f.cords:
                draw_figure(j, i, f.color)
            if i * 10 + j in next_figure.cords:
                draw_figure(j + 8, i + 2, next_figure.color)
            if i * 10 + j in list_of_blocks:
                draw_blocks(j, i)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                f.rotate_right()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                f.move_left()
            if event.key == pygame.K_RIGHT:
                f.move_right()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
    if counter % (fps // g) == 0 or pressing_down:
        f.move_y()
    if not f.islife:
        list_of_blocks.update(f.cords)
        f = next_figure
        next_figure = Figure(0, 0)
        if f.type == 0:
            dryness = 0
        else:
            dryness += 1
    # draw_new_grid()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()

# TODO:
# 1) рисовать сетку каждый проход цикла done
# 2) обработать коллизии (останавливать фигуры, удалять столбцы)
# 3) показывать следующую фигуру done 
# 4) начислять очки, изменять скорость
# 5) подкрутить sql
# 6) сделать меню и HUD


# 7) добавить искуственный интеллект!!!!

# extra:
# - добавить музыку
# - добавить режим на время
# - написать свой рандомайзер
# - отображать засуху
