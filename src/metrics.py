import numpy as np


def s_metric(x, y):
    # прямой проход
    x1 = np.array(x).copy()
    y1 = np.array(y).copy()
    n1 = 0
    for i in x1:
        ind = np.where(i == y1)[0]
        if len(ind) > 0:
            y1 = np.delete(y1, ind[0], None)
            n1 += 1
        if y1.size == 0:
            break
    n1 /= len(x1) if len(x1) != 0 else 0
    # обратный проход
    x2 = np.array(x).copy()
    y2 = np.array(y).copy()
    n2 = 0
    for i in y2:
        ind = np.where(i == x2)[0]
        if len(ind) > 0:
            x2 = np.delete(x2, ind[0], None)
            n2 += 1
        if x2.size == 0:
            break
    n2 /= len(y2) if len(y2) != 0 else 0
    return n1 * n2
