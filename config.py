import pygame

WIDTH = 700
HEIGHT = 650
FPS = 10
BLOCK_SIZE = 30

LEFT = 200
TOP = 20

WIDTH_SIZE = 10
HEIGHT_SIZE = 20


ICON = pygame.image.load('data/icon.png')  # path to icon

FIGURES = [
    [[3, 4, 5, 6], [5, 15, 25, 35]],
    [[4, 5, 14, 15], [4, 5, 14, 15]],
    [[4, 5, 15, 16], [5, 15, 14, 24]],
    [[5, 6, 14, 15], [5, 15, 16, 26]],
    [[5, 14, 15, 16], [5, 15, 16, 25], [5, 6, 7, 16], [5, 14, 15, 25]],
    [[4, 5, 6, 16], [5, 15, 25, 24], [4, 14, 15, 16], [5, 6, 15, 25]],
    [[14, 4, 5, 6], [4, 5, 15, 25], [6, 14, 15, 16], [5, 15, 25, 26]]
]

COLORS = [
    'DeepSkyBlue',
    'DarkViolet',
    'Salmon',
    'Cyan',
    'Yellow',
    'Crimson',
    'LimeGreen'

]

GRID_COLOR = BLOCKS_GRID_COLOR = 'black'
BACKGROUND_COLOR = 'Snow'
BLOCKS_COLOR = 'grey'
