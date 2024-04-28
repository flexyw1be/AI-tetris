def get_holes(lst):
    s = 0
    for i in range(1, 200):
        if i > 189:
            if i % 10 == 9:
                if i - 10 in lst and i - 1 in lst and i not in lst:
                    s += 1
            elif i % 10 == 0:
                if i - 10 in lst and i + 1 in lst and i not in lst:
                    s += 1
            else:
                if i - 10 in lst and i + 1 in lst and i - 1 in lst and i not in lst:
                    s += 1
        else:
            if i % 10 == 9:
                if i - 10 in lst and i + 10 in lst and i - 1 in lst and i not in lst:
                    s += 1
            elif i % 10 == 0:
                if i - 10 in lst and i + 10 in lst and i + 1 in lst and i not in lst:
                    s += 1
            else:
                if i - 10 in lst and i + 10 in lst and i + 1 in lst and i - 1 in lst and i not in lst:
                    s += 1
    return s


# print([x for x in range(170, 200)])
s = [170, 171, 172, 173, 174, 176, 177, 178, 179, 180, 181, 182, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194,
     195, 196, 198, 199]
print(get_holes(s))
