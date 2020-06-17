import re
from pathlib import Path

from adding_puzzle import AddingBoardGraph
from book_parser import parse, Styles
from domino_puzzle import BoardAnalysis, Board
from dominosa import DominosaBoard, FitnessCalculator, LEVEL_WEIGHTS, DominosaProblem
from mirror import MirrorFitnessCalculator, MirrorProblem


def main():
    rules_path = Path(__file__).parent / 'docs' / 'new_rules.md'
    rules_text = rules_path.read_text()

    states = parse(rules_text)
    summaries = []
    heading = ''
    is_dominosa = False
    is_mirror = False
    for state in states:
        if state.style == 'Heading2':
            is_dominosa = 'Dominosa' in state.text
            is_mirror = 'Mirror' in state.text
        if state.style == Styles.Diagram and heading.startswith('Problem'):
            if is_dominosa:
                summary = check_dominosa(state, heading)
            elif is_mirror:
                summary = check_mirror(state, heading)
            else:
                summary = check_other(state, heading)
            summaries.append(summary)
        if state.style.startswith(Styles.Heading):
            heading = state.text
    print(*summaries, sep='\n')


def check_dominosa(state, heading):
    """ Score solution to a Dominosa problem.

    Current fitness scores:
    1. 4x3 -21 (52 nodes)
    2. 5x4 -28 (398 nodes)
    3. 6x5 -42 (1746 nodes)
    4. 5x4 -36 (369 nodes)
    5. 6x5 -50 (909 nodes)
    6. 6x5 -50 (3212 nodes)
    7. 7x6 -70 (9369 nodes)
    8. 7x6 -71 (884 nodes)
    9. 6x5 -48 (3156 nodes)
    10. 6x5 -47 (4422 nodes)
    11. 7x6 -70 (5910 nodes)
    12. 7x6 -70 (9119 nodes)
    13. 8x7 -105 (8230 nodes)
    14. 8x7 -104 (4244 nodes)
    15. 6x5 -56 (2579 nodes)
    16. 6x5 -54 (6021 nodes)
    17. 7x6 -71 (3457 nodes)
    18. 7x6 -78 (9966 nodes)
    19. 8x7 -102 (2565 nodes)
    20. 8x7 -106 (4137 nodes)
    """
    n_text = heading.split(' ')[-1]
    n = int(re.match(r'\d+', n_text).group(0))
    if n <= 3:
        move_weights = LEVEL_WEIGHTS['easy']
    elif n <= 8:
        move_weights = LEVEL_WEIGHTS['medium']
    elif n <= 14:
        move_weights = LEVEL_WEIGHTS['hard']
    else:
        move_weights = LEVEL_WEIGHTS['tricky']
    fitness_calculator = FitnessCalculator(move_weights)
    board = DominosaBoard.create(state.text)
    board.max_pips = board.width - 2
    problem = DominosaProblem(dict(solution=board.display(),
                                   max_pips=board.max_pips))
    fitness_calculator.calculate(problem)
    print(n_text + '.', fitness_calculator.format_details())
    return n_text + '. ' + fitness_calculator.format_summaries()


def check_mirror(state, heading):
    """ Check solution to a mirror problem.

    Current details:
    1. 4x3: 6 moves, max 9, avg 6.571428571428571, 48 states
    2. 4x3: 6 moves, max 9, avg 7.285714285714286, 72 states
    3. 4x3: 12 moves, max 9, avg 7.230769230769231, 1032 states
    4. 5x4: 14 moves, max 10, avg 7.466666666666667, 1582 states
    5. 5x4: 18 moves, max 9, avg 7.578947368421052, 7461 states
    6. 5x4: 18 moves, max 10, avg 7.473684210526316, 3823 states
    7. 5x4: 18 moves, max 10, avg 8.210526315789474, 3933 states
    8. 5x4: 18 moves, max 11, avg 7.7368421052631575, 2513 states
    9. 5x4: 28 moves, max 11, avg 8.482758620689655, 23139 states
    10. 5x4: 29 moves, max 10, avg 8.0, 25404 states
    11. 5x4: 28 moves, max 10, avg 7.482758620689655, 15961 states
    12. 6x5: 29 moves, max 10, avg 7.766666666666667, 8086 states
    13. 6x5: 24 moves, max 9, avg 7.48, 7996 states
    14. 6x5: 27 moves, max 10, avg 8.464285714285714, 8339 states
    15. 7x6: 41 moves, max 11, avg 8.357142857142858, 109348 states
    16. 7x6: 49 moves, max 10, avg 7.38, 96395 states
    17. 7x6: 95 moves
    18. 8x7: 84 moves
    19. 8x7: 92 moves
    20. 8x7: 393 moves
    """
    n = heading.split(' ')[-1]
    size_limit = 1_000_000
    fitness_calculator = MirrorFitnessCalculator(size_limit=size_limit)
    problem = MirrorProblem(dict(start=state.text, max_pips=6))
    fitness_calculator.calculate(problem)
    print(n + '.', fitness_calculator.format_details())
    return n + '. ' + fitness_calculator.format_summaries()


def check_other(state, heading):
    n = heading.split(' ')[-1]
    board = Board.create(state.text)
    analysis = BoardAnalysis(board, AddingBoardGraph())
    if board.hasMatch():
        n += '(matches)'
    print(n + '. ' + ', '.join(analysis.solution).upper())
    score = BoardAnalysis.calculate_score(analysis.get_values())
    new_scores = '{}. {}x{} {} ({} nodes)\n'.format(n,
                                                    board.width,
                                                    board.height,
                                                    score,
                                                    analysis.graph_size)
    return new_scores


main()
