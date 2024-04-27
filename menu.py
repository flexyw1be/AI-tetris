from config import *
from utility import *
import pygame


class Menu:
    def __init__(self, display) -> None:

        self.logo = image_load(LOGO, (600, 174))

        self.button_list = [MENU_FONT.render('AI mode', True, 'black'), MENU_FONT.render('Play', True, 'black'),
                            MENU_FONT.render('Quit', True, 'black')]
        self.running = True
        self.cur_text = SCORES_FONT.render('Press ENTER', True, 'darkgrey')
        self.display = display
        self.selected = 0
        self.mode = 1
        self.show()

    def show(self):
        while self.running:
            self.display.fill(MENU_COLOR)
            self.display.blit(self.logo, (65, 70))
            self.display.blit(self.cur_text, (270, 430))

            pygame.draw.rect(self.display, 'SpringGreen', pygame.Rect(250, 270 + self.selected * 50 + 5, 40, 40))
            pygame.draw.rect(self.display, 'black', pygame.Rect(250, 270 + self.selected * 50 + 5, 40, 40), 3)

            for n, i in enumerate(self.button_list):
                self.display.blit(i, (300, 270 + 50 * n))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if self.selected + 1 < len(self.button_list):
                            self.selected += 1
                    if event.key == pygame.K_UP:
                        if self.selected - 1 >= 0:
                            self.selected -= 1
                    if event.key == pygame.K_RETURN:
                        if self.selected == 1:
                            self.mode = 1
                            pygame.mixer.music.play(-1)
                        elif self.selected == 0:
                            self.mode = 0
                            pygame.mixer.music.play(-1)
                        else:
                            quit()
                        self.running = False
            pygame.display.flip()
