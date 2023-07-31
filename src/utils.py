def get_phrases(filename: str) -> list:
    try:
        with open(filename, encoding='utf-8') as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        return []
