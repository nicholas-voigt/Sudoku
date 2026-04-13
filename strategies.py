from sudoku_graph import SudokuGraph

def brute_force(sudoku: SudokuGraph) -> bool:
    """Brute-force backtracking solver."""
    # Find next empty cell
    empty_cell = None
    for _, node in sudoku.nodes.items():
        if node.value == 0:
            empty_cell = node
            break
    
    if not empty_cell:
        return True  # Solved
    
    for num in range(1, sudoku.size + 1):
        if empty_cell.check_value(num):
            empty_cell.set_value(num)
            if brute_force(sudoku):
                return True
            empty_cell.set_value(0)  # Backtrack
    
    return False

