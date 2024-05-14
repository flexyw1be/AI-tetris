import pygame

pygame.init()

# музыка
pygame.mixer.music.load("data/20.mp3")
SWITCH_SOUND = pygame.mixer.Sound('data/menu_switch.mp3')
CLEAR_LINE_SOUND = pygame.mixer.Sound('data/line.mp3')

SCORES_FONT = pygame.font.SysFont('Tahoma', 24)
MENU_FONT = pygame.font.SysFont('Tahoma', 40)

WIDTH = 700
HEIGHT = 650
LEFT = 200
TOP = 20

BLOCK_SIZE = 30
WIDTH_SIZE = 10
HEIGHT_SIZE = 20

FPS = 30

CLEAR_BONUS = 10

ICON = pygame.image.load('data/icon.png')  # path to icon
LOGO = "data/logo.jpg"

FIGURES = [
    [[3, 4, 5, 6], [5, 15, 25, 35]],
    [[4, 5, 14, 15], [4, 5, 14, 15]],
    [[4, 5, 15, 16], [5, 15, 14, 24]],
    [[5, 6, 14, 15], [5, 15, 16, 26]],
    [[5, 14, 15, 16], [5, 15, 16, 25], [4, 5, 6, 15], [5, 14, 15, 25]],
    [[4, 5, 6, 16], [5, 15, 25, 24], [4, 14, 15, 16], [5, 6, 15, 25]],
    [[14, 4, 5, 6], [4, 5, 15, 25], [6, 14, 15, 16], [5, 15, 25, 26]]
]

POINTS = {0:0, 1: 1000, 2: 2000, 3:6000, 4:24000}

# цвета
COLORS = [
    'DeepSkyBlue',
    'DarkViolet',
    'Salmon',
    'Cyan',
    'Yellow',
    'Crimson',
    'LimeGreen'
]

GRID_COLOR = BLOCKS_GRID_COLOR = 'DimGray'
BACKGROUND_COLOR = MENU_COLOR = 'white'
BLOCKS_COLOR = 'grey'

FITNESS_PATH = 'data/fitness.txt'
