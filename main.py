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


class Game():
    def __init__(self) -> None:
        pass

    def run(self) -> None:
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


def check_break_lines(lst: list, g: int, score: int) -> bool:
    lst = sorted(lst)
    for i in range(0, 191, 10):
        if (i + 9 in lst and i in lst) and lst.index(i + 9) - lst.index(i) == 9:
            for j in range(i, i + 10):
                lst.remove(j)
            line_go_down(i, lst)
            score += 1
            g = 1.75 + score // 30 * 2
    return lst, g, score


class Figure:

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        self.type = 0
        self.set_type()
        self.color = COLORS[self.type]
        self.rotation = randint(0, len(FIGURES[self.type]) - 1)
        self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])
        self.life = True

    def set_type(self) -> None:
        self.type = randint(0, len(FIGURES) - 1)

    def move_y(self, lst: list) -> None:
        if not self.check_y(1, lst):
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
        for n in range(len(self.cords)):
            self.cords[n] = 10 * self.y + self.x + copy.deepcopy(FIGURES[self.type][self.rotation][n])

    def intersects(self, lst: list, cords: list) -> bool:
        for cord in cords:
            if cord + 10 * self.y + self.x in lst:
                return False
        return True

    def check_rotate(self) -> bool:
        for cord in self.cords:
            if self.x + cord % 10 < 0 or self.x + cord % 10 > 9:
                return False
        return True

    def check_x(self, x: int, lst: list) -> bool:
        for cord in self.cords:
            if cord % 10 + x > 9 or cord % 10 + x < 0 or cord + x in lst:
                return False
        return True

    def check_y(self, y: int, lst: list) -> bool:
        for cord in self.cords:
            if (cord // 10 + y) // 20 >= 1 or cord + 10 * y in lst:
                self.add_block(lst, cord)
                self.life = False
                return False
        return True

    def move_x(self, x: int, lst: list) -> None:
        if not self.check_x(x, lst):
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

SCORES_FONT = pygame.font.SysFont('Tahoma', 24)

count_of_broken_lines = 0
count_of_figures = 0

clock.tick(FPS)
g = 1.75
f = Figure(0, 0)
next_figure = Figure(0, 0)
counter = 0
dryness = 0 if f.type == 0 else 1
# g = 20
pressing_down = False
flLeft = flRight = False
type1 = type2 = type3 = type4 = type5 = type6 = 0
while not game_over:
    display.fill(BACKGROUND_COLOR)
    scores_text = SCORES_FONT.render('scores: ' + str(score), False, 'darkGrey')
    figures_text = SCORES_FONT.render('figures: ' + str(count_of_figures), False, 'darkGrey')
    lines_text = SCORES_FONT.render('lines: ' + str(count_of_broken_lines), False, 'darkGrey')

    type1_text = SCORES_FONT.render('type 1: ' + str(type1), False, 'darkGrey')
    type2_text = SCORES_FONT.render('type 2: ' + str(type2), False, 'darkGrey')
    type3_text = SCORES_FONT.render('type 3: ' + str(type3), False, 'darkGrey')
    type4_text = SCORES_FONT.render('type 4: ' + str(type4), False, 'darkGrey')
    type5_text = SCORES_FONT.render('type 5: ' + str(type5), False, 'darkGrey')
    type6_text = SCORES_FONT.render('type 6: ' + str(type6), False, 'darkGrey')

    if dryness > 10:
        dryness_text = SCORES_FONT.render('dryness: ' + str(dryness), False, (255, 0, 0))
    else:
        dryness_text = SCORES_FONT.render('dryness: ' + str(dryness), False, 'darkGrey')

    # scores_rect = scores_text.get_rect()
    display.blit(scores_text, (20, 20))
    display.blit(figures_text, (20, 60))
    display.blit(lines_text, (20, 100))
    display.blit(dryness_text, (20, 140))

    display.blit(type1_text, (20, 180))
    display.blit(type2_text, (20, 210))
    display.blit(type3_text, (20, 240))
    display.blit(type4_text, (20, 270))
    display.blit(type5_text, (20, 300))
    display.blit(type6_text, (20, 330))

    counter = (counter + 1) % 100000

    for y in range(20):
        for x in range(10):
            draw_grid(x, y)
            if y * 10 + x in f.cords:
                draw_figure(x, y, f.color)
            if y * 10 + x in next_figure.cords:
                draw_figure(x + 8, y + 2, next_figure.color)
            if y * 10 + x in list_of_blocks:
                draw_blocks(x, y)

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
                f.move_x(-1, list_of_blocks)

            elif event.key == pygame.K_RIGHT:
                flRight = True
                f.move_x(1, list_of_blocks)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                flLeft = flRight = False
            if event.key == pygame.K_DOWN:
                pressing_down = False
    # if flLeft:
    #     f.move_x(-1)
    # elif flRight:
    #     f.move_x(1)
    if counter % (FPS // g) == 0 or pressing_down:
        f.move_y(list_of_blocks)
    if not f.life:
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

        if f.type == 1:
            type1 += 1
        elif f.type == 2:
            type2 += 1
        elif f.type == 3:
            type3 += 1
        elif f.type == 4:
            type4 += 1
        elif f.type == 5:
            type5 += 1
        elif f.type == 6:
            type6 += 1

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
