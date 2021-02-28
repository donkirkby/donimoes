from sys import maxsize

from networkx.algorithms.shortest_paths.weighted \
    import dijkstra_predecessor_and_distance

from domino_puzzle import BoardGraph, BadPositionError, find_boards_with_deap


class BlockingBoardGraph(BoardGraph):
    def walk(self, board, size_limit=maxsize):
        states = super().walk(board, size_limit=size_limit)
        _preds, distances = dijkstra_predecessor_and_distance(self.graph,
                                                              board.display())
        _dist, state = max((d, s) for s, d in distances.items())
        self.last = self.start
        self.start = state
        return states

    def move(self, domino, dx, dy):
        """ Move a domino and calculate the new board state.

        Afterward, put the board back in its original state.
        @return: the new board state and remaining moves
        @raise BadPositionError: if the move is illegal
        """
        remaining = 1  # ignored for this puzzle
        domino.move(dx, dy)
        try:
            board = domino.head.board
            if not board.is_connected():
                raise BadPositionError('Board is not connected.')
            if board.hasMatch():
                raise BadPositionError('Board has a match.')
            return board.display(cropped=True), remaining
        finally:
            domino.move(-dx, -dy)


def main():
    find_boards_with_deap(graph_class=BlockingBoardGraph)


if __name__ == '__main__':
    main()
