import numpy.random

from config import *
from random import *
import pygame
import numpy as np
import copy


class Figure:

    def __init__(self, x: int, y: int, type=12) -> None:
        self.x, self.y = x, y
        # if type !=12:
        # self.type = self.get_type()
        #     print(1)
        # else:
        self.type = type
        # print(self.type)
        # self.set_type()
        self.color = COLORS[self.type]
        self.rotation = randrange(0, len(FIGURES[self.type]) - 1)
        self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])
        self.life = True

    def get_type(self):
        return numpy.random.randint(0, 7)

    def set_type(self) -> None:
        self.type = randrange(0, len(FIGURES) - 1)

    def move_y(self, lst: list) -> None:
        if not self.check_y(1, lst):
            return
        self.y += 1
        self.update()

    def rotate_right(self, lst: list) -> None:
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % len(FIGURES[self.type])

        self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])
        if not self.intersects(lst, self.cords) or not self.check_rotate():
            self.rotation = old_rotation
            self.cords = copy.deepcopy(FIGURES[self.type][self.rotation])

        self.update()

    def update(self) -> None:
        for n in range(len(self.cords)):
            self.cords[n] = 10 * self.y + self.x + copy.deepcopy(FIGURES[self.type][self.rotation][n])

    def intersects(self, lst: list, cords: list) -> bool:
        for cord in cords:
            if cord + 10 * self.y + self.x in lst:
                return False
        return True

    def check_rotate(self) -> bool:
        for cord in self.cords:
            if self.x + cord % 10 < 0 or self.x + cord % 10 > 9:
                return False
        return True

    def check_x(self, x: int, lst: list):
        for cord in self.cords:
            if cord + x in lst or cord % 10 + x < 0 or cord % 10 + x > 9:
                return False
        return x

    def check_ai(self, y: int, lst: list) -> bool:
        g = set([cord % 10 for cord in self.cords])
        for cord in self.cords:
            if cord + 10 * y in lst or (cord // 10 + y) // 20 >= 1:
                return False
        for x in range(min(g), max(g) + 1):
            for y1 in range(y + 1):
                if y1 * 10 + x in lst:
                    return False

        return True

    def check_y(self, y: int, lst: list) -> bool:
        for cord in self.cords:
            if cord + 10 * y in lst:
                self.add_block(lst, cord)
                self.life = False
                return False
            if (cord // 10 + y) // 20 >= 1:
                self.add_block(lst, cord)
                self.life = False
                return False
        return True

    def move_x(self, x: int, lst: list) -> None:
        if not self.check_x(x, lst):
            return
        self.x += x
        self.update()

    def add_block(self, lst: list, block: int) -> list:
        lst.append(block)
        return lst

    def __str__(self) -> str:
        return f'{self.cords}'
