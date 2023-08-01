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


def get_mask_words(common: dict, phrases_count: int, key=None, reverse: bool = False):
    return sorted([d for d in common.items()
                   if d[1]['phrases_count'] >= phrases_count],
                  key=key, reverse=reverse)


__all__ = ['get_phrases', 'write_header', 'write_row', 'get_mask_words']
