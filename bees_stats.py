import re
from collections import Counter, defaultdict
from csv import DictWriter, DictReader
from itertools import groupby
from operator import itemgetter
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from bees import BeesProblem, BeesFitnessCalculator


def main():
    plt.switch_backend('TkAgg')
    stats_path = Path('bees_stats.csv')
    all_size_counts = count_stats(stats_path)

    colours = dict(touching='b', redeal='r')
    fig, axes_table = plt.subplots(4, 4, sharex='all', sharey='all')
    for (pips, queen, blanks), size_counts in all_size_counts.items():
        sizes = []
        counts = []
        prev_size = -2
        for size, count in sorted(size_counts.items()):
            prev_size += 1
            while prev_size < size:
                sizes.append(prev_size)
                counts.append(0)
                prev_size += 1
            sizes.append(size)
            counts.append(count)
        axes: Axes = axes_table[pips-3][queen-3]
        axes.plot(sizes, counts, colours[blanks])
        axes.set_title(f'{pips} pips with {queen} queen', fontsize='small')

    for pips in range(3, 7):
        for queen in range(3, 7):
            if queen > pips:
                axes = axes_table[pips-3][queen-3]
                axes.set_frame_on(False)
                axes.tick_params(bottom=False, left=False)

    plt.tight_layout()
    plt.show()


def count_stats(stats_path: Path) -> dict:
    all_size_counts = defaultdict(Counter)  # {(pips, queen, blanks): {size: count}}
    try:
        with stats_path.open() as counts_file:
            reader = DictReader(counts_file)
            for (pips, queen, blanks), rows in groupby(reader,
                                                       itemgetter('pips',
                                                                  'queen',
                                                                  'blanks')):
                pips = int(pips)
                queen = int(queen)
                size_counts = all_size_counts[(pips, queen, blanks)]
                for row in rows:
                    size = int(row['solution'])
                    count = int(row['count'])
                    size_counts[size] += count
    except FileNotFoundError:
        pass

    write_missing_counts(all_size_counts, stats_path)
    return all_size_counts


def write_missing_counts(all_size_counts: dict, stats_path: Path):
    new_stats_path = stats_path.with_suffix('.new.csv')
    assert not new_stats_path.exists()
    calculator = BeesFitnessCalculator()
    was_data_missing = False
    stats_columns = ['pips', 'queen', 'blanks', 'solution', 'count']
    target_count = 1000
    with new_stats_path.open('w') as counts_file:
        writer = DictWriter(counts_file, stats_columns)
        for blanks in ('touching', 'redeal'):
            for max_pips in range(3, 7):
                init_params = dict(max_pips=max_pips,
                                   width=max_pips + 2,
                                   height=max_pips + 1,
                                   blanks=blanks)
                size_counts = all_size_counts[(max_pips, 3, blanks)]
                old_count = sum(size_counts.values())
                if old_count < target_count and not was_data_missing:
                    write_old_counts(all_size_counts, writer)
                    counts_file.flush()
                    was_data_missing = True
                for i in range(old_count, target_count):
                    problem = BeesProblem(init_params=init_params)
                    calculator.calculate(problem)
                    details = calculator.details.pop()
                    calculator.summaries.pop()
                    terms = re.split(r'[ +=]+', details)
                    terms.pop(0)  # 3x4
                    terms.pop(-1)  # total_moves
                    for queen, term in enumerate(terms, 3):
                        if term == 'unsolved':
                            size = -1
                        else:
                            size = int(term)
                        size_counts = all_size_counts[(max_pips, queen, blanks)]
                        size_counts[size] += 1
                        writer.writerow(dict(pips=max_pips,
                                             queen=queen,
                                             blanks=blanks,
                                             solution=size,
                                             count=1))
    if was_data_missing:
        with stats_path.open('w') as stats_file:
            writer = DictWriter(stats_file, stats_columns)
            write_old_counts(all_size_counts, writer)
        new_stats_path.unlink(missing_ok=True)


def write_old_counts(all_size_counts: dict, writer: DictWriter):
    writer.writeheader()
    for (pips, queen, blanks), size_counts in all_size_counts.items():
        for size, count in size_counts.items():
            writer.writerow(dict(pips=pips,
                                 queen=queen,
                                 blanks=blanks,
                                 solution=size,
                                 count=count))


main()
