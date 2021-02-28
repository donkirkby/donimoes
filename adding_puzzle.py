import typing
from sys import maxsize

from domino_puzzle import (BadPositionError, find_boards_with_deap, Domino,
                           BoardGraph, MoveDescription)
from queued_board import QueuedBoard


class AddingBoardGraph(BoardGraph):
    def __init__(self, board_class=QueuedBoard):
        super().__init__(board_class)

    def generate_moves(self, board: QueuedBoard):
        start_display = board.display(cropped=bool(board.dominoes))
        start_board = QueuedBoard.create(start_display, border=1)
        if not start_board.dominoes:
            start_board.add(start_board.get_from_queue(), 1, 2)
            start_board.add(start_board.get_from_queue(), 2, 2)
        yield from super().generate_moves(start_board)
        yield from self.try_add(start_board)

    def move(self, domino, dx, dy) -> typing.Tuple[str, int]:
        """ Move a domino and calculate the new board state.

        Afterward, put the board back in its original state.
        @return: the new board state and the number of dominoes left unadded
        @raise BadPositionError: if the move is illegal
        """
        domino.move(dx, dy)
        try:
            self.check_matches(domino, is_complement_allowed=True)
            board = domino.head.board
            if not board.is_connected():
                raise BadPositionError('Board is not connected.')
            remaining = self.check_progress(board)
            return board.display(cropped=True), remaining
        finally:
            domino.move(-dx, -dy)

    def try_add(self, board: QueuedBoard):
        if not board.queue:
            return
        added_domino: Domino = board.get_from_queue()
        for x in range(board.width):
            for y in range(board.height):
                for angle_index in range(4):
                    try:
                        added_domino.rotate_to(angle_index * 90)
                        new_display, remaining = self.add(added_domino,
                                                          board,
                                                          x,
                                                          y)
                        move = added_domino.describe_add(x, board.height-y-1)
                        yield MoveDescription(move,
                                              new_display,
                                              remaining=remaining)
                    except BadPositionError:
                        pass

    def add(self,
            domino: Domino,
            board: QueuedBoard,
            x: int,
            y: int) -> typing.Tuple[str, float]:
        """ Add a domino and calculate the new board state.

        Afterward, put the board back in its original state.
        @return: the new board state and remaining progress to reach goal
        @raise BadPositionError: if the move is illegal
        """
        board.add(domino, x, y)
        try:
            self.check_matches(domino)

            new_display = board.display(cropped=True)
            remaining = self.check_progress(board)
            return new_display, remaining
        finally:
            board.remove(domino)

    @staticmethod
    def check_matches(domino: Domino, is_complement_allowed=False):
        match_count = 0
        complement_count = 0
        for cell in (domino.head, domino.tail):
            for neighbour in cell.find_neighbours():
                if neighbour.pips == cell.pips:
                    match_count += 1
                if neighbour.pips + cell.pips == 6:
                    complement_count += 1
        if is_complement_allowed:
            if match_count < 2 and complement_count < 1:
                raise BadPositionError(
                    "Domino doesn't have two matching neighbours or one "
                    "neighbour that adds up to six.")
        else:
            if match_count < 2:
                raise BadPositionError(
                    "Domino doesn't have two matching neighbours.")

    def walk(self, board: QueuedBoard, size_limit=maxsize) -> typing.Set[str]:
        start = board.display(cropped=True)
        states = super().walk(board, size_limit)
        self.start = start
        return states

    def check_progress(self, board: QueuedBoard):
        """ Keep track of which board state was the closest to a solution. """
        if len(board.dominoes) <= 2:
            # Only added the first two dominoes. No real progress
            domino_count = len(board.dominoes) + len(board.queue)
        elif board.queue:
            domino_count = len(board.queue)
        else:
            # The last domino count is for progress toward a rectangular shape.
            xmin, xmax, ymin, ymax = board.get_bounds(cropped=True)
            width = xmax-xmin+1
            height = ymax-ymin+1
            domino_count = 1 - 2*len(board.dominoes)/(width*height)
        return domino_count


def main():
    find_boards_with_deap(graph_class=AddingBoardGraph,
                          board_class=QueuedBoard)


if __name__ == '__main__':
    main()
