import main


def get_weights():
    height = -1000
    clears = 6000
    holes = -2000
    blockades = -900
    block = 300
    wall = 200
    floor = 1050
    weights = [height, clears, holes, blockades, block, wall, floor]
    # calculate weights with genetic algorithm
    return weights


_GENERATIONS = 10
_COUNT_OF_GAMES = 5
for generation in range(_GENERATIONS):
    scores = []
    for _ in range(_COUNT_OF_GAMES):
        pass
    # юзаем га и находим веса (get_weights())
