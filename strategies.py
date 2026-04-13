from sudoku_graph import SudokuGraphNode


def brute_force(nodes: list[SudokuGraphNode], idx: int = 0) -> bool:
    """Brute-force backtracking solver."""    
    if idx == len(nodes):
        return True  # Solved

    node = nodes[idx]

    for num in node.range:
        if node.check_value(num):
            node.set_value(num)
            if brute_force(nodes, idx + 1):  # Recur with the remaining nodes
                return True
            node.set_value(0)  # Backtrack
    
    return False


