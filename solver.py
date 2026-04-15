### Wrapper to handle the solving of a sudoku graph with different strategies.

from sudoku_graph import SudokuGraph
from strategies import backtracking_solver


def solve_sudoku(sudoku: SudokuGraph, method: str = 'standard') -> bool:
    if method == 'standard':
        cells_to_fill = [node for node in sudoku.nodes.values() if node.value == 0]
        return backtracking_solver(cells_to_fill)
    
    else:
        raise ValueError(f"Unknown solving method: {method}")
