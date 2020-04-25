from pathlib import Path

from networkx import shortest_path, edges, DiGraph, NetworkXNoPath

from adding_puzzle import AddingBoardGraph
from book_parser import parse, Styles
from domino_puzzle import BoardAnalysis, Board, GraphLimitExceeded
from dominosa import DominosaBoard, DominosaGraph


def main():
    rules_path = Path(__file__).parent / 'docs' / 'new_rules.md'
    rules_text = rules_path.read_text()

    states = parse(rules_text)
    scores = ''
    heading = ''
    is_dominosa = False
    for state in states:
        if state.style == 'Heading2':
            is_dominosa = 'Dominosa' in state.text
        if state.style == Styles.Diagram and heading.startswith('Problem'):
            if is_dominosa:
                new_scores = check_dominosa(state, heading)
            else:
                new_scores = check_other(state, heading)
            scores += new_scores
        if state.style.startswith(Styles.Heading):
            heading = state.text
    print(scores)


def check_dominosa(state, heading):
    n = heading.split(' ')[-1]
    board = DominosaBoard.create(state.text)
    board.max_pips = board.width - 2
    graph = DominosaGraph(move_weights={1: 1,
                                        2: 3,
                                        3: 3,
                                        4: 3,
                                        5: 4,
                                        6: 10})
    fitness = 0
    try:
        graph.walk(board, size_limit=10_000)
    except GraphLimitExceeded:
        if graph.last is None:
            raise
        fitness -= 1_000_000
    assert graph.last is not None
    solution_nodes = shortest_path(graph.graph,
                                   graph.start,
                                   graph.last,
                                   'weight')
    moves = []
    for i in range(len(solution_nodes)-1):
        source, target = solution_nodes[i:i+2]
        edge = graph.graph[source][target]
        fitness -= edge.get('weight', 1)
        moves.append(edge.get('move'))
    required_moves = []
    for excluded_move_num in graph.move_weights:
        remaining_graph = DiGraph()
        for a, b in edges(graph.graph):
            edge_attrs = graph.graph[a][b]
            if edge_attrs.get('move_num') != excluded_move_num:
                remaining_graph.add_edge(a, b, **edge_attrs)
        try:
            shortest_path(remaining_graph, graph.start, graph.last, 'weight')
        except (NetworkXNoPath, KeyError):
            required_moves.append(excluded_move_num)
    required_moves.sort()
    print(n + '. ' + '; '.join(moves), '==>', fitness)
    print('required moves:', required_moves)
    print(graph.last)
    new_scores = '{}. {}x{} {} ({} nodes)\n'.format(n,
                                                    board.width,
                                                    board.height,
                                                    fitness,
                                                    len(graph.graph))
    return new_scores


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
