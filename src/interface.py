# Get metric entry threshold for phrase to be included in a group
def get_min_k():
    while True:
        try:
            min_k = float(input('Укажите минимальное значение для включения фразы в группу: '))
            assert 0 <= min_k <= 1
            return min_k
        except (ValueError, AssertionError):
            print('Значение должно быть вещественным числом в диапазоне от 0 до 1')
