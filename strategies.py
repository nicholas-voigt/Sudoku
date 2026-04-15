from sudoku_graph import SudokuGraphNode


def backtracking_solver(nodes: list[SudokuGraphNode], idx: int = 0) -> bool:
    """Backtracking solver which tries only currently possible values based on the neighboring values."""    
    if idx == len(nodes):
        return True  # Solved

    node = nodes[idx]

    for num in node.range:
        if node.check_value(num):  # Try only values that are not already used by neighbors
            node.set_value(num)
            if backtracking_solver(nodes, idx + 1):  # Recur with the remaining nodes
                return True
            node.set_value(0)  # Backtrack
    
    return False


