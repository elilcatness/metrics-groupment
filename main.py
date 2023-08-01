import os
from string import punctuation as punct
from dotenv import load_dotenv

from src.interface import *
from src.utils import *
from src.metrics import s_metric


def main():
    phrases_filename = os.getenv('phrases_filename', 'phrases.txt')
    rest_filename = os.getenv('rest_filename', 'rest.csv')
    output_filename = os.getenv('output_filename', 'output.csv')
    phrases = get_phrases(phrases_filename)
    if not phrases:
        return print(f'Файл с фразами {phrases_filename} пуст или не существует!')
    min_k = get_min_k()
    round_digits_count = get_round_digits_count()
    rest_fieldnames = ['Phrases', 'Metrics', 'Similar phrase']
    output_fieldnames = ['Phrases', 'Metrics', 'Similar phrase', 'Group', 'Group_name']
    write_header(rest_filename, rest_fieldnames)
    write_header(output_filename, output_fieldnames)
    # groups, out = [], []
    groups_count = 0
    for i in range(len(phrases) - 1):
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
            continue
        else:
            groups_count += 1
        rows = []
        freq = dict()
        # words = dict()
        for k, item in enumerate([(phrases[i], 0)] + decent_phrases):
            ph, m_val = item
            if k > 0:
                rows.append({'Phrases': phrases[i], 'Metrics': round(m_val, round_digits_count),
                             'Similar phrase': ph, 'Group': groups_count})
            words = ph.split()
            processed_words = []
            for pos, word in enumerate(words):
                word = word.lower()
                if word not in processed_words:
                    freq[word] = freq.get(word, 0) + 1
                    processed_words.append(word)
        group_name = ' '.join([key for key, _ in sorted(
            freq.items(), key=lambda it: (
                -it[1],
                [ord(s) if s not in punct else punct.index(s) for s in it[0]]))])
        for row in rows:
            write_row(output_filename, output_fieldnames, {**row, 'Group_name': group_name})


if __name__ == '__main__':
    load_dotenv()
    main()
