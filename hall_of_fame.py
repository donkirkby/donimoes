from deap.tools.support import HallOfFame
from operator import eq
import domino_puzzle


class MappedHallOfFame(HallOfFame):
    def __init__(self,
                 maxsize,
                 similar=eq,
                 filename="leader.log",
                 solution_length_index=1):
        super(MappedHallOfFame, self).__init__(maxsize, similar)
        self.solution_length_index = solution_length_index
        self.filename = filename
        self.file_mode = 'w'
        self.map = {}  # {solution_length: best_item}

    def update(self, population):
        old_leader = self and self[0] or None
        super(MappedHallOfFame, self).update(population)
        new_leader = self[0]
        if old_leader is None or new_leader != old_leader:
            self.log(new_leader)

    def insert(self, item):
        solution_length = item.fitness.values[self.solution_length_index]
        best_item = self.map.get(solution_length)
        if best_item is None or item.fitness > best_item.fitness:
            if best_item is not None:
                try:
                    self.items.remove(best_item)
                except ValueError:
                    pass
            super(MappedHallOfFame, self).insert(item)
            self.map[solution_length] = item

    def log(self, board):
        display = board.display()
        with open(self.filename, self.file_mode) as f:
            f.write(display)
        self.file_mode = 'a'

    def display(self, graph_class):
        for board in self:
            analysis = domino_puzzle.BoardAnalysis(board, graph_class())
            print()
            print(analysis.start.replace('x', ' '))
            score = board.fitness.values[0]
            if score < 0:
                print('{} score.'.format(score))
            else:
                print(analysis.display())
