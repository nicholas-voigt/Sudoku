from structure import SudokuGraph, SudokuMatrix


def backtrackingSolver(sudoku: SudokuGraph | SudokuMatrix, blanks: list[tuple[int, int]], idx: int = 0) -> bool:
    """Backtracking solver working on graph representation which tries only currently possible values based on the neighboring values."""    
    if idx == len(blanks):
        return True  # Solved
    
    r, c = blanks[idx]
    for value in range(1, sudoku.size + 1):
        if sudoku.setValue(r, c, value):
            if backtrackingSolver(sudoku, blanks, idx + 1):  # Recur with the remaining nodes
                return True
            sudoku.clearValue(r, c)  # Backtrack
    
    return False
