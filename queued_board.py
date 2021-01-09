from domino_puzzle import Board, Domino, DiceSet, ArrowSet


class QueuedBoard(Board):
    def __init__(self,
                 width: int,
                 height: int,
                 max_pips: int = None,
                 dice_set: DiceSet = None,
                 arrows: ArrowSet = None):
        super().__init__(width, height, max_pips, dice_set, arrows)
        self.queue = []

    @classmethod
    def create(cls, state, border=0, max_pips=None) -> 'QueuedBoard':
        board_state, *other_states = state.split('===\n')
        board = super().create(board_state, border, max_pips)
        if other_states:
            queue_state, = other_states
            heads, _, tails = queue_state.splitlines()
            for head, tail in zip(heads, tails):
                if head == ' ':
                    continue
                domino = Domino(int(head), int(tail))
                domino.rotate(-90)
                board.add_to_queue(domino)
        return board

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        return (len(self.queue) == len(other.queue) and
                all(d1.head.pips == d2.head.pips and
                    d1.tail.pips == d2.tail.pips and
                    d1.direction == d2.direction
                    for d1, d2 in zip(self.queue, other.queue)))

    def fill(self, random, matches_allowed=True, reset_cycles=True):
        queue_size = self.width * self.height // 2
        new_dominoes = random.sample(self.extra_dominoes, queue_size)
        for domino in new_dominoes:
            is_flipped = random.randint(0, 1)
            if is_flipped:
                domino.rotate(180)
            self.add_to_queue(domino)
        return True

    # noinspection PyPep8Naming
    def mutate(self, random, board_type=None, matches_allowed=True):
        new_board = board_type.create(self.display(), max_pips=self.max_pips)
        mutation_count = new_board.pick_mutation_count(len(new_board.queue),
                                                       random)
        for _ in range(mutation_count):
            i = random.randint(0, len(new_board.queue) - 1)
            domino = new_board.queue.pop(i)
            new_board.extra_dominoes.append(domino)
        new_dominoes = random.sample(new_board.extra_dominoes, mutation_count)
        for domino in new_dominoes:
            is_flipped = random.randint(0, 1)
            if is_flipped:
                domino.rotate(180)
            target_index = random.randint(0, len(new_board.queue))
            new_board.add_to_queue(domino, target_index)
        return new_board

    def __repr__(self):
        return 'QueuedBoard({}, {})'.format(self.width, self.height)

    def add_to_queue(self, domino, target_index=None):
        if self.extra_dominoes:
            self.extra_dominoes.remove(domino)
        if target_index is None:
            self.queue.append(domino)
        else:
            self.queue[target_index:target_index] = [domino]

    def get_from_queue(self):
        return self.queue.pop(0)

    def display(self, cropped=False, cropping_bounds=None):
        display = super().display(cropped, cropping_bounds)
        if self.queue:
            display += '===\n'
            queue_names = [domino.get_name() for domino in self.queue]
            display += ' '.join(name[0] for name in queue_names) + '\n'
            display += ' '.join('-' for _ in queue_names) + '\n'
            display += ' '.join(name[1] for name in queue_names) + '\n'
        return display
