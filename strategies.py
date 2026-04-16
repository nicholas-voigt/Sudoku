from sudoku_graph import SudokuGraphNode
from matrix import SudokuMatrix


def graph_backtracking_solver(nodes: list[SudokuGraphNode], idx: int = 0) -> bool:
    """Backtracking solver working on graph representation which tries only currently possible values based on the neighboring values."""    
    if idx == len(nodes):
        return True  # Solved

    node = nodes[idx]

    for num in node.range:
        if node.check_value(num):  # Try only values that are not already used by neighbors
            node.set_value(num)
            if graph_backtracking_solver(nodes, idx + 1):  # Recur with the remaining nodes
                return True
            node.set_value(0)  # Backtrack
    
    return False


def matrix_backtracking_solver(matrix: SudokuMatrix, blanks: list[tuple[int, int]], idx: int = 0) -> bool:
    """Backtracking solver working on matrix representation. Tries only currently possible values based on the neighboring values."""
    if idx == len(blanks):
        return True  # Solved

    r, c = blanks[idx]
    for i, flag in enumerate(matrix.values[r][c]):
        if flag and matrix.check_value(r, c, i + 1):
            matrix.set_value(r, c, i + 1)
            if matrix_backtracking_solver(matrix, blanks, idx + 1):
                return True
            matrix.remove_value(r, c)  # Backtrack

    return False
