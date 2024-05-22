# система «штрафов» для расчета оптимального хода
height = 100  # высота
clears = 6000  # очистка линии
holes = -2000  # дырка
blockades = -900  # блокада
block = 300  # касание блока
wall = 200  # касание стены
floor = 1050


def get_weights():
    return [height, clears, holes, blockades, block, wall, floor]


def get_score(lst: list, cords: list, y: int, weights) -> int:
    height, clears, holes, blockades, block, wall, floor = weights
    cords = [i + y * 10 for i in cords]
    # print("чистые линии: ", get_clear_lines(lst))
    # print("высота: ", get_height(lst, cords))
    # print("дырки: ", get_holes(lst, cords))
    # print("блоки: ", get_taken_blocks(lst, cords))
    # print("стены: ", get_taken_walls(lst, cords))
    # print("пол: ", get_taken_floor(lst, cords))

    summ = height * get_height(lst, cords) + \
           clears * get_clear_lines(lst) + \
           holes * get_holes(lst, cords) + \
           block * get_taken_blocks(lst, cords) + \
           wall * get_taken_walls(lst, cords) + \
           floor * get_taken_floor(lst, cords) + \
           blockades * get_blockades(lst, cords)
    # print("штраф:", summ)
    return summ


def get_blockades(lst:list, cords:list) -> int:
    s = 0
    for cord in cords:
        if cord // 10 <= 18:
            if cord + 10 not in lst and cord + 20 not in lst:
                s += 1
    return s


def get_taken_blocks(lst, cords):
    # print(cords)
    s = set()
    for i in cords:
        if 0 < i % 10 < 9:
            if i - 1 in lst and i - 1 not in cords:
                s.add(i - 1)
            if i + 1 in lst and i + 1 not in cords:
                s.add(i + 1)
        if i - 10 in lst and i - 10 not in cords:
            s.add(i - 10)
        if i + 10 in lst and i + 10 not in cords:
            s.add(i + 10)
    return len(s)


def get_taken_walls(lst, cords):
    summ = 0
    for i in cords:
        if i % 10 == 0:
            summ += 1
        if i % 10 == 9:
            summ += 1
    return summ


def get_taken_floor(lst, cords):
    summ = 0
    for i in range(190, 200):
        if i in cords:
            summ += 1
    return summ


def get_holes(lst, cords):
    s = 0
    for cord in cords:
        if cord // 10 < 19:
            if cord + 10 not in lst:
                s += 1
    return s

    # s = 0
    # for i in range(1, 190):
    #     if i > 189:
    #         if i % 10 == 9:
    #             if i - 10 in lst and i - 1 in lst and i not in lst:
    #                 s += 1
    #         elif i % 10 == 0:
    #             if i - 10 in lst and i + 1 in lst and i not in lst:
    #                 s += 1
    #         else:
    #             if i - 10 in lst and i + 1 in lst and i - 1 in lst and i not in lst:
    #                 s += 1
    #     else:
    #         if i % 10 == 9:
    #             if i - 10 in lst and i + 10 in lst and i - 1 in lst and i not in lst:
    #                 s += 1
    #         elif i % 10 == 0:
    #             if i - 10 in lst and i + 10 in lst and i + 1 in lst and i not in lst:
    #                 s += 1
    #         else:
    #             if i - 10 in lst and i + 10 in lst and i + 1 in lst and i - 1 in lst and i not in lst:
    #                 s += 1
    # return s


def get_clear_lines(lst):
    s = 0
    lst = sorted(lst)
    for i in range(0, 191, 10):
        if (i + 9 in lst and i in lst) and lst.index(i + 9) - lst.index(i) == 9:
            s += 2
    return s


def get_height(lst, cords):
    return sum([20 - x // 10 for x in cords])
