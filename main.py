from config import *
from random import randint

from menu import Menu
from figure import Figure

import pygame
import copy


class HUD():
    def __init__(self) -> None:
        pass


class Game():
    def __init__(self) -> None:
        self.list_of_blocks = []
        self.score = 0
        self.game_over = False
        self.clock = pygame.time.Clock()

        self.count_of_broken_lines = 0
        self.count_of_figures = 0
        self.paused = True

        self.clock.tick(FPS)
        self.pause_text = MENU_FONT.render('Pause', True, 'black')
        self.cur_text = MENU_FONT.render('Press ENTER', True, 'darkgrey')
        self.space_text = SCORES_FONT.render('Press SPACE', True, 'darkgrey')

        self.g = 1.75
        self.f = Figure(0, 0)
        self.next_figure = Figure(0, 0)
        self.counter = 0
        self.dryness = 0 if self.f.type == 0 else 1

        self.pressing_down = False
        self.flLeft = self.flRight = False

        self.scores_text = SCORES_FONT.render('scores: ' + str(self.score), True, 'darkGrey')
        self.m = Menu(display)
        self.run()

    def start_game(self):
        self.list_of_blocks = []
        self.score = 0
        self.game_over = False
        self.clock = pygame.time.Clock()

        self.count_of_broken_lines = 0
        self.count_of_figures = 0
        self.paused = True

        self.clock.tick(FPS)
        self.pause_text = MENU_FONT.render('Pause', True, 'black')
        self.cur_text = MENU_FONT.render('Press ENTER', True, 'darkgrey')
        self.space_text = SCORES_FONT.render('Press SPACE', True, 'darkgrey')

        self.g = 1.75
        self.f = Figure(0, 0)
        self.next_figure = Figure(0, 0)
        self.counter = 0
        self.dryness = 0 if self.f.type == 0 else 1

        self.pressing_down = False
        self.flLeft = self.flRight = False

        self.scores_text = SCORES_FONT.render('scores: ' + str(self.score), True, 'darkGrey')

    def run(self) -> None:
        while not self.game_over:
            display.fill(BACKGROUND_COLOR)

            self.scores_text = SCORES_FONT.render('scores: ' + str(self.score), True, 'darkGrey')
            display.blit(self.scores_text, (20, 20))

            self.counter = (self.counter + 1) % 100000

            for y in range(20):
                for x in range(10):
                    draw_grid(x, y)
                    if y * 10 + x in self.f.cords:
                        draw_figure(x, y, self.f.color)
                    if y * 10 + x in self.next_figure.cords:
                        draw_figure(x + 8, y + 2, self.next_figure.color)
                    if y * 10 + x in self.list_of_blocks:
                        draw_blocks(x, y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.f.rotate_right(self.list_of_blocks)
                    if event.key == pygame.K_DOWN:
                        self.pressing_down = True
                    if event.key == pygame.K_LEFT:
                        self.flLeft = True
                        self.f.move_x(-1, self.list_of_blocks)
                    if event.key == pygame.K_SPACE:
                        self.pause()
                        self.paused = True

                    elif event.key == pygame.K_RIGHT:
                        self.flRight = True
                        self.f.move_x(1, self.list_of_blocks)
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        self.flLeft = self.flRight = False
                    if event.key == pygame.K_DOWN:
                        self.pressing_down = False
            self.check_lose()
            if self.counter % (FPS // self.g) == 0 or self.pressing_down:
                self.f.move_y(self.list_of_blocks)
            if not self.f.life:
                self.list_of_blocks.extend(self.f.cords)
                self.list_of_blocks = list(set(self.list_of_blocks))
                self.f = self.next_figure
                self.next_figure = Figure(0, 0)
                self.count_of_figures += 1
                self.list_of_blocks, self.g, self.score = check_break_lines(self.list_of_blocks, self.g, self.score)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    def check_lose(self):
        for i in self.list_of_blocks:
            if 4 <= i <= 7:
                self.start_game()
                self.m = Menu(display)

    def pause(self):
        while self.paused:
            display.fill(BACKGROUND_COLOR)
            display.blit(self.pause_text, (300, 250))
            display.blit(self.space_text, (287, 300))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused

            pygame.display.update()


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
            g = 1.75 + score // 30
    return lst, g, score


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('AI-Tetris')
    pygame.display.set_icon(ICON)
    display.fill(BACKGROUND_COLOR)
    #
    # SCORES_FONT = pygame.font.SysFont('Tahoma', 24)
    # MENU_FONT = pygame.font.SysFont('Tahoma', 40)

    g = Game()

# TODO:
# 4) начислять очки, изменять скорость (работаем)
# 5) подкрутить sql (?????)


# 7) добавить искуственный интеллект!!!!

# extra:
# - добавить музыку
# - добавить режим на время
# - написать свой рандомайзер
# - отображать засуху
