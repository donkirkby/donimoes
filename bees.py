import random
import sys
import typing
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from sys import maxsize

from networkx import Graph, is_connected

from domino_puzzle import Board, BoardGraph, GraphLimitExceeded, DiceSet, ArrowSet
from evo import Individual, Evolution


class BeesProblem(Individual):
    def __repr__(self):
        return f'BeesProblem({self.value!r}'

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
        max_pips = self.value['max_pips']
        board = BeesBoard.create(self.value['start'],
                                 max_pips=max_pips)
        new_board = board.mutate(random, BeesBoard)
        self.value = dict(start=new_board.display(),
                          max_pips=max_pips)

    def _random_init(self, init_params):
        board = BeesBoard(**init_params)
        while True:
            if board.fill(random):
                break
        board.place_dice()

        return dict(start=board.display(),
                    max_pips=board.queen_pips)


class BeesFitnessCalculator:
    def __init__(self, target_length=100, size_limit=10_000):
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
        for queen_pips in range(3, max_pips+1):
            graph = BeesGraph()
            board.place_dice(queen_pips)
            try:
                graph.walk(board, size_limit=self.size_limit)
            except GraphLimitExceeded:
                fitness -= 100_000
            except BaseException:
                print('Failed to solve:', file=sys.stderr)
                print(board.display(), file=sys.stderr)
                raise
            min_heuristic = graph.min_gaps
            if graph.last is None:
                fitness -= 1_000_000 * min_heuristic
                moves = ['unsolved']
            else:
                moves = graph.get_solution()
                solution_lengths.append(len(moves))

            move_display = ', '.join(moves)
            round_summaries.append(f'Moves for {queen_pips}: {move_display}.')
        if len(solution_lengths) == max_pips - 2:
            move_product = 1000
            for solution_length in solution_lengths:
                move_product *= abs(solution_length - self.target_length + 0.1)
            move_product = round(move_product)
            total_moves = sum(solution_lengths)  # < 100?
            fitness = (100_000_000_000 +
                       -1_000 * move_product +
                       total_moves)
            round_summaries.insert(0, f'Total moves: {total_moves}.')
        self.summaries.append('\n    '.join(round_summaries))
        self.details.append(f'{board.width}x{board.height} {fitness} ')

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


class BeesGraph(BoardGraph):
    def __init__(self,
                 board_class=BeesBoard,
                 debug=False):
        super().__init__(board_class)
        self.debug = debug
        self.solution_states = set()
        self.last = None
        self.min_gaps: typing.Optional[int] = None

    def walk(self, board, size_limit=maxsize):
        self.min_gaps = None
        self.check_progress(board)
        self.solution_states.clear()
        self.last = None
        states = super().walk(board, size_limit)
        return states

    def generate_moves(self, board: BeesBoard) -> typing.Iterator[
            typing.Tuple[str, str]]:
        """ Generate all moves from the board's current state.

        :param Board board: the current state
        :return: a generator of (move_description, state, edge_attrs, heuristic)
            tuples, where the last two are optional
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
                self.check_progress(board)
                yield move, combined_display
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

        wild_position = None
        for position, pips2 in board.dice_set.dice.items():
            if pips2 == board.queen_pips:
                queen_x, queen_y = position
                wild_cell = board[queen_x][queen_y].partner
                wild_position = wild_cell.x, wild_cell.y
                if wild_position in board.dice_set.dice:
                    # Wild position is already occupied, can't use it.
                    wild_position = None
        direct_positions = []
        for position2 in targets:
            if position2 in positions:
                continue
            x2, y2 = position2
            pips2 = board[x2][y2].pips
            if pips2 == pips or position2 == wild_position:
                direct_positions.append(position2)
            elif position2 in board.dice_set.dice:
                yield from self.extend_positions(positions + [position2], board)
        for position2 in direct_positions:
            yield positions + [position2]

    def check_progress(self, board):
        """ Keep track of which board state was the closest to a solution. """
        neighbour_graph = Graph()
        total_gaps = 0
        queen_pips = board.queen_pips
        for (x1, y1), pips1 in board.dice_set.dice.items():
            neighbour_graph.add_edge(pips1, pips1)
            for (x2, y2), pips2 in board.dice_set.dice.items():
                gap = abs(x1-x2) + abs(y1-y2) - 1
                if gap >= 0 and pips1 == queen_pips:
                    total_gaps += gap
                if gap == 0:
                    neighbour_graph.add_edge(pips1, pips2)
        if self.min_gaps is None or total_gaps < self.min_gaps:
            self.min_gaps = total_gaps
        if self.last is None and is_connected(neighbour_graph):
            self.last = board.display()


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
    return parser.parse_args()


def main():
    # Suggested sizes:
    # easy (1-3) 3 targets 4-8
    # medium (4-7) 4 targets 5-11
    # hard (8-13) 5 targets 6-16
    # tricky (14-20) 6 targets 7-19

    args = parse_args()
    max_pips = args.max_pips
    print(f'Searching for solutions of length {args.target_length} '
          f'with up to {max_pips} pips.')
    fitness_calculator = BeesFitnessCalculator(target_length=args.target_length)
    init_params = dict(max_pips=max_pips, width=max_pips+2, height=max_pips+1)
    evo = Evolution(
        pool_size=100,
        fitness=fitness_calculator.calculate,
        individual_class=BeesProblem,
        n_offsprings=30,
        pair_params=None,
        mutate_params=None,
        init_params=init_params)
    n_epochs = 1000

    hist = []
    for i in range(n_epochs):
        top_individual = evo.pool.individuals[-1]
        top_fitness = evo.pool.fitness(top_individual)
        mid_fitness = evo.pool.fitness(evo.pool.individuals[-len(evo.pool.individuals)//5])
        print(i,
              top_fitness,
              mid_fitness,
              repr(top_individual.value['start']),
              top_fitness % 1000)
        hist.append(top_fitness)
        evo.step()

    best = evo.pool.individuals[-1]
    for problem in evo.pool.individuals:
        print(evo.pool.fitness(problem))
    # plt.plot(hist)
    # plt.show()
    solution = best.value['start']
    print(solution)


if __name__ == '__main__':
    main()
