# Script to fill a generated Sudoku graph with starting values.
# Option 1 (Intermediate): Use py-sudoku library.
# Option 2: Create a complete solution and then remove values to create a puzzle.

from sudoku import Sudoku
from itertools import product
from sudoku_graph import SudokuGraph

def fill_sudoku_graph(sudoku_graph: SudokuGraph, method: int = 0 | 1, **kwargs):
    if method == 0:
        # Use py-sudoku to generate a complete Sudoku and fill the graph
        sub_size = sudoku_graph.sub_size
        difficulty = kwargs.get('difficulty', 0.5)
        sudoku = Sudoku(sub_size).difficulty(difficulty)

        for r, c in product(range(sudoku_graph.size), repeat=2):
            value = sudoku.board[r][c]
            sudoku_graph.nodes[(r, c)].set_value(value)

    elif method == 1:
        # Create a complete solution and then remove values to create a puzzle
        # This is a more complex approach and may require backtracking to ensure a valid solution
        pass  # Placeholder for custom implementation