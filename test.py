def get_type():
    from random import shuffle
    tiles = list([0, 1, 2, 3, 4, 5, 6])
    while True:
        shuffle(tiles)
        for tile in tiles:
            return tile

for i in range(10):
    print(i)