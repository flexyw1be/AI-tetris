# система «штрафов» для расчета оптимального хода
height = -0.5  # высота
clears = 8  # очистка линии
holes = -7.5  # дырка
blockades = -3.5  # блокада
block = 50  # касание блока
wall = 0.05  # касание стены
floor = 50  # касание пола


def get_score(lst, cords):
    print("чистые линии: ", get_clear_lines(lst))
    print("высота: ", get_height(lst))
    print("дырки: ", get_holes(lst))
    print("блоки: ", get_taken_blocks(lst, cords))
    print("стены: ", get_taken_walls(lst))
    print("пол: ", get_taken_floor(lst))

    summ = height * get_height(lst) + \
           clears * get_clear_lines(lst) + \
           holes * get_holes(lst) + \
           block * get_taken_blocks(lst, cords) + \
           wall * get_taken_walls(lst) + \
           floor * get_taken_floor(lst)
    return summ


def get_taken_blocks(lst, cords):
    s = 0
    for i in cords:
        if 0 < i % 10 < 9:
            if i - 1 in lst and i - 1 not in cords:
                s += 1
            if i + 1 in lst and i + 1 not in cords:
                s += 1
        if i - 10 in lst and i - 10 not in cords:
            s += 1
        if i + 10 in lst and i + 10 not in cords:
            s += 1
    return s


def get_taken_walls(lst):
    summ = 0
    for i in lst:
        if i % 10 == 0:
            summ += 1
        if i % 10 == 9:
            summ += 1
    return summ


def get_taken_floor(lst):
    summ = 0
    for i in range(190, 200):
        if i in lst:
            summ += 1
    return summ


def get_holes(lst):
    return 0


def get_clear_lines(lst):
    return 0


def get_height(lst):
    return 20 - min(lst) // 10
