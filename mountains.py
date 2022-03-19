import random
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

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


def main():
    args = parse_args()
    board = Board(args.columns, args.rows, args.max_pips)
    board.fill(random)
    longest_results = []
    shortest_results = []
    fitness_calculator = MountainsFitnessCalculator()
    init_params = dict(max_pips=6,
                       width=6,
                       height=6)
    for i in range(10000):
        if i % 100 == 0:
            for generation_count, start in shortest_results:
                print(f'Short {generation_count}:')
                print(start)
            for generation_count, start in longest_results:
                print(f'Long {generation_count}:')
                print(start)
        evo = MountainsEvolution(pool_size=100,
                                 fitness=fitness_calculator.calculate,
                                 individual_class=MountainsProblem,
                                 n_offsprings=30,
                                 pair_params=None,
                                 mutate_params=None,
                                 init_params=init_params,
                                 deal_num=i)

        evo.run(max_epochs=10000)
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
Short 6:
3|3 2|4 1|5

4 3 4|4 2|6
- -
3 2 5 6 3|5
    - -
0|1 0 3 4|6

1|2 2 2|5 6
    -     -
0|0 0 0|4 6

Short 6:
3|3 3 2 2|3
    - -
4|4 5 2 1 4
        - -
0|1 4|3 1 0

1|2 4|6 1|6

0|3 3|6 6 5
        - -
0|2 4|5 5 5

Short 6:
5|5 4|1 1|1

2|5 4 1|2 3
    -     -
1|6 3 2|4 3

2|2 3|6 4|5

1|3 4|6 3|5

0|3 5|6 2|6

Long 5650:
0|0 0|3 4 5
        - -
0|1 2|2 1 4

1|1 0 2|0 6
    -     -
2|6 6 1|5 6

3|5 5|5 4|3

2|3 4|6 4|2

Long 4610:
3 4|4 3|6 6
-         -
3 3|5 6 5 6
      - -
2|4 4 1 2 6
    -     -
2|2 0 0|2 2

1|3 4|1 0|3

1|2 1|1 0|0

Long 3916:
1|1 0|6 4|5

2|6 6 5 6 5
    - - - -
2|5 4 1 6 5

1|6 0|0 0|4

0|1 0 3 3|3
    - -
2|1 2 2 2|4
"""


if __name__ == '__main__':
    main()
