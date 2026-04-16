### Wrapper to handle the solving of a sudoku graph with different strategies.

from sudoku_graph import SudokuGraph
from matrix import SudokuMatrix
from strategies import graph_backtracking_solver, matrix_backtracking_solver


def solve_sudoku(sudoku: SudokuGraph | SudokuMatrix, method: str = 'standard') -> bool:
    if method == 'standard':
        if isinstance(sudoku, SudokuGraph):
            cells_to_fill = [node for node in sudoku.nodes.values() if node.value == 0]
            return graph_backtracking_solver(cells_to_fill)
        
        elif isinstance(sudoku, SudokuMatrix):
            cells_to_fill = sudoku.get_blanks()
            return matrix_backtracking_solver(sudoku, cells_to_fill)

    else:
        raise ValueError(f"Unknown solving method: {method}")
