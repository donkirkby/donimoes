import re
from pathlib import Path

from adding_puzzle import AddingBoardGraph
from book_parser import parse, Styles
from domino_puzzle import BoardAnalysis, Board
from dominosa import DominosaBoard, FitnessCalculator, LEVEL_WEIGHTS, DominosaProblem


def main():
    rules_path = Path(__file__).parent / 'docs' / 'new_rules.md'
    rules_text = rules_path.read_text()

    states = parse(rules_text)
    summaries = []
    heading = ''
    is_dominosa = False
    for state in states:
        if state.style == 'Heading2':
            is_dominosa = 'Dominosa' in state.text
        if state.style == Styles.Diagram and heading.startswith('Problem'):
            if is_dominosa:
                summary = check_dominosa(state, heading)
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
