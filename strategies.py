from structure import SudokuGraph, SudokuMatrix


def graph_backtracking_solver(graph: SudokuGraph, blanks: list[tuple[int, int]], idx: int = 0) -> bool:
    """Backtracking solver working on graph representation which tries only currently possible values based on the neighboring values."""    
    if idx == len(blanks):
        return True  # Solved
    
    r, c = blanks[idx]
    for value in graph.nodes[(r, c)].range:
        if graph.checkValue(r, c, value):  # Try only values that are not already used by neighbors
            graph.setValue(r, c, value)
            if graph_backtracking_solver(graph, blanks, idx + 1):  # Recur with the remaining nodes
                return True
            graph.clearValue(r, c)  # Backtrack
    
    return False


def matrix_backtracking_solver(matrix: SudokuMatrix, blanks: list[tuple[int, int]], idx: int = 0) -> bool:
    """Backtracking solver working on matrix representation. Tries only currently possible values based on the neighboring values."""
    if idx == len(blanks):
        return True  # Solved

    r, c = blanks[idx]
    for i, flag in enumerate(matrix.values[r][c]):
        if flag and matrix.checkValue(r, c, i + 1):
            matrix.setValue(r, c, i + 1)
            if matrix_backtracking_solver(matrix, blanks, idx + 1):
                return True
            matrix.clearValue(r, c)  # Backtrack

    return False
