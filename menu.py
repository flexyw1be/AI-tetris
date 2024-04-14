from config import *
from utility import *
import pygame


class Menu():
    def __init__(self, display) -> None:

        self.logo = image_load(LOGO, (600, 174))

        self.button_list = [MENU_FONT.render('Play', True, 'black'), MENU_FONT.render('Quit', True, 'black')]
        self.running = True
        self.cur_text = SCORES_FONT.render('Press ENTER', True, 'darkgrey')
        self.display = display
        self.selected = 0
        self.show()

    def show(self):
        while self.running:
            self.display.fill(MENU_COLOR)
            self.display.blit(self.logo, (65, 70))
            self.display.blit(self.cur_text, (295, 450))

            pygame.draw.rect(self.display, 'darkGrey', pygame.Rect(20 + 300, 30 + self.selected * 60 + 300, 75, 50))
            for n, i in enumerate(self.button_list):
                if n > 0:
                    self.display.blit(i, (20 + 300, 100 + 40 * n + 250))
                else:
                    self.display.blit(i, (20 + 300, 100 + 40 * n + 230))

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
