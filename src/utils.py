from csv import DictWriter


def get_phrases(filename: str) -> list:
    try:
        with open(filename, encoding='utf-8') as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        return []


def write_header(filename: str, fieldnames: list, delimiter: str = ';'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        DictWriter(f, fieldnames, delimiter=delimiter).writeheader()


def write_row(filename: str, fieldnames: list, row: dict, delimiter: str = ';'):
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        DictWriter(f, fieldnames, delimiter=delimiter).writerow(row)


__all__ = ['get_phrases', 'write_header', 'write_row']
