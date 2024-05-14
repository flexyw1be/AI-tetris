from random import choice

from config import *

from menu import Menu
from figure import Figure
from finish import Finish
from utility import *
from ai import get_score
import copy


class Game:
    def __init__(self, display) -> None:
        self.display = display
        self.list_of_blocks = []
        self.score = 0
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.fit = False

        self.count_of_broken_lines = 0
        self.count_of_figures = 1
        self.paused = True

        self.clock.tick(FPS)
        self.pause_text = MENU_FONT.render('Pause', True, 'black')
        self.cur_text = MENU_FONT.render('Press ENTER', True, 'darkgrey')
        self.space_text = SCORES_FONT.render('Press SPACE', True, 'darkgrey')
        self.home_text = SCORES_FONT.render('Press ESCAPE to HOME', True, 'darkgrey')

        self.g = 1.75
        self.f = Figure(0, 0)
        self.next_figure = Figure(0, 0)
        self.counter = 0
        self.dryness = 0 if self.f.type == 0 else 1

        self.pressing_down = False
        self.flLeft = self.flRight = False

        self.scores_text = SCORES_FONT.render('score: ' + str(self.score), True, GRID_COLOR)
        self.figures_text = SCORES_FONT.render('figures: ' + str(self.count_of_figures), True, GRID_COLOR)
        self.lines_text = SCORES_FONT.render('lines: ' + str(self.count_of_broken_lines), True, GRID_COLOR)
        self.m = Menu(self.display)
        if self.m.mode == 0:
            self.get_pos()
            self.ai_mode()
        else:
            self.player_mode()

    def start_game(self) -> None:
        pygame.mixer.music.play(-1)
        self.list_of_blocks = []
        self.score = 0
        self.game_over = False
        self.clock = pygame.time.Clock()

        self.count_of_broken_lines = 0
        self.count_of_figures = 0
        self.paused = True

        self.clock.tick(FPS)
        self.home_text = SCORES_FONT.render('Press ESCAPE to HOME', True, 'darkgrey')
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

        self.scores_text = SCORES_FONT.render('scores: ' + str(self.score), True, GRID_COLOR)
        self.figures_text = SCORES_FONT.render('figures: ' + str(self.count_of_figures), True, GRID_COLOR)
        self.lines_text = SCORES_FONT.render('lines: ' + str(self.count_of_broken_lines), True, GRID_COLOR)

    def events(self) -> None:
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
                    pygame.mixer.music.pause()
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

    def player_mode(self) -> None:
        while not self.game_over:
            self.display.fill(BACKGROUND_COLOR)
            self.hud()
            self.counter = (self.counter + 1) % 100000
            self.draw_field()
            self.events()
            self.check_lose()
            if self.counter % (FPS // self.g) == 0 or self.pressing_down:
                self.f.move_y(self.list_of_blocks)
            if not self.f.life:
                self.list_of_blocks.extend(self.f.cords)
                self.list_of_blocks = list(set(self.list_of_blocks))
                self.f = self.next_figure
                self.next_figure = Figure(0, 0)
                self.count_of_figures += 1
                self.list_of_blocks, self.g, self.score, self.count_of_broken_lines = check_break_lines(self.list_of_blocks, self.g, self.score, self.count_of_broken_lines)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    def hud(self) -> None:
        self.scores_text = SCORES_FONT.render('score: ' + str(self.score), True, GRID_COLOR)
        self.figures_text = SCORES_FONT.render('figures: ' + str(self.count_of_figures), True, GRID_COLOR)
        self.lines_text = SCORES_FONT.render('lines: ' + str(self.count_of_broken_lines), True, GRID_COLOR)
        self.display.blit(self.scores_text, (20, 20))
        self.display.blit(self.figures_text, (20, 80))
        self.display.blit(self.lines_text, (20, 50))

    def ai_mode(self) -> None:
        while not self.game_over:
            self.display.fill(BACKGROUND_COLOR)
            self.counter = (self.counter + 1) % 1000
            self.hud()
            self.pressing_down = True

            self.draw_field()
            self.events()
            self.check_lose()
            if self.counter % (FPS / self.g) == 0 or self.pressing_down:
                self.f.move_y(self.list_of_blocks)
            if not self.f.life:
                self.list_of_blocks.extend(self.f.cords)
                self.list_of_blocks = list(set(self.list_of_blocks))
                self.f = self.next_figure
                self.next_figure = Figure(0, 0)
                self.count_of_figures += 1
                self.list_of_blocks, self.g, self.score, self.count_of_broken_lines = check_break_lines(self.list_of_blocks, self.g, self.score, self.count_of_broken_lines)
                self.get_pos()
            pygame.display.flip()
            self.clock.tick(900)
        pygame.quit()

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
                scores.append([rotation, self.f.x, get_score(lst, self.f.cords, y)])
                self.f.move_x(1, self.list_of_blocks)
        print("ФИГУРА:", max(scores, key=lambda x: x[2]))
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

    def check_lose(self) -> None:
        if self.fit:
            return self.score
        for i in self.list_of_blocks:
            if 0 <= i <= 10:
                self.f = Finish(self.display, self.count_of_broken_lines)
                self.start_game()
                # self.m = Menu(self.display)
                if self.m.mode == 0:
                    self.ai_mode()
                else:
                    self.player_mode()

    def pause(self) -> None:
        while self.paused:
            self.display.fill(BACKGROUND_COLOR)
            self.display.blit(self.pause_text, (300, 250))
            self.display.blit(self.space_text, (287, 300))
            self.display.blit(self.home_text, (227, 335))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                        pygame.mixer.music.unpause()
                    elif event.key == pygame.K_ESCAPE:
                        self.m = Menu(self.display)
                        self.start_game()
                        if self.m.mode == 0:
                            self.ai_mode()
                        else:
                            self.player_mode()

            pygame.display.update()

    def __str__(self):
        return f'{self.score}'
