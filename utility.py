import pygame
from config import *
from random import randint


def image_load(path, size, alpha=True):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, size)
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


def draw_grid(display, x: int, y: int) -> None:
    pygame.draw.rect(display, GRID_COLOR,
                     pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE), 1)


def draw_new_grid(display) -> None:
    pygame.draw.rect(display, GRID_COLOR,
                     pygame.Rect(LEFT + 11 * BLOCK_SIZE, 1 * BLOCK_SIZE + TOP, BLOCK_SIZE * 4, BLOCK_SIZE * 4), 2)


def draw_figure(display, x: int, y: int, color: str) -> None:
    pygame.draw.rect(display, color, pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(display, GRID_COLOR,
                     pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE), 2)


def draw_blocks(display, x: int, y: int) -> None:
    pygame.draw.rect(display, BLOCKS_COLOR,
                     pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(display, GRID_COLOR,
                     pygame.Rect(LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE + TOP, BLOCK_SIZE, BLOCK_SIZE), 2)


def line_go_down(ind: int, lst: list) -> list:
    for i in range(0, ind):
        if i in lst:
            lst[lst.index(i)] += 10
    return lst


def check_break_lines(lst: list, g: int, score: int, lines: int) -> [list, int, int, int]:
    lst = sorted(lst)
    cnt = 0
    for i in range(0, 191, 10):
        if (i + 9 in lst and i in lst) and lst.index(i + 9) - lst.index(i) == 9:
            CLEAR_LINE_SOUND.play()
            for j in range(i, i + 10):
                lst.remove(j)
            line_go_down(i, lst)
            cnt += 1
            lines += 1
            g = 1.75 + lines // 30
    score += cnt ** 2 * CLEAR_BONUS
    return lst, g, score, lines

