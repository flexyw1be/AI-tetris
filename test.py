import numpy as np


def get_type():
    from random import shuffle
    tiles = list([0, 1, 2, 3, 4, 5, 6])
    while True:
        shuffle(tiles)
        for tile in tiles:
            return tile


def get_random_weights():
    # return [HEIGHT, CLEARS, HOLES, BLOCKADES, BLOCK, WALL, FLOOR]
    return ' '.join(map(str, [np.random.randint(-1000, 0), np.random.randint(0, 1000), np.random.randint(-1000, 0),
                              np.random.randint(-1000, 0), np.random.randint(0, 1000), np.random.randint(0, 1000),
                              np.random.randint(0, 1000)]))

def get_type():
    return np.random.randint(0, 7)

for i in range(20):
    print(get_type())
# f = open("results.txt", 'rt').read().split('\n')
# mx = 0
# g = 0
# for i in f:
#     a = i.split()
#     if int(a[-1]) > mx:
#         mx = int(a[-1])
#         g = i
# print(g)