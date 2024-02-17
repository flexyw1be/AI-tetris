import pygame


class Figure():
    def __init__(self):
        pass


class Board():
    def __init__(self):
        pass


pygame.init()

dis = pygame.display.set_mode((500, 400))
pygame.display.update()
pygame.display.set_caption('Змейка от Skillbox')  # Добавляем название игры.

game_over = False  # Создаём переменную, которая поможет нам контролировать

while not game_over:
    for event in pygame.event.get():
        print(event)  # Выводить в терминал все произошедшие события.

pygame.quit()
