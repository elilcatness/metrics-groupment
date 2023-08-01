import os
from string import punctuation as punct
from dotenv import load_dotenv

from alive_progress import alive_bar

from src.interface import *
from src.utils import *
from src.metrics import s_metric
from src.constants import MASK_MODES, DEFAULT_MASK_MODE


def main():
    phrases_filename = os.getenv('phrases_filename', 'phrases.txt')
    rest_filename = os.getenv('rest_filename', 'rest.csv')
    output_filename = os.getenv('output_filename', 'output.csv')
    phrases = get_phrases(phrases_filename)
    if not phrases:
        return print(f'Файл с фразами {phrases_filename} пуст или не существует!')
    min_k = get_min_k()
    round_digits_count = get_round_digits_count()
    mask_mode = None
    while mask_mode is None:
        try:
            s = input('Выберите режим для маски '
                      f'(для значения по умолчанию {DEFAULT_MASK_MODE} '
                      'нажмите Enter):\n' +
                      '\n'.join([f'{i + 1}. {MASK_MODES[i]}'
                                 for i in range(len(MASK_MODES))]) + '\n')
            if not s:
                mask_mode = DEFAULT_MASK_MODE
            else:
                idx = int(s) - 1
                assert idx >= 0
                mask_mode = MASK_MODES[idx]
        except (ValueError, IndexError, AssertionError):
            print(f'\nЧисло должно быть от 1 до {len(MASK_MODES)}\n')
    rest_fieldnames = ['Phrases', 'Metrics', 'Similar phrase']
    output_fieldnames = ['Phrases', 'Metrics', 'Similar phrase',
                         'Group', 'Group_name']
    write_header(rest_filename, rest_fieldnames)
    groups_count = 0
    total = len(phrases) - 1
    with alive_bar(total, title='Формирование групп') as bar:
        for i in range(total):
            decent_phrases = []
            max_phrase_out, max_val_out = None, 0
            for j in range(i + 1, len(phrases)):
                if (metric_val := s_metric(list(phrases[i]), list(phrases[j]))) >= min_k:
                    decent_phrases.append((phrases[j], metric_val))
                elif metric_val > max_val_out:
                    max_phrase_out, max_val_out = phrases[j], metric_val
            if not decent_phrases:
                write_row(rest_filename, rest_fieldnames,
                          {'Phrases': phrases[i], 'Metrics': round(max_val_out, round_digits_count),
                           'Similar phrase': max_phrase_out})
                bar()
                continue
            else:
                groups_count += 1
            rows = []
            freq = dict()  # dictionary of words' entry frequency
            common = dict()  # fixed-position frequencies
            phrases_count = len(decent_phrases) + 1
            mask_mode_parts = mask_mode.split()
            for k, item in enumerate([(phrases[i], 0)] + decent_phrases):
                ph, m_val = item
                if k > 0:
                    rows.append({'Phrases': phrases[i], 'Metrics': round(m_val, round_digits_count),
                                 'Similar phrase': ph, 'Group': groups_count})
                words = ph.split()
                words_count = len(words)
                processed_words = []
                for pos, word in enumerate(words):
                    word = word.lower()
                    if word not in processed_words:
                        freq[word] = freq.get(word, 0) + 1
                        processed_words.append(word)
                        if word not in common:
                            common[word] = {'phrases_count': 1}
                        else:
                            common[word]['phrases_count'] += 1
                        if 'sum' in mask_mode_parts:
                            common[word]['sum'] = common[word].get('sum', 0) + pos
                        # noinspection PyTypeChecker
                        common[word][pos] = common[word].get(pos, 0) + 1
            group_words = [key for key, _ in sorted(
                freq.items(), key=lambda it: (
                    -it[1],
                    [ord(s0) if s0 not in punct else punct.index(s0) for s0 in it[0]]))]
            group_name = ' '.join(group_words)
            mask_dict = dict()
            for mode, key, rule in [
                    ('max', 'Mask_Max',
                     lambda d: [(key, -val) for key, val in d[1].items()
                                if isinstance(key, int)]),
                    ('sum', 'Mask_Sum', lambda d: [d[1]['sum']])]:
                if mode in mask_mode_parts:
                    if key not in output_fieldnames:
                        output_fieldnames.append(key)
                    mask_words = []
                    tmp_group_words = group_words[:]
                    for mask_word, _ in get_mask_words(common, phrases_count, rule):
                        tmp_group_words.remove(mask_word)
                        mask_words.append(mask_word)
                    mask_dict[key] = (f'[{" ".join(mask_words)}] '
                                      if mask_words else '') + ' '.join(tmp_group_words)
            if i == 0:
                write_header(output_filename, output_fieldnames)
            for row in rows:
                output_row = {**row, 'Group_name': group_name, **mask_dict}
                write_row(output_filename, output_fieldnames, output_row)
            bar()


if __name__ == '__main__':
    load_dotenv()
    main()
