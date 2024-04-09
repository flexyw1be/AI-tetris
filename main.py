import pygame
import copy

from nltk.metrics import scores
from config import *
from random import *


class Menu():
    def __init__(self) -> None:
        self.button_list = [MENU_FONT.render('Play', True, 'black'), MENU_FONT.render('Quit', True, 'black')]
        self.running = True
        self.cur_text = SCORES_FONT.render('Press ENTER', True, 'darkgrey')


        self.selected = 0
        self.show()

    def show(self):
        while self.running:
            display.fill(MENU_COLOR)
            display.blit(self.cur_text, (295, 450))

            pygame.draw.rect(display, 'darkGrey', pygame.Rect(20 + 300, 30 + self.selected * 60 + 300, 75, 50))
            for n, i in enumerate(self.button_list):
                if n > 0:
                    display.blit(i, (20 + 300, 100 + 40 * n + 250))
                else:
                    display.blit(i, (20 + 300, 100 + 40 * n + 230))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if self.selected + 1 < len(self.button_list):
                            self.selected += 1
                    if event.key == pygame.K_UP:
                        if self.selected - 1 >= 0:
                            self.selected -= 1
                    if event.key == pygame.K_RETURN:
                        if self.selected == 0:
                            self.running = 0
                        else:
                            quit()
            pygame.display.flip()
        # pygame.quit()


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
        self.m = Menu()
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
                self.m = Menu()

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

    def rotate_right(self, lst) -> None:
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % len(FIGURES[self.type])

        self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])
        if not self.intersects(lst, self.cords) or not self.check_rotate():
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


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('AI-Tetris')
    pygame.display.set_icon(ICON)
    display.fill(BACKGROUND_COLOR)

    SCORES_FONT = pygame.font.SysFont('Tahoma', 24)
    MENU_FONT = pygame.font.SysFont('Tahoma', 40)

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
