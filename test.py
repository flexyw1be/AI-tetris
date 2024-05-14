from config import *
from random import randint


f = open('1.txt', 'wt')
s = ''
for i in range(3000):
    g = randint(0, len(FIGURES) - 1)
    s += str(g) +' '
f.write(s)