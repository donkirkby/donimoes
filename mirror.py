import random
import typing
from sys import maxsize

from domino_puzzle import Board, BadPositionError, Domino, BoardGraph, Cell, GraphLimitExceeded
from evo import Individual, Evolution


def get_cell_marker(cell: Cell) -> str:
    board = cell.board
    return board.markers.get((cell.x, cell.y))


class MirrorGraph(BoardGraph):
    def __init__(self, board_class=Board):
        super().__init__(board_class)
        self.min_marker_area = None

    def generate_moves(self, board: Board):
        if board.are_markers_connected:
            if self.last is None:
                self.last = '0|0\n---\n1'
            yield 'SOLVED', self.last
            return
        marker_area = board.marker_area
        if self.min_marker_area is None or marker_area < self.min_marker_area:
            self.min_marker_area = marker_area
        for domino in board.dominoes[:]:
            dx, dy = domino.direction
            yield from self.try_move_domino(domino, dx, dy)
            yield from self.try_move_domino(domino, -dx, -dy)
        for x, y in list(board.markers.keys()):
            for dx, dy in Domino.directions:
                yield from self.try_move_marker(board, x, y, dx, dy)

    def try_move_marker(self, board: Board, x: int, y: int, dx: int, dy: int):
        try:
            move, new_state, heuristic = self.move_marker(board, x, y, dx, dy)
            yield move, new_state, None, heuristic
        except BadPositionError:
            pass

    def move_marker(self, board: Board, x: int, y: int, dx: int, dy: int):
        x2 = x+dx
        y2 = y+dy
        new_cell = board[x2][y2]
        if new_cell is None:
            raise BadPositionError('Marker cannot move off the board.')
        if (x2, y2) in board.markers:
            raise BadPositionError(f'A marker is already on {x2}, {y2}.')
        start_cell = board[x][y]
        if new_cell.domino is not start_cell.domino:
            start_pips = start_cell.pips
            new_pips = new_cell.pips
            if new_pips != start_pips:
                raise BadPositionError(
                    f"Marker cannot move from {start_pips} to {new_pips}.")
        direction_name = Domino.describe_direction(dx, dy).upper()
        marker = board.markers.pop((x, y))
        board.markers[(x2, y2)] = marker
        move = f'{marker}{direction_name}'

        new_state = board.display(cropped=True)
        heuristic = self.calculate_heuristic(board)

        del board.markers[(x2, y2)]
        board.markers[(x, y)] = marker
        return move, new_state, heuristic

    def try_move_domino(self, domino: Domino, dx: int, dy: int):
        try:
            move, new_state, heuristic = self.move_domino(domino, dx, dy)
            yield move, new_state, None, heuristic
        except BadPositionError:
            pass

    def move_domino(self, domino: Domino, dx, dy):
        head_marker = get_cell_marker(domino.head)
        tail_marker = get_cell_marker(domino.tail)
        marker = head_marker or tail_marker
        if marker is None:
            raise BadPositionError('Cannot move a domino with no markers on it.')
        board: Board = domino.head.board
        direction_name = domino.describe_direction(dx, dy).upper()
        move = f'{marker}D{direction_name}'
        original_markers = board.markers.copy()
        try:
            if head_marker:
                del board.markers[(domino.head.x, domino.head.y)]
            if tail_marker:
                del board.markers[(domino.tail.x, domino.tail.y)]

            domino.move(dx, dy)
            if head_marker:
                board.markers[(domino.head.x, domino.head.y)] = head_marker
            if tail_marker:
                board.markers[(domino.tail.x, domino.tail.y)] = tail_marker
        except Exception:
            board.markers = original_markers
            raise
        try:
            if not board.is_connected():
                raise BadPositionError('Board is not connected.')
            heuristic = self.calculate_heuristic(board)
            return move, board.display(cropped=True), heuristic
        finally:
            domino.move(-dx, -dy)
            board.markers = original_markers

    def calculate_heuristic(self, board):
        # Calculate centre of mass for markers.
        x_sum = y_sum = 0
        for x, y in board.markers:
            x_sum += x
            y_sum += y
        marker_count = len(board.markers)
        cx = x_sum // marker_count
        cy = y_sum // marker_count

        # Count moves to centre.
        total_moves = 0
        for x, y in board.markers:
            total_moves += abs(x - cx) + abs(y-cy)

        # Not all pieces have to get all the way to the centre.
        total_moves -= min(total_moves, marker_count)
        return total_moves

    def get_solution(self, return_partial=False, solution_nodes=None):
        solution = super().get_solution(return_partial, solution_nodes)
        assert solution[-1] == 'SOLVED'
        return solution[:-1]

    def walk(self, board, size_limit=maxsize) -> typing.Set[str]:
        if not board.markers and len(board.dominoes) > 1:
            board.markers[(0, 0)] = 'N'
            board.markers[(board.width-1, 0)] = 'R'
            board.markers[(0, board.height-1)] = 'P'
            board.markers[(board.width-1, board.height-1)] = 'B'

        return super().walk(board, size_limit)


class MirrorProblem(Individual):
    def __repr__(self):
        return f'MirrorProblem({self.value!r}'

    def pair(self, other, pair_params):
        return MirrorProblem(self.value)

    def mutate(self, mutate_params):
        max_pips = self.value['max_pips']
        board = Board.create(self.value['start'], max_pips=max_pips)
        new_board = board.mutate(random, Board)
        self.value = dict(start=new_board.display(), max_pips=max_pips)

    def _random_init(self, init_params):
        max_pips = init_params['max_pips']
        board = Board(**init_params)
        while True:
            if board.fill(random):
                break

        return dict(start=board.display(), max_pips=max_pips)


class FitnessCalculator:
    def __init__(self, target_length=None):
        self.target_length = target_length

    def calculate(self, problem):
        """ Calculate fitness score based on the solution length.

        -100,000 if there's no solution.
        -1000 * abs(solution_length-target_length)
        -10*max_choices
        -avg_choices
        """
        value = problem.value
        fitness = value.get('fitness')
        if fitness is not None:
            return fitness
        board = Board.create(value['start'], max_pips=value['max_pips'])
        graph = MirrorGraph()
        fitness = 0
        try:
            graph.walk(board, size_limit=10_000)
        except GraphLimitExceeded:
            pass
        if graph.last is None:
            fitness -= 100_000
            fitness -= graph.min_marker_area
        else:
            solution_nodes = graph.get_solution_nodes()
            solution_moves = graph.get_solution(solution_nodes=solution_nodes)
            domino_move_count = sum(len(move) == 3 for move in solution_moves)
            fitness += 300*domino_move_count
            if self.target_length is None:
                fitness += len(solution_nodes)*1000
            else:
                fitness -= 1000*abs(len(solution_nodes) - self.target_length)

            max_choices = graph.get_max_choices(solution_nodes)
            average_choices = graph.get_average_choices(solution_nodes)
            fitness -= max_choices*10
            fitness -= average_choices

        value['fitness'] = fitness
        return fitness


def main():
    max_pips = 5
    fitness_calculator = FitnessCalculator(target_length=50)
    init_params = dict(max_pips=max_pips, width=max_pips+1, height=max_pips)
    evo = Evolution(
        pool_size=100,
        fitness=fitness_calculator.calculate,
        individual_class=MirrorProblem,
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
        print(i, top_fitness, mid_fitness, repr(top_individual.value['start']))
        hist.append(top_fitness)
        evo.step()

    best = evo.pool.individuals[-1]
    for problem in evo.pool.individuals:
        print(evo.pool.fitness(problem))
    # plt.plot(hist)
    # plt.show()
    start = best.value['start']
    print(start)


if __name__ == '__main__':
    main()
