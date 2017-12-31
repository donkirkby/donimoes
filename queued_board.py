from domino_puzzle import Board, Domino


class QueuedBoard(Board):
    def __init__(self, width, height, max_pips=None):
        super().__init__(width, height, max_pips)
        self.queue = []

    @classmethod
    def create(cls, state, border=0, max_pips=None):
        board_state, *other_states = state.split('===\n')
        board = super().create(board_state, border, max_pips)
        if other_states:
            queue_state, = other_states
            for line in queue_state.splitlines():
                head = int(line[0])
                tail = int(line[-1])
                board.add_to_queue(Domino(head, tail))
        return board

    def __repr__(self):
        return 'QueuedBoard({}, {})'.format(self.width, self.height)

    def add_to_queue(self, domino):
        if self.extra_dominoes:
            self.extra_dominoes.remove(domino)
        self.queue.append(domino)

    def get_from_queue(self):
        return self.queue.pop(0)

    def display(self, cropped=False, cropping_bounds=None):
        display = super().display(cropped, cropping_bounds)
        if self.queue:
            display += '===\n'
            display += ''.join(domino.display()+'\n' for domino in self.queue)
        return display
