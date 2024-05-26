from random import choice

from config import *

from figure import Figure
from utility import *
from ai import get_score
import copy


class Game:
    def __init__(self, display, weights) -> None:
        self.display = display
        self.list_of_blocks = []
        self.score = 0
        self.game_over = False
        self.figures_list = list(map(int, open('figures.txt', 'rt').read().split()))
        self.clock = pygame.time.Clock()
        self.weights = weights

        self.count_of_broken_lines = 0
        self.count_of_figures = 1

        self.clock.tick(FPS)

        self.g = 1.75
        self.f = Figure(0, 0, self.figures_list[0])
        self.figures_list = self.figures_list[1:]
        self.next_figure = Figure(0, 0, self.figures_list[0])
        self.figures_list = self.figures_list[1:]
        self.counter = 0

        self.pressing_down = False

        self.get_pos()
        self.ai_mode()

    def draw_field(self) -> None:
        for y in range(20):
            for x in range(10):
                draw_grid(self.display, x, y)
                if y * 10 + x in self.f.cords:
                    draw_figure(self.display, x, y, self.f.color)
                if y * 10 + x in self.next_figure.cords:
                    draw_figure(self.display, x + 8, y + 2, self.next_figure.color)
                if y * 10 + x in self.list_of_blocks:
                    draw_blocks(self.display, x, y)

    def ai_mode(self) -> None:
        while not self.game_over:
            self.display.fill(BACKGROUND_COLOR)
            self.counter = (self.counter + 1) % 1000
            self.pressing_down = True

            self.draw_field()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            if self.check_lose():
                self.game_over = True
            if self.counter % (FPS / self.g) == 0 or self.pressing_down:
                self.f.move_y(self.list_of_blocks)
            if not self.f.life:
                self.list_of_blocks.extend(self.f.cords)
                self.list_of_blocks = list(set(self.list_of_blocks))
                self.f = self.next_figure
                self.next_figure = Figure(0, 0, self.figures_list[0])
                self.figures_list = self.figures_list[1:]
                self.count_of_figures += 1
                self.list_of_blocks, self.g, self.score, self.count_of_broken_lines = check_break_lines(
                    self.list_of_blocks, self.g, self.score, self.count_of_broken_lines)
                self.get_pos()
            pygame.display.flip()
            self.clock.tick(900)
        return self.score

    def get_blocks_list(self) -> list:
        lst = copy.deepcopy(self.list_of_blocks)
        return lst

    def get_pos(self) -> None:
        scores = []
        lst = self.get_blocks_list()
        lst.extend([x for x in range(200, 210)])
        for rotation in range(len(FIGURES[self.f.type])):
            self.f.x = 0
            self.f.rotation = rotation
            self.f.update()
            l_border = min([cord % 10 for cord in self.f.cords])
            self.f.move_x(-l_border, self.list_of_blocks)
            for j in range(10):
                lst, y = self.get_list(self.get_blocks_list())
                scores.append([rotation, self.f.x, get_score(lst, self.f.cords, y, self.weights)])
                self.f.move_x(1, self.list_of_blocks)
        # print("ФИГУРА:", max(scores, key=lambda x: x[2]))
        rotation, x, score = max(scores, key=lambda x: x[2])
        self.f.rotation = rotation
        self.f.x = x
        self.f.update()

    def get_list(self, lst: list) -> [list, int]:
        cords, y = copy.deepcopy(self.f.cords), 0
        for y in range(20, -1, -1):
            if self.f.check_ai(y, lst):
                break
        for i in range(len(cords)):
            cords[i] += 10 * y
        lst.extend(cords)
        return lst, y

    def check_lose(self):
        for i in self.list_of_blocks:
            if 0 <= i <= 10:
                return True

    def __str__(self):
        return f'{self.score}'
