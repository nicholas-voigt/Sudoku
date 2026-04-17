### Wrapper to handle the solving of a sudoku graph with different strategies.

from structure import SudokuGraph, SudokuMatrix
from strategies import backtrackingSolver


def solve_sudoku(sudoku: SudokuGraph | SudokuMatrix, method: str = 'standard') -> bool:
    if method == 'standard':
        cellsToFill = sudoku.getBlanks()
        return backtrackingSolver(sudoku, cellsToFill)

    else:
        raise ValueError(f"Unknown solving method: {method}")
