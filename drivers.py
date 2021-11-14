import operator
import random
import sys
import typing
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime
from functools import reduce
from sys import maxsize

from bees import count_gaps
from domino_puzzle import (Board, BoardGraph, GraphLimitExceeded, DiceSet,
                           ArrowSet, MoveDescription, Domino, BoardError)
from evo import Individual, Evolution


class DriversProblem(Individual):
    def __repr__(self):
        return f'DriversProblem({self.value!r}'

    def pair(self, other, pair_params):
        return DriversProblem(self.value)

    def mutate(self, mutate_params):
        self.value: dict
        max_pips = self.value['max_pips']
        board = DriversBoard.create(self.value['start'],
                                    max_pips=max_pips)
        while True:
            new_board = board.mutate(random, DriversBoard)
            if self.is_valid(new_board):
                break
        self.value = dict(start=new_board.display(),
                          max_pips=max_pips)

    def _random_init(self, init_params: dict):
        while True:
            board = DriversBoard(**init_params)
            while True:
                if board.fill(random):
                    break
            if self.is_valid(board):
                break

        return dict(start=board.display(),
                    max_pips=board.max_pips)

    @staticmethod
    def is_valid(board):
        board.place_dice()
        return len(board.dice_set.items()) == 4


class DriversFitnessCalculator:
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
        -100,000 when the graph had more than 10,000 nodes and stopped exploring
        -1,000,000 when the problem was unsolved.
        10,000 * variey of move types
        -1,000 * difference from target length
        10* max choices at any step
        average choices at any step
        """
        value = problem.value
        fitness = value.get('fitness')
        if fitness is not None:
            return fitness
        board = DriversBoard.create(value['start'])
        fitness = 0
        graph = DriversGraph(process_count=2)
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
            fitness -= 1_000_000
            fitness -= min_remaining
            self.summaries.append('unsolved')
        else:
            solution_nodes = graph.get_solution_nodes()
            solution_moves = graph.get_solution(solution_nodes=solution_nodes)
            move_types = {str(pips): 0.1 for pos, pips in board.dice_set.items()}
            move_types['domino'] = 0.1
            for move in solution_moves:
                if len(move) == 3:
                    move_types['domino'] += 1
                move_type = move[0]
                move_types[move_type] += 1
            variety_score = reduce(operator.mul, move_types.values(), 1)
            fitness += variety_score * 10000

            if self.target_length is None:
                fitness += len(solution_nodes)*1000
            else:
                fitness -= 1000*abs(len(solution_nodes) - self.target_length)

            max_choices = graph.get_max_choices(solution_nodes)
            average_choices = graph.get_average_choices(solution_nodes)
            fitness -= max_choices*10
            fitness -= average_choices
            self.summaries.append(', '.join(solution_moves))
            self.details.append(
                f'{board.width}x{board.height}: {len(solution_moves)} moves, '
                f'max {max_choices}, avg {average_choices}, '
                f'variety {variety_score}, '
                f'{len(graph.graph)} states')

        value['fitness'] = fitness
        return fitness


class DriversBoard(Board):
    @classmethod
    def create(cls, state, border=0, max_pips=None) -> 'DriversBoard':
        board = super().create(state, border, max_pips)
        if board.max_pips is None:
            board.max_pips = max(board[x][y].pips
                                 for x in range(board.width)
                                 for y in range(board.height))
        if board.dice_set is None:
            board.place_dice()

        return board

    def __init__(self,
                 width: int,
                 height: int,
                 max_pips: int = None,
                 dice_set: DiceSet = None,
                 arrows: ArrowSet = None):
        super().__init__(width, height, max_pips, dice_set, arrows)

    def place_dice(self):
        self.dice_set = DiceSet()
        placed_pips = set()
        for x, y in ((0, self.height-1),
                     (self.width-1, self.height-1),
                     (0, 0),
                     (self.width-1, 0),):
            pips = self[x][y].pips
            if pips != 0 and pips not in placed_pips:
                self.dice_set.dice[x, y] = pips
                placed_pips.add(pips)


class DriversGraph(BoardGraph):
    def __init__(self,
                 board_class=DriversBoard,
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

    def generate_moves(self, board: DriversBoard) -> typing.Iterator[
            MoveDescription]:
        """ Generate all moves from the board's current state.

        :param Board board: the current state
        """
        generated_moves = set()
        dice_set = board.dice_set
        forced_pips = None
        for (x, y), pips in dice_set.items():
            cell = board[x][y]
            if cell.pips != pips:
                forced_pips = pips
                break

        for (x, y), pips in list(dice_set.items()):
            if forced_pips is not None and pips != forced_pips:
                # Another die must walk.
                continue
            # Try to walk die.
            for dx, dy in Domino.directions:
                x2 = x+dx
                y2 = y+dy
                if (x2, y2) in dice_set:
                    continue
                cell = board[x2][y2]
                if cell is None:
                    continue
                if pips < cell.pips:
                    continue
                positions = [(x, y), (x2, y2)]
                move = dice_set.move(*positions, show_length=False)
                combined_display = board.display(cropped=True)
                total_gaps = self.check_progress(board)
                yield MoveDescription(move,
                                      combined_display,
                                      remaining=total_gaps)
                positions.reverse()
                dice_set.move(*positions)
            # Try to drive domino
            cell = board[x][y]
            if cell.pips != pips:
                # Must walk, not drive.
                continue
            domino = cell.domino
            partner_cell = cell.partner
            dx = cell.x - partner_cell.x
            dy = cell.y - partner_cell.y
            partner_position = (partner_cell.x, partner_cell.y)
            dice_start_positions = [(x, y)]
            if partner_position in dice_set:
                dice_start_positions.append(partner_position)
            move_sets = (((dx, dy), dice_start_positions),
                         ((-dx, -dy), list(reversed(dice_start_positions))))
            for (dx, dy), dice_start_positions in move_sets:
                try:
                    domino.move(dx, dy)
                except BoardError:
                    continue
                if board.is_connected():
                    x, y = dice_start_positions[0]
                    positions = [(x, y), (x+dx, y+dy)]
                    move = dice_set.move(*positions, show_length=False)
                    move = move[0] + 'd' + move[1:]
                    if len(dice_start_positions) == 2:
                        x2, y2 = dice_start_positions[1]
                        positions2 = [(x2, y2), (x2+dx, y2+dy)]
                        dice_set.move(*positions2)
                    else:
                        positions2 = None
                    combined_display = board.display(cropped=True)
                    total_gaps = self.check_progress(board)
                    if move not in generated_moves:
                        generated_moves.add(move)
                        yield MoveDescription(move,
                                              combined_display,
                                              remaining=total_gaps,
                                              heuristic=total_gaps)
                    if len(dice_start_positions) == 2:
                        positions2.reverse()
                        dice_set.move(*positions2)
                    positions.reverse()
                    dice_set.move(*positions)
                domino.move(-dx, -dy)

    def check_progress(self, board: DriversBoard) -> int:
        """ See how close a board is to a solution. """
        positions = {(x, y)
                     for x in range(board.width)
                     for y in range(board.height)
                     if (cell := board[x][y]) is not None and cell.pips == 0}
        return count_gaps(positions, board.width, board.height)


def parse_args():
    parser = ArgumentParser(description='Search for Donimo Drivers problems.',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--max_pips',
                        '-p',
                        type=int,
                        default=4,
                        help='Maximum number of pips to include on dominoes.')
    parser.add_argument('--target_length',
                        '-l',
                        type=int,
                        default=25,
                        help='Highest scoring solution length.')
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
    start_time = datetime.now()
    args = parse_args()
    max_pips = args.max_pips
    print(f'Searching for solutions of length {args.target_length} '
          f'with up to {max_pips} pips.')
    target_total = args.target_length
    fitness_calculator = DriversFitnessCalculator(target_length=args.target_length)
    init_params = dict(max_pips=max_pips,
                       width=max_pips+2,
                       height=max_pips+1)
    evo = Evolution(
        pool_size=args.pool_size,
        fitness=fitness_calculator.calculate,
        individual_class=DriversProblem,
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
