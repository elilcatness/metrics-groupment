import os

from dotenv import load_dotenv

from src.interface import get_min_k
from src.utils import get_phrases
from src.metrics import s_metric


def main():
    phrases_filename = os.getenv('phrases_filename', 'phrases.txt')
    phrases = get_phrases(phrases_filename)
    if not phrases:
        return print(f'Файл с фразами {phrases_filename} пуст или не существует!')
    min_k = get_min_k()


if __name__ == '__main__':
    load_dotenv()
    main()
