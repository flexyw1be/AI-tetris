import pygame
import copy

from nltk.metrics import scores
from config import *
from random import *


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


def line_go_down(ind: int, lst: list) -> list:
    for i in range(0, ind):
        if i in lst:
            lst[lst.index(i)] += 10
    return lst


def check_break_lines(lst: list, g: int, score: int):
    lst = sorted(lst)
    for i in range(0, 191, 10):
        if (i + 9 in lst and i in lst) and lst.index(i + 9) - lst.index(i) == 9:
            for j in range(i, i + 10):
                lst.remove(j)
            line_go_down(i, lst)
            score += 1
            g = 1.75 + score//30 * 2
    return lst, g, score


class Figure:

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        self.type = self.get_type()
        # self.type = 0
        self.color = COLORS[self.type]
        self.rotation = randint(0, len(FIGURES[self.type]) - 1)
        self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])
        self.islife = True

    def get_type(self) -> int:
        return randint(0, len(FIGURES) - 1)

    def move_y(self):
        if not self.check_y(1, list_of_blocks):
            return
        self.y += 1
        self.update()

    def rotate_right(self) -> None:
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % len(FIGURES[self.type])

        self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])
        if not self.intersects(list_of_blocks, self.cords) or not self.check_rotate():
            self.rotation = old_rotation
            self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])

        self.update()

    def update(self) -> None:
        for i in range(len(self.cords)):
            self.cords[i] = 10 * self.y + self.x + copy.deepcopy(FIGURES[self.type][self.rotation][i])

    def intersects(self, lst: list, cords: list) -> bool:
        for i in cords:
            if i + 10 * self.y + self.x in lst:
                return False
        return True

    def check_rotate(self):
        for i in self.cords:
            if self.x + i % 10 < 0 or self.x + i % 10 > 9:
                return False
        return True

    def check_x(self, x: int, lst: list) -> bool:
        for i in self.cords:
            if i % 10 + x > 9 or i % 10 + x < 0 or i + x in lst:
                return False
        return True

    def check_y(self, y: int, lst: list):
        for i in self.cords:
            if (i // 10 + y) // 20 >= 1 or i + 10 * y in lst:
                self.add_block(list_of_blocks, i)
                self.islife = False
                return False
        return True

    def move_x(self, x: int):
        if not self.check_x(x, list_of_blocks):
            return
        self.x += x
        self.update()

    def add_block(self, lst: list, block: int) -> list:
        lst.append(block)
        return lst

    def __str__(self) -> str:
        return f'{self.cords}'


pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI-Tetris')
pygame.display.set_icon(ICON)
display.fill(BACKGROUND_COLOR)

list_of_blocks = []

score = 0

game_over = False
clock = pygame.time.Clock()

SCORES_FONT = pygame.font.SysFont('arial', 40)

count_of_broken_lines = 0
count_of_figures = 1

clock.tick(FPS)
g = 1.75
f = Figure(0, 0)
next_figure = Figure(0, 0)
counter = 0
dryness = 0 if f.type == 0 else 1
# g = 20
pressing_down = False
flLeft = flRight = False
while not game_over:
    display.fill(BACKGROUND_COLOR)
    scores_text = SCORES_FONT.render('Scores: ' + str(score), False, (255, 0, 0))
    scores_rect = scores_text.get_rect()
    display.blit(scores_text, scores_rect)

    counter = (counter + 1) % 100000

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
                flLeft = True

            elif event.key == pygame.K_RIGHT:
                flRight = True

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                flLeft = flRight = False
            if event.key == pygame.K_DOWN:
                pressing_down = False
    if flLeft:
        f.move_x(-1)
    elif flRight:
        f.move_x(1)
    if counter % (FPS // g) == 0 or pressing_down:
        f.move_y()
    if not f.islife:
        list_of_blocks.extend(f.cords)
        list_of_blocks = list(set(list_of_blocks))
        f = next_figure
        next_figure = Figure(0, 0)
        count_of_figures += 1
        list_of_blocks, g, score = check_break_lines(list_of_blocks, g, score)
        if f.type == 0:
            dryness = 0
        else:
            dryness += 1

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()

# TODO:
# 1) рисовать сетку каждый проход цикла done
# 2) обработать коллизии (останавливать фигуры, удалять столбцы) ДАН
# 3) показывать следующую фигуру done
# 4) начислять очки, изменять скорость (работаем)
# 5) подкрутить sql (?????)
# 6) сделать меню и HUD


# 7) добавить искуственный интеллект!!!!

# extra:
# - добавить музыку (какую нахуй музыку)
# - добавить режим на время
# - написать свой рандомайзер
# - отображать засуху
