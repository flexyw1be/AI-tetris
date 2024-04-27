# система «штрафов» для расчета оптимального хода
height = -1000  # высота
clears = 8  # очистка линии
holes = -7.5  # дырка
blockades = -3.5  # блокада
block = 4  # касание блока
wall = -500  # касание стены
floor = 5


def get_score(lst, cords, y):
    cords = [i + y * 10 for i in cords]
    print("чистые линии: ", get_clear_lines(lst))
    print("высота: ", get_height(lst, cords))
    print("дырки: ", get_holes(lst))
    print("блоки: ", get_taken_blocks(lst, cords))
    print("стены: ", get_taken_walls(lst, cords))
    print("пол: ", get_taken_floor(lst, cords))

    summ = height * get_height(lst, cords) + \
           clears * get_clear_lines(lst) + \
           holes * get_holes(lst) + \
           block * get_taken_blocks(lst, cords) + \
           wall * get_taken_walls(lst, cords) + \
           floor * get_taken_floor(lst, cords)
    print("штраф:", summ)
    return summ


def get_taken_blocks(lst, cords):
    print(cords)
    s = set()
    for i in cords:
        if 0 < i % 10 < 9:
            if i - 1 in lst and i - 1 not in cords:
                s.add(i-1)
            if i + 1 in lst and i + 1 not in cords:
                s.add(i+1)
        if i - 10 in lst and i - 10 not in cords:
            s.add(i-10)
        if i + 10 in lst and i + 10 not in cords:
            s.add(i+10)
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


def get_holes(lst):
    return 0


def get_clear_lines(lst):
    return 0


def get_height(lst, cords):
    return 20 -min(cords) // 10
