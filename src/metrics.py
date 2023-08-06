from logging import warning as log


# import numpy as np
#
#
# def s_metric(x, y):
#     # прямой проход
#     x1 = np.array(x).copy()
#     y1 = np.array(y).copy()
#     n1 = 0
#     for i in x1:
#         ind = np.where(i == y1)[0]
#         if len(ind) > 0:
#             y1 = np.delete(y1, ind[0], None)
#             n1 += 1
#         if y1.size == 0:
#             break
#     n1 /= len(x1) if len(x1) != 0 else 0
#     # обратный проход
#     x2 = np.array(x).copy()
#     y2 = np.array(y).copy()
#     n2 = 0
#     for i in y2:
#         ind = np.where(i == x2)[0]
#         if len(ind) > 0:
#             x2 = np.delete(x2, ind[0], None)
#             n2 += 1
#         if x2.size == 0:
#             break
#     n2 /= len(y2) if len(y2) != 0 else 0
#     return n1 * n2


def metric(s1: str, s2: str):
    log(f'Сравнение "{s1}" и "{s2}"')
    s1, s2 = s1.split(), s2.split()
    matched = 0
    if (len1 := len(s1)) <= (len2 := len(s2)):
        min_s, max_s = s1, s2
        min_len, max_len = len1, len2
    else:
        min_s, max_s = s2, s1
        min_len, max_len = len2, len1
    log(f'Обход по "{" ".join(min_s)}"')
    for i, word in enumerate(min_s[:], 1):
        log(f'{i}. {word}')
        if word in max_s:
            log(f'Удаляем первое вхождение "{word}" в "{" ".join(max_s)}"')
            s1.remove(word)
            s2.remove(word)
            matched += 1
        else:
            log(f'"{word}" нет в "{" ".join(max_s)}"')
        log(f'... {" ".join(min_s)} ...')
    log(f'Слов из "{" ".join(min_s)}" в "{" ".join(max_s)}" найдено: '
        f'{matched}/{min_len} = {(matched / min_len):.4f}')
    res = matched / min_len * matched / max_len
    log(f'Итого: {matched}/{min_len} * {matched}/{max_len} = '
        f'{matched / min_len:.4f} * {matched / max_len:.4f} = '
        f'{matched / min_len * matched / max_len:.4f}')
    return res
