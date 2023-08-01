# Get metric entry threshold for phrase to be included in a group
from src.constants import ROUND_DIGITS_COUNT


def get_min_k():
    while True:
        try:
            min_k = float(input('Укажите минимальное значение для включения фразы в группу: '))
            assert 0 <= min_k <= 1
            return min_k
        except (ValueError, AssertionError):
            print('Значение должно быть вещественным числом в диапазоне от 0 до 1')


def get_round_digits_count():
    while True:
        round_digits_count = input(
            'Введите кол-во цифр после запятой '
            f'(для значения по умолчанию {ROUND_DIGITS_COUNT} нажмите Enter): ')
        if not round_digits_count:
            return ROUND_DIGITS_COUNT
        try:
            round_digits_count = int(round_digits_count)
            assert round_digits_count > 0
            return round_digits_count
        except (ValueError, AssertionError):
            print('Количество цифр должно быть натуральным')


__all__ = ['get_min_k', 'get_round_digits_count']
