from book_parser import parse, Styles
from domino_puzzle import BoardAnalysis, Board


def main():
    with open('rules.md', 'rU') as f:
        rules_text = f.read()

    states = parse(rules_text)
    scores = ''
    heading = ''
    for state in states:
        if state.style == Styles.Diagram and heading.startswith('Problem'):
            n = heading.split(' ')[-1]
            board = Board.create(state.text)
            analysis = BoardAnalysis(board)
            if board.hasMatch():
                n += '(matches)'
            print(n + '. ' + ', '.join(analysis.solution).upper())
            score = BoardAnalysis.calculate_score(analysis.get_values())
            scores += '{}. {}x{} {} ({} nodes)\n'.format(n,
                                                         board.width,
                                                         board.height,
                                                         score,
                                                         analysis.graph_size)
        if state.style.startswith(Styles.Heading):
            heading = state.text
    print(scores)

if __name__ == '__main__':
    main()
