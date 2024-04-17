from config import *

from menu import Menu
from figure import Figure
from finish import Finish
from utility import *


class Game:
    def __init__(self, display) -> None:

        self.display = display
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
        self.home_text = SCORES_FONT.render('Press ESCAPE to HOME', True, 'darkgrey')

        self.g = 1.75
        self.f = Figure(0, 0)
        self.next_figure = Figure(0, 0)
        self.counter = 0
        self.dryness = 0 if self.f.type == 0 else 1

        self.pressing_down = False
        self.flLeft = self.flRight = False

        self.scores_text = SCORES_FONT.render('scores: ' + str(self.score), True, 'darkGrey')
        self.m = Menu(self.display)
        print(self.m.mode)
        if self.m.mode == 0:
            self.ai_mode()
        else:
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

        self.scores_text = SCORES_FONT.render('scores: ' + str(self.score), True, 'darkGrey')

    def run(self) -> None:
        while not self.game_over:
            self.display.fill(BACKGROUND_COLOR)

            self.scores_text = SCORES_FONT.render('scores: ' + str(self.score), True, 'darkGrey')
            self.display.blit(self.scores_text, (20, 20))

            self.counter = (self.counter + 1) % 100000

            for y in range(20):
                for x in range(10):
                    draw_grid(self.display, x, y)
                    if y * 10 + x in self.f.cords:
                        draw_figure(self.display, x, y, self.f.color)
                    if y * 10 + x in self.next_figure.cords:
                        draw_figure(self.display, x + 8, y + 2, self.next_figure.color)
                    if y * 10 + x in self.list_of_blocks:
                        draw_blocks(self.display, x, y)
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

    def ai_mode(self):
        while not self.game_over:
            self.display.fill(BACKGROUND_COLOR)
            print(self.f.cords)
            self.counter = (self.counter + 1) % 100000
            self.scores_text = SCORES_FONT.render('scores: ' + str(self.score), True, 'darkGrey')
            self.display.blit(self.scores_text, (20, 20))

            for y in range(20):
                for x in range(10):
                    draw_grid(self.display, x, y)
                    if y * 10 + x in self.f.cords:
                        draw_figure(self.display, x, y, self.f.color)
                    if y * 10 + x in self.next_figure.cords:
                        draw_figure(self.display, x + 8, y + 2, self.next_figure.color)
                    if y * 10 + x in self.list_of_blocks:
                        draw_blocks(self.display, x, y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause()
                        self.paused = True
                    if event.key == pygame.K_LEFT:
                        self.flLeft = True
                        self.f.move_x(-1, self.list_of_blocks)
                    if event.key == pygame.K_RIGHT:
                        self.flLeft = True
                        self.f.move_x(1, self.list_of_blocks)

            self.check_lose()
            # if self.counter % (FPS // self.g) == 0 or self.pressing_down:
            #     self.f.move_y(self.list_of_blocks)
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
                self.f = Finish(self.display, self.score)
                self.start_game()
                self.m = Menu(self.display)
                if self.m.mode == 0:
                    self.ai_mode()
                else:
                    self.run()

    def pause(self):
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
                    elif event.key == pygame.K_ESCAPE:
                        self.m = Menu(self.display)
                        self.start_game()
                        if self.m.mode == 0:
                            self.ai_mode()
                        else:
                            self.run()

            pygame.display.update()
