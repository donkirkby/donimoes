import random
import sys
import typing
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime
from sys import maxsize

from domino_puzzle import (Board, BoardGraph, GraphLimitExceeded, DiceSet,
                           ArrowSet, MoveDescription)
from evo import Individual, Evolution

DEFAULT_BLANKS = 'touching'


class BeesProblem(Individual):
    def __repr__(self):
        return f'BeesProblem({self.value!r})'

    def pair(self, other, pair_params):
        # self_head = self.value[:int(len(self.value) * pair_params['alpha'])].copy()
        # self_tail = self.value[int(len(self.value) * pair_params['alpha']):].copy()
        # other_tail = other.value[int(len(other.value) * pair_params['alpha']):].copy()
        #
        # mapping = {other_tail[i]: self_tail[i] for i in range(len(self_tail))}
        #
        # for i in range(len(self_head)):
        #     while self_head[i] in other_tail:
        #         self_head[i] = mapping[self_head[i]]

        # return DominosaProblem(np.hstack([self_head, other_tail]))
        return BeesProblem(self.value)

    def mutate(self, mutate_params):
        self.value: dict
        max_pips = self.value['max_pips']
        board = BeesBoard.create(self.value['start'],
                                 max_pips=max_pips)
        new_board = board.mutate(random, BeesBoard)
        self.value = dict(start=new_board.display(),
                          max_pips=max_pips,
                          blanks=self.value.get('blanks', DEFAULT_BLANKS))

    def _random_init(self, init_params: dict):
        final_params = dict(init_params)
        blanks = final_params.pop('blanks', DEFAULT_BLANKS)
        board = BeesBoard(**final_params)
        while True:
            if not board.fill(random):
                pass
            elif not board.has_touching_blanks:
                break
            elif blanks == 'redeal':
                board = BeesBoard(**final_params)
            else:
                break

        return dict(start=board.display(),
                    max_pips=board.max_pips,
                    blanks=blanks)


class BeesFitnessCalculator:
    def __init__(self, target_length=100, size_limit=11_200):
        self.target_length = target_length
        self.size_limit = size_limit
        self.details = []
        self.summaries = []

    def format_summaries(self):
        display = '\n'.join(self.summaries)
        self.summaries.clear()
        return display

    def format_details(self):
        display = '\n\n'.join(self.details)
        self.details.clear()
        return display

    def calculate(self, problem):
        """ Calculate fitness score based on the solution.

        Categories (most valuable to least:
        -1,000,000 * unsolved dominoes when no unique solution found
        -100,000 when the graph had more than 10,000 nodes and stopped exploring
        """
        value = problem.value
        fitness = value.get('fitness')
        if fitness is not None:
            return fitness
        board = BeesBoard.create(value['start'])
        max_pips = board.queen_pips
        round_summaries = []
        solution_lengths = []
        fitness = 0
        blanks = value.get('blanks')
        are_all_blanks_wild = blanks == 'wild'
        for queen_pips in range(3, max_pips+1):
            graph = BeesGraph(process_count=3,
                              are_all_blanks_wild=are_all_blanks_wild)
            board.place_dice(queen_pips)
            try:
                graph.walk(board, size_limit=self.size_limit)
            except GraphLimitExceeded:
                fitness -= 100_000
            except BaseException:
                print('Failed to solve:', file=sys.stderr)
                print(board.display(), file=sys.stderr)
                raise
            min_remaining = graph.min_remaining
            if min_remaining is None:
                min_remaining = board.width + board.height
            if graph.last is None:
                fitness -= 1_000_000 * min_remaining
                moves = ['unsolved']
                solution_lengths.append('unsolved')
            else:
                moves = graph.get_solution()
                solution_lengths.append(len(moves))

            move_display = ', '.join(moves)
            round_summaries.append(f'Moves for {queen_pips}: {move_display}.')
        if 'unsolved' in solution_lengths:
            total_moves = 'unsolved'
        else:
            move_product = 1000
            for solution_length in solution_lengths:
                move_product *= abs(solution_length - self.target_length + 0.1)
            move_product = round(move_product)
            total_moves = sum(solution_lengths)  # < 100?
            fitness = (100_000_000_000 +
                       -1_000 * move_product +
                       total_moves)
            round_summaries.insert(0, f'Total moves: {total_moves}.')

        lengths_display = ' + '.join(str(length)
                                     for length in solution_lengths)
        lengths_display += f' = {total_moves}'
        self.summaries.append('\n    '.join(round_summaries))
        self.details.append(f'{board.width}x{board.height} {lengths_display}')

        value['fitness'] = fitness
        return fitness


class BeesBoard(Board):
    @classmethod
    def create(cls, state, border=0, max_pips=None) -> 'BeesBoard':
        # We never want borders for Bees boards, because dominoes don't move.
        board = super().create(state, border=0, max_pips=max_pips)
        if board.max_pips is None:
            board.max_pips = max(board[x][y].pips
                                 for x in range(board.width)
                                 for y in range(board.height))
        if board.dice_set is None:
            board.place_dice()
        if board.dice_set.dice:
            board.queen_pips = max(board.dice_set.dice.values())

        return board

    def __init__(self,
                 width: int,
                 height: int,
                 max_pips: int = None,
                 dice_set: DiceSet = None,
                 arrows: ArrowSet = None):
        super().__init__(width, height, max_pips, dice_set, arrows)
        self.queen_pips = 0

    def place_dice(self, max_pips: int = None):
        if max_pips is None:
            max_pips = self.max_pips
        self.dice_set = DiceSet()
        for x in range(self.width):
            for y in range(self.height):
                cell = self[x][y]
                partner_cell = cell.partner
                if (partner_cell.pips == 0 and
                        cell.pips != 0 and
                        cell.pips <= max_pips):
                    self.dice_set.dice[x, y] = cell.pips
        self.queen_pips = max(self.dice_set.dice.values())

    @property
    def has_touching_blanks(self):
        for domino1 in self.dominoes:
            if domino1.head.pips != 0 and domino1.tail.pips != 0:
                continue
            for domino2 in domino1.find_neighbours():
                if domino2.head.pips == 0 or domino2.tail.pips == 0:
                    return True
        return False


def count_gaps(positions: typing.Set[typing.Tuple[int, int]],
               width: int,
               height: int):
    if not positions:
        return 0
    unvisited = set(positions)
    max_gap = width + height
    old_total = max_gap * len(unvisited)
    grouped = set()
    grouped.add(unvisited.pop())
    while True:
        total_gaps = 0
        while unvisited:
            x1, y1 = unvisited.pop()
            min_gap = width + height
            for x2, y2 in grouped:
                gap = abs(x1 - x2) + abs(y1 - y2) - 1
                if gap == 0:
                    break
                elif gap < min_gap:
                    min_gap = gap
            else:
                total_gaps += min_gap
                continue
            grouped.add((x1, y1))
        if total_gaps == 0 or total_gaps == old_total:
            break
        old_total = total_gaps
        unvisited = positions - grouped
    return total_gaps


class BeesGraph(BoardGraph):
    def __init__(self,
                 board_class=BeesBoard,
                 process_count: int = 0,
                 debug=False,
                 are_all_blanks_wild=False):
        super().__init__(board_class, process_count)
        self.debug = debug
        self.are_all_blanks_wild = are_all_blanks_wild
        self.solution_states = set()
        self.last = None
        self.min_gaps: typing.Optional[int] = None

    def clone(self) -> 'BoardGraph':
        clone = super().clone()
        clone.are_all_blanks_wild = self.are_all_blanks_wild
        return clone

    def walk(self, board, size_limit=maxsize):
        self.min_gaps = None
        self.check_remaining(self.check_progress(board), board.display())
        self.solution_states.clear()
        states = super().walk(board, size_limit)
        return states

    def generate_moves(self, board: BeesBoard) -> typing.Iterator[
            MoveDescription]:
        """ Generate all moves from the board's current state.

        :param Board board: the current state
        """
        dice_set = board.dice_set
        board.dice_set = None
        board_display = board.display()
        board.dice_set = dice_set
        for (x, y), pips in list(dice_set.items()):
            if pips == board.queen_pips:
                continue
            positions = [(x, y)]
            for extended_positions in self.extend_positions(positions, board):
                move = dice_set.move(*extended_positions)
                dice_display = dice_set.text
                combined_display = f'{board_display}---\ndice:{dice_display}\n'
                total_gaps = self.check_progress(board)
                yield MoveDescription(move,
                                      combined_display,
                                      remaining=total_gaps)
                dice_set.move(extended_positions[-1], (x, y))

    def extend_positions(self, positions: typing.List[typing.Tuple[int, int]], board: BeesBoard):
        pips = board.dice_set.dice[positions[0]]
        x, y = positions[-1]

        if len(positions) <= 1:
            dx = dy = 0
        else:
            # Force moves over a die to turn a corner.
            x2, y2 = positions[-2]
            dx = x - x2
            dy = y - y2
        targets = []
        if dx == 0:
            targets.extend((x2, y) for x2 in range(board.width))
        if dy == 0:
            targets.extend((x, y2) for y2 in range(board.height))

        wild_positions = set()
        if self.are_all_blanks_wild:
            for x in range(board.width):
                for y in range(board.height):
                    if board[x][y].pips == 0:
                        wild_positions.add((x, y))
            wild_positions.difference_update(board.dice_set.dice)
        else:
            for position, pips2 in board.dice_set.dice.items():
                if pips2 == board.queen_pips:
                    queen_x, queen_y = position
                    wild_cell = board[queen_x][queen_y].partner
                    wild_position = wild_cell.x, wild_cell.y
                    if wild_position not in board.dice_set.dice:
                        # Wild position is not occupied, can use it.
                        wild_positions.add(wild_position)

        direct_positions = []
        for position2 in targets:
            if position2 in positions:
                continue
            x2, y2 = position2
            pips2 = board[x2][y2].pips
            if pips2 == pips or position2 in wild_positions:
                direct_positions.append(position2)
            elif position2 in board.dice_set.dice:
                yield from self.extend_positions(positions + [position2], board)
        for position2 in direct_positions:
            yield positions + [position2]

    def check_progress(self, board: BeesBoard) -> int:
        """ See how close a board is to a solution. """
        return count_gaps(set(board.dice_set.dice), board.width, board.height)


def parse_args():
    parser = ArgumentParser(description='Search for Bee Donimoes problems.',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--max_pips',
                        '-p',
                        type=int,
                        default=3,
                        help='Maximum number of pips to include on dominoes.')
    parser.add_argument('--target_length',
                        '-l',
                        type=int,
                        default=25,
                        help='Highest scoring solution length for each queen.')
    parser.add_argument('--pool_size',
                        '-s',
                        type=int,
                        default=100,
                        help='Number of items in each evolutionary pool.')
    parser.add_argument('--offspring',
                        '-o',
                        type=int,
                        default=30,
                        help='Number of offspring to generate in each pool per epoch.')
    parser.add_argument('--num_pools',
                        '-n',
                        type=int,
                        default=2,
                        help='Number of evolutionary pools.')
    parser.add_argument('--epochs',
                        '-e',
                        type=int,
                        default=1000,
                        help='Number of evolutionary epochs.')
    return parser.parse_args()


def main():
    # Suggested sizes:
    # easy (1-3) 3 targets 4-8
    # medium (4-7) 4 targets 5-11
    # hard (8-13) 5 targets 6-16
    # tricky (14-20) 6 targets 7-19

    start_time = datetime.now()
    args = parse_args()
    max_pips = args.max_pips
    print(f'Searching for solutions of length {args.target_length} '
          f'with up to {max_pips} pips.')
    target_total = args.target_length * (max_pips - 2)
    fitness_calculator = BeesFitnessCalculator(target_length=args.target_length)
    init_params = dict(max_pips=max_pips,
                       width=max_pips+2,
                       height=max_pips+1)
    evo = Evolution(
        pool_size=args.pool_size,
        fitness=fitness_calculator.calculate,
        individual_class=BeesProblem,
        n_offsprings=args.offspring,
        pair_params=None,
        mutate_params=None,
        init_params=init_params,
        pool_count=args.num_pools)
    n_epochs = args.epochs

    hist = []
    for i in range(n_epochs):
        top_individual = evo.pool.individuals[-1]
        top_fitness = evo.pool.fitness(top_individual)
        mid_fitness = evo.pool.fitness(evo.pool.individuals[-len(evo.pool.individuals)//5])
        summaries = []
        for pool in evo.pools:
            pool_fitness = pool.fitness(pool.individuals[-1])
            total = pool_fitness % 1000
            summaries.append(f'{total}/{target_total}')
        print(i,
              top_fitness,
              mid_fitness,
              repr(top_individual.value['start']),
              ', '.join(summaries))
        hist.append(top_fitness)
        evo.step()

    best = evo.pool.individuals[-1]
    for problem in evo.pool.individuals:
        print(evo.pool.fitness(problem))
    # plt.plot(hist)
    # plt.show()
    solution = best.value['start']
    print(solution)
    duration = datetime.now() - start_time
    print(f'Finished {n_epochs} epochs in {duration}.')


if __name__ == '__main__':
    main()
