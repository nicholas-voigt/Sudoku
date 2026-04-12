### creates sudokus as graphs where fields are nodes and are connected to relevant adjacent fields (same quadrant, column, line)
from itertools import product


class SudokuGraph:
    def __init__(self, sub_size: int) -> None:
        self.sub_size = sub_size
        self.size = sub_size * sub_size
        self.nodes = {}  # (row, col) -> SudokuGraphNode
        # Build the empty graph structure
        self.build_graph()


    def build_graph(self):
        # Create nodes for each cell in the Sudoku grid
        self.nodes = {
            (r, c): SudokuGraphNode(r, c)
            for r, c in product(range(self.size), repeat=2)
        }

        # Create edges between nodes
        for r, c in product(range(self.size), repeat=2):
            node = self.nodes[(r, c)]
            # Peers in same row and column
            row_peers = {(r, cc) for cc in range(self.size) if cc != c}
            col_peers = {(rr, c) for rr in range(self.size) if rr != r}
            # Peers in same subgrid
            start_row = (r // self.sub_size) * self.sub_size
            start_col = (c // self.sub_size) * self.sub_size
            subgrid_peers = {
                (rr, cc)
                for rr, cc in product(range(start_row, start_row + self.sub_size), range(start_col, start_col + self.sub_size))
                if (rr, cc) != (r, c)
            }
            # Add peers as neighbors to the node
            for pr, pc in (row_peers | col_peers | subgrid_peers):
                node.add_neighbor(self.nodes[(pr, pc)])
    

    def __repr__(self) -> str:
        value_length = len(str(self.size))
        row_border = '+' + '-+'.join(['-' * (1 + value_length) * self.sub_size] * self.sub_size) + '-+\n'

        s = ''
        s += row_border

        for r in range(self.size):
            s += '|' 

            for c in range(self.size):
                node = self.nodes[(r, c)]
                value_str = str(node.value) if node.value != 0 else ' '
                s += f' {value_str:^{value_length}}{' |' if (c + 1) % self.sub_size == 0 else ''}'
            
            s += f'\n{row_border if (r + 1) % self.sub_size == 0 else ""}'  # End of row and add border after subgrid
        
        return s


class SudokuGraphNode:
    def __init__(self, row: int, col: int) -> None:
        self.position = (row, col)
        self.value = 0
        self.adjacent_nodes = set()
    
    def add_neighbor(self, neighbor_node: 'SudokuGraphNode'):
        self.adjacent_nodes.add(neighbor_node)
    
    def set_value(self, value: int | None, start_value: bool = False):
        self.value = value if value is not None else 0
        self.start_value = start_value
    
    def check_value(self, value: int) -> bool:
        for neighbor in self.adjacent_nodes:
            if neighbor.value == value:
                return False
        return True

