from config import *
from utility import *
import pygame


class Finish:
    def __init__(self, display, score) -> None:
        self.running = True
        self.cur_text = SCORES_FONT.render('Press ENTER', True, 'darkgrey')
        self.text = MENU_FONT.render('YOU LOSE', True, 'black')
        self.score = MENU_FONT.render(f"Your score: {score}", True, 'black')
        self.display = display
        self.show()

    def show(self):
        while self.running:
            self.display.fill(MENU_COLOR)
            self.display.blit(self.cur_text, (270, 430))
            self.display.blit(self.score, (230, 330))
            self.display.blit(self.text, (250, 230))
            pygame.mixer.music.stop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running = False
            pygame.display.flip()
