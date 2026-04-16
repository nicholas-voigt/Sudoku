# Script to fill a generated Sudoku graph with starting values.
# Option 1 (Interim): Use py-sudoku library.
# Option 2: Create a complete solution and then remove values to create a puzzle.

from sudoku import Sudoku
from itertools import product
from sudoku_graph import SudokuGraph
from matrix import SudokuMatrix


def fill_sudoku(sudoku_structure: SudokuGraph | SudokuMatrix, method: int = 0 | 1, **kwargs):
    """Fills the given Sudoku structure with starting values based on the specified method.
    Args:
        sudoku_structure: The SudokuGraph or SudokuMatrix to fill.
        method: The method to use for filling the Sudoku (0 for py-sudoku, 1 for given values in kwargs).
        kwargs: Additional parameters for the filling method (e.g., difficulty level).
    Returns:
        None. The sudoku_structure is modified in place.
    """
    if method == 0:
        sub_size = sudoku_structure.sub_size
        difficulty = kwargs.get('difficulty', 0.5)
        sudoku = Sudoku(sub_size).difficulty(difficulty)

    elif method == 1:
        sudoku = kwargs.get('sudoku_board')
        assert sudoku is not None, "Method 1 requires a 'sudoku_board' parameter in kwargs."
        assert is_valid_board(sudoku), "The 'sudoku_board' parameter is not a valid Sudoku board."
        
    else:
        raise ValueError("Invalid method. Supported methods are 0 (py-sudoku) and 1 (given board).")

    for r, c in product(range(sudoku_structure.size), repeat=2):
        value = sudoku.board[r][c]
        if value is not None:
            if isinstance(sudoku_structure, SudokuGraph):
                sudoku_structure.nodes[(r, c)].set_value(value, start_value=True)
            elif isinstance(sudoku_structure, SudokuMatrix):
                sudoku_structure.set_value(r, c, value, update=True, preassigned=True)


def is_valid_board(x: object) -> bool:
    """Checkss if the object is a valid sudoku board as list[list[int | None]]."""
    if not isinstance(x, list):
        return False
    if not all(isinstance(row, list) for row in x):
        return False
    if not all(isinstance(cell, (int, type(None))) for row in x for cell in row):
        return False
    return True