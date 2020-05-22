from enum import Enum

from domino_puzzle import Board, BadPositionError, Domino

LadderMoveType = Enum('LadderMoveType', 'MARKER DOMINO')


class LadderBoard(Board):
    @classmethod
    def create(cls, state, border=0, max_pips: int = None):
        """ Create a ladder board.

        :param state: Standard board state, plus '---' and an extra status line
            that holds the move type and the target number. Move type is 'M' for
            marker and 'D' for domino, so 'D2' means a domino move with a target
            of 2.
        :param border: number of blank rows and columns to add around the edge
        :param max_pips: maximum number of pips in the full set of dominoes
        """
        divider = '\n---\n'
        sections = state.split(divider)
        move_state = sections.pop()
        board_state = divider.join(sections)
        board = super().create(board_state, border, max_pips)
        board.move_type = (LadderMoveType.MARKER
                           if move_state[0] == 'M'
                           else LadderMoveType.DOMINO)
        board.target = int(move_state[1:])
        return board

    def __init__(self, width, height, max_pips=None):
        super().__init__(width, height, max_pips)
        self.target = 1
        self.move_type = LadderMoveType.MARKER

    def display(self, cropped=False, cropping_bounds=None):
        domino_display = super().display(cropped, cropping_bounds)
        move_char = self.move_type.name[0]
        return f'{domino_display}---\n{move_char}{self.target}\n'


class LadderGraph:
    def __init__(self):
        self.is_started = False

    def generate_moves(self, board: LadderBoard):
        self.is_started = True

        # Passing is always a legal domino move.
        board.move_type = LadderMoveType.MARKER
        yield 'D...', board.display(cropped=True)
        board.move_type = LadderMoveType.DOMINO

        for domino in board.dominoes:
            dx, dy = domino.direction
            yield from self.try_move_domino(domino, dx, dy)
            yield from self.try_move_domino(domino, -dx, -dy)

    def try_move_domino(self, domino: Domino, dx: int, dy: int):
        try:
            move, new_state = self.move_domino(domino, dx, dy)
            yield move, new_state
        except BadPositionError:
            pass

    @staticmethod
    def move_domino(domino, dx, dy):
        domino_markers = {
            (cell.x, cell.y): domino.head.board.markers.get((cell.x, cell.y))
            for cell in (domino.head, domino.tail)}
        domino_markers = {position: marker
                          for position, marker in domino_markers.items()
                          if marker is not None}
        if not domino_markers:
            raise BadPositionError('Cannot move domino without marker.')
        board = domino.head.board
        original_markers = board.markers.copy()
        domino.move(dx, dy)
        board.move_type = LadderMoveType.MARKER
        for position, marker in domino_markers.items():
            if marker is not None:
                del board.markers[position]
        for (x, y), marker in domino_markers.items():
            if marker is not None:
                board.markers[(x+dx, y+dy)] = marker
        try:
            if not board.isConnected():
                raise BadPositionError('Board is not connected.')
            direction_name = domino.describe_direction(dx, dy).upper()
            marker, *_ = domino_markers.values()
            return 'D'+marker+direction_name, board.display(cropped=True)
        finally:
            board.move_type = LadderMoveType.DOMINO
            domino.move(-dx, -dy)
            board.markers = original_markers
