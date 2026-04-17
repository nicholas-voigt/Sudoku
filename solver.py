### Wrapper to handle the solving of a sudoku graph with different strategies.

from structure import SudokuGraph, SudokuMatrix
from strategies import graph_backtracking_solver, matrix_backtracking_solver


def solve_sudoku(sudoku: SudokuGraph | SudokuMatrix, method: str = 'standard') -> bool:
    if method == 'standard':
        cellsToFill = sudoku.getBlanks()

        if isinstance(sudoku, SudokuGraph):
            return graph_backtracking_solver(sudoku, cellsToFill)
        elif isinstance(sudoku, SudokuMatrix):
            return matrix_backtracking_solver(sudoku, cellsToFill)

    else:
        raise ValueError(f"Unknown solving method: {method}")
