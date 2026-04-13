### Wrapper to handle the solving of a sudoku graph with different strategies.

from sudoku_graph import SudokuGraph
from strategies import brute_force


def solve_sudoku(sudoku: SudokuGraph, method: str = 'brute_force') -> bool:
    if method == 'brute_force':
        cells_to_fill = [node for node in sudoku.nodes.values() if node.value == 0]
        return brute_force(cells_to_fill)
    else:
        raise ValueError(f"Unknown solving method: {method}")