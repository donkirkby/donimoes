from collections import defaultdict
from random import Random
from sys import maxsize
from datetime import datetime

from networkx.algorithms.shortest_paths.weighted \
    import dijkstra_predecessor_and_distance

from domino_puzzle import BoardGraph, BadPositionError, createRandomBoard, \
    Board

WIDTH = 4
HEIGHT = 4

"""
139 283431
x x x x x x x x 0 x x x
                -
4|4 x x x x 0|2 5 x x x

x 6|1 x x x x 3 4|0 6 x
              -     -
x x 4|3 2|5 x 2 x x 6 x

x x x x x 3 0|0 x x 0|1
          -
x x x x x 5 x x x x x x

--- 2017-01-27 00:03:27.019913 ---
"""


class BlockingBoardGraph(BoardGraph):
    def walk(self, board, size_limit=maxsize):
        states = BoardGraph.walk(self, board, size_limit=size_limit)
        _preds, distances = dijkstra_predecessor_and_distance(self.graph,
                                                              board.display())
        _dist, state = max((d, s) for s, d in distances.items())
        self.last = self.start
        self.start = state
        return states

    def move(self, domino, dx, dy):
        """ Move a domino and calculate the new board state.

        Afterward, put the board back in its original state.
        @return: the new board state
        @raise BadPositionError: if the move is illegal
        """
        domino.move(dx, dy)
        try:
            board = domino.head.board
            if not board.isConnected():
                raise BadPositionError('Board is not connected.')
            if board.hasMatch():
                raise BadPositionError('Board has a match.')
            return board.display(cropped=True)
        finally:
            domino.move(-dx, -dy)


def main():
    random = Random()
    graph = BlockingBoardGraph()
    maxes = defaultdict(lambda: 0)  # {max_choices: soln_len}
    for _ in range(1000):
        board = createRandomBoard(Board, random, WIDTH, HEIGHT)
        graph.walk(board)
        choice_counts = graph.get_choice_counts()
        max_choice_count = choice_counts and max(choice_counts) or 0
        soln_len = len(choice_counts)
        best_max = maxes[max_choice_count]
        if soln_len > best_max:
            maxes[max_choice_count] = soln_len
            print([soln_len, max_choice_count])
            print(graph.start.replace('x', ' '))
            print('--- {} ---'.format(datetime.now()) +
                  ' ' * 100 + ', '.join(graph.get_solution()))

if __name__ == '__main__':
    main()
