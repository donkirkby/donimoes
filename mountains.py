import random
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from itertools import count
from textwrap import dedent

from networkx import Graph, minimum_spanning_edges

from domino_puzzle import Board, Domino
from evo import Evolution, Individual


def parse_args():
    parser = ArgumentParser(
        description='Generate and solve Mountains and Valleys problems.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--max_pips',
                        type=int,
                        default=6,
                        help='Maximum pips in domino set')
    parser.add_argument('-r', '--rows',
                        type=int,
                        default=6,
                        help='Height of layout')
    parser.add_argument('-c', '--columns',
                        type=int,
                        default=6,
                        help='Width of layout')
    return parser.parse_args()


def mountain_score(board: Board):
    graph = Graph()
    for x1 in range(board.width):
        for y1 in range(board.height):
            pips1 = board[x1][y1].pips
            for dx, dy in Domino.directions[2:]:
                x2 = x1 + dx
                if x2 < 0:
                    continue
                y2 = y1 + dy
                if y2 < 0:
                    continue
                pips2 = board[x2][y2].pips
                weight = abs(pips2-pips1)
                if weight < 2:
                    weight = 0
                graph.add_edge((x1, y1), (x2, y2), weight=weight)

    score = sum(d['weight'] for u, v, d in minimum_spanning_edges(graph, keys=True))

    return score


class MountainsProblem(Individual):
    def _random_init(self, init_params):
        start = init_params.get('start')
        if start is not None:
            board = Board.create(start, max_pips=init_params['max_pips'])
            board.mutate(random)
        else:
            board = Board(**init_params)
            while True:
                if board.fill(random):
                    break

        return dict(start=board.display(),
                    max_pips=board.max_pips)

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
        return MountainsProblem(self.value)

    def mutate(self, mutate_params):
        self.value: dict
        max_pips = self.value['max_pips']
        board = Board.create(self.value['start'],
                             max_pips=max_pips)
        board.extra_dominoes.clear()
        new_board = board.mutate(random, Board)
        self.value = dict(start=new_board.display(),
                          max_pips=max_pips)


class MountainsFitnessCalculator:
    def __init__(self):
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
        """
        value = problem.value
        fitness = value.get('fitness')
        if fitness is not None:
            return fitness
        board = Board.create(value['start'])
        fitness = -mountain_score(board)
        self.summaries.append(f'{fitness}')

        value['fitness'] = fitness
        return fitness


class MountainsEvolution(Evolution):
    def __init__(self,
                 pool_size,
                 fitness,
                 individual_class,
                 n_offsprings,
                 pair_params,
                 mutate_params,
                 init_params,
                 pool_count: int = 1,
                 deal_num: int = 0):
        super().__init__(pool_size,
                         fitness,
                         individual_class,
                         n_offsprings,
                         pair_params,
                         mutate_params,
                         init_params,
                         pool_count)
        self.deal_num = deal_num

    def is_finished(self):
        top_individual = self.pool.individuals[-1]
        top_fitness = self.pool.fitness(top_individual)
        return top_fitness == 0

    def print_step_summaries(self,
                             top_individual,
                             top_fitness,
                             mid_fitness,
                             summaries):
        pass

    def print_final_summary(self, duration):
        print(f'{self.deal_num}: Ran {len(self.history)} generations '
              f'in {duration}.')


def find_gaps():
    """ See how common impossible deals are: 5938/11720000 = 0.000507. """
    args = parse_args()
    gap_count = 0
    for i in count(1):
        board = Board(args.columns, args.rows, args.max_pips)
        while True:
            if board.fill(random):
                break
        if has_gap(board):
            print(board.display())
            gap_count += 1
        if i % 10000 == 0:
            print(f'{gap_count}/{i} = {gap_count/i}')


def has_gap(board):
    required_numbers = set(range(1, 6))
    numbers = {board[x][y].pips
               for x in range(board.width)
               for y in range(board.height)}
    return numbers.intersection(required_numbers) != required_numbers


def solve_deal():
    init_params = dict(max_pips=6,
                       start=(dedent("""\
                            3|3 4 3|4 4
                                -     -
                            2|2 2 2|6 4
                            
                            1 4 4 3|6 6
                            - - -     -
                            0 0 1 4|5 4
                            
                            0|6 6 5 0|3
                                - -
                            1|6 6 0 1|3""")))
    fitness_calculator = MountainsFitnessCalculator()
    evo = MountainsEvolution(pool_size=100,
                             fitness=fitness_calculator.calculate,
                             individual_class=MountainsProblem,
                             n_offsprings=30,
                             pair_params=None,
                             mutate_params=None,
                             init_params=init_params)

    evo.run(max_epochs=10000)
    top_individual = evo.pool.individuals[-1]
    top_fitness = evo.pool.fitness(top_individual)
    print(f'{top_fitness=}')
    print(top_individual.value['start'])
    print(len(evo.history))


def main():
    args = parse_args()
    longest_results = []
    shortest_results = []
    gap_count = 0
    fitness_calculator = MountainsFitnessCalculator()
    for i in count(1):
        if i % 100 == 0:
            print(f'Gap odds are {gap_count}/{i} = {gap_count/i}.')
            for generation_count, start in shortest_results:
                print(f'Short {generation_count}:')
                print(start)
            for generation_count, start in longest_results:
                print(f'Long {generation_count}:')
                print(start)
        board = Board(args.columns, args.rows, args.max_pips)
        while True:
            if board.fill(random):
                break
        if has_gap(board):
            gap_count += 1
            print(f'{i}: Gap found.')
            continue
        init_params = dict(max_pips=args.max_pips, start=board.display())
        evo = MountainsEvolution(pool_size=100,
                                 fitness=fitness_calculator.calculate,
                                 individual_class=MountainsProblem,
                                 n_offsprings=30,
                                 pair_params=None,
                                 mutate_params=None,
                                 init_params=init_params,
                                 deal_num=i)

        evo.run(max_epochs=40000)
        top_individual = evo.pool.individuals[-1]
        top_fitness = evo.pool.fitness(top_individual)
        if top_fitness != 0:
            print(f'{top_fitness=}')
            print(top_individual.value['start'])
            break
        result = (len(evo.history), top_individual.value['start'])
        longest_results.append(result)
        longest_results.sort(reverse=True)
        if len(longest_results) > 3:
            longest_results.pop()
        shortest_results.append(result)
        shortest_results.sort()
        if len(shortest_results) > 3:
            shortest_results.pop()
        should_print = False
        if result in shortest_results:
            should_print = True
            print('New short:')
        if result in longest_results:
            should_print = True
            print('New long:')
        if should_print:
            print(top_individual.value['start'])


"""
Gap odds are 0/3300 = 0.0.
Short 11:
4|5 5 5|6 6
    -     -
3|6 5 1|6 6

3|3 3 2|6 6
    -     -
4|0 2 4|4 4

0|1 2 3 2|2
    - -
0|2 1 0 0|0

Short 14:
4 5|6 5|5 6
-         -
1 1|0 4|2 2

1|1 1|5 2|2

1|2 0|5 6|3

0|2 2|5 5|4

3|3 4|4 6|4

Short 17:
6|6 5 4|3 4
    -     -
6|1 0 0|2 4

5|5 4 1|3 3
    -     -
5|6 5 0|1 3

5 4 5 1|1 3
- - -     -
3 2 2 1|2 2

Long 29291:
3|5 4 5|4 4
    -     -
3 4 0 6|1 2
- -
2 4 0|0 0|2

1|5 6 6 0|3
    - -
0|5 3 4 3|4

0|6 6|6 5|5

Long 25772:
0 2|2 6 6 5
-     - - -
0 1|6 6 0 1

0|5 6 6 0|2
    - -
0|4 3 4 3|2

0|3 6 5|2 2
    -     -
0|1 2 3|3 4

Long 21384:
2 3 3|3 4|6
- -
2 1 2 3|4 6
    -     -
1|6 6 2|4 6

0|6 5|5 4 5
        - -
0|5 3 4 0 1
    - -
0|3 2 1 0|2

3342: Ran 40000 generations in 0:32:42.851259.
top_fitness=-2
0|2 6|6 5|6

0|3 4|5 0|6

2 2|4 4 1|6
-     -
2 2|5 3 2|6

3|6 5 4 1|2
    - -
4|6 0 0 0|0

3069: Ran 40000 generations in 0:31:27.698066.
top_fitness=-2
4 3|6 0|4 4
-         -
1 2|6 1|3 2

0|3 4 2 0|2
    - -
0|0 3 2 1|1

0|5 4|6 1|6

0|6 6|6 5|6

"""


if __name__ == '__main__':
    main()
