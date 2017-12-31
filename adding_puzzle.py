from blocking_puzzle import BlockingBoardGraph
from domino_puzzle import BadPositionError
from queued_board import QueuedBoard


class AddingBoardGraph(BlockingBoardGraph):
    def __init__(self, board_class=QueuedBoard):
        super().__init__(board_class)

    def generate_moves(self, board):
        yield from super().generate_moves(board)
        for domino in board.dominoes[:]:
            yield from self.try_remove(domino)

    def move(self, domino, dx, dy):
        """ Move a domino and calculate the new board state.

        Afterward, put the board back in its original state.
        @return: the new board state
        @raise BadPositionError: if the move is illegal
        """
        if not domino.dominates_neighbours():
            raise BadPositionError("Domino doesn't dominate before move.")
        domino.move(dx, dy)
        try:
            if not domino.dominates_neighbours():
                raise BadPositionError("Domino doesn't dominate after move.")
            board = domino.head.board
            if not board.isConnected():
                raise BadPositionError('Board is not connected.')
            return board.display(cropped=True)
        finally:
            domino.move(-dx, -dy)

    def try_remove(self, domino):
        try:
            new_state = self.remove(domino)
            move = domino.describe_remove()
            yield move, new_state
        except BadPositionError:
            pass

    @staticmethod
    def remove(domino):
        """ Remove a domino and calculate the new board state.

        Afterward, put the board back in its original state.
        @return: the new board state
        @raise BadPositionError: if the move is illegal
        """
        if not (domino.head.pips or domino.tail.pips):
            raise BadPositionError("Cannot remove 0|0.")
        if sum(1 for _ in domino.find_neighbour_cells()) < 2:
            raise BadPositionError("Domino doesn't have two neighbours.")
        if not domino.dominates_neighbours():
            raise BadPositionError("Domino doesn't dominate before removing.")
        x = domino.head.x
        y = domino.head.y
        board = domino.head.board
        try:
            board.remove(domino)
            board.add_to_queue(domino)
            if not board.isConnected():
                raise BadPositionError('Board is not connected.')
            return board.display(cropped=True)
        finally:
            board.get_from_queue()
            board.add(domino, x, y)
