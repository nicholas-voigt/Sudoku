### This module defines the possible structures to represent a Sudoku puzzle.
### Current implemenetations:
### - SudokuGraph: A graph-based representation where each cell is a node and edges represent constraints between cells.
### - SudokuMatrix: A matrix-based representation where the Sudoku grid is represented as a 2D list.

from abc import ABC, abstractmethod
from itertools import product


class SudokuStructure(ABC):
    """Base class for Sudoku structures. Not meant to be instantiated directly."""
    def __init__(self, sub_size: int):
        self.sub_size = sub_size
        self.size = sub_size * sub_size

    @abstractmethod
    def getValue(self, r: int, c: int) -> int:
        """Returns the value at cell (r, c) or 0 if blank."""
        ...
    
    @abstractmethod
    def checkValue(self, r: int, c: int, v: int) -> bool:
        """Returns whether v is valid at (r, c) in current state."""
        ...

    @abstractmethod
    def setValue(self, r: int, c: int, v: int, preassigned: bool = False) -> None:
        """Sets v as value of cell (r, c). Raises Error if values are out of bounds or cell is preassigned. Does not check validity of value"""
        ...
    
    @abstractmethod
    def clearValue(self, r: int, c: int) -> None:
        """Backtracking function, clears the value of the given cell (r, c)."""
        ...
    
    @abstractmethod
    def getBlanks(self) -> list[tuple[int, int]]:
        """Returns a list of coordinates from empty cells in the Sudoku."""
        ...

    def checkSolution(self) -> bool:
        """Checks if the current sudoku is a valid solution."""
        for r, c in product(range(self.size), repeat=2):
            num = self.getValue(r, c)
            if num == 0 or not self.checkValue(r, c, num):
                return False
        return True
    
    def __repr__(self) -> str:
        s = ''
        value_length = len(str(self.size))
        row_border = '+' + '-+'.join(['-' * (1 + value_length) * self.sub_size] * self.sub_size) + '-+\n'
        s += row_border

        for r in range(self.size):
            s += '|' 
            for c in range(self.size):
                value = self.getValue(r, c)
                value_str = str(value) if value != 0 else ' '
                s += f' {value_str:^{value_length}}{' |' if (c + 1) % self.sub_size == 0 else ''}'
            s += f'\n{row_border if (r + 1) % self.sub_size == 0 else ""}'  # End of row and add border after subgrid
        return s


class SudokuGraph(SudokuStructure):
    def __init__(self, sub_size: int) -> None:
        super().__init__(sub_size)
        self.nodes = {}  # (row, col) -> SudokuGraphNode
        self._buildGraph()

    def getValue(self, r: int, c: int) -> int:
        return self.nodes[(r, c)].value    

    def checkValue(self, r: int, c: int, v: int) -> bool:
        if not (0 <= r < self.size and 0 <= c < self.size and 1 <= v <= self.size):
            raise ValueError("Invalid inputs")
        node = self.nodes[(r, c)]
        for neighbor in node.adjacent_nodes:
            if neighbor.value == v:
                return False
        return True
    
    def setValue(self, r: int, c: int, v: int, preassigned: bool = False) -> None:
        if not (0 <= r < self.size and 0 <= c < self.size and 1 <= v <= self.size):
            raise ValueError("Invalid inputs")
        node = self.nodes[(r, c)]
        assert not node.preassigned
        node.value = v
        node.preassigned = preassigned
        return
    
    def clearValue(self, r: int, c: int) -> None:
        if not (0 <= r < self.size and 0 <= c < self.size):
            raise ValueError("Invalid inputs")
        node = self.nodes[(r, c)]
        assert not node.preassigned
        node.value = 0
        return
    
    def getBlanks(self) -> list[tuple[int, int]]:
        return [node.position for node in self.nodes.values() if node.value == 0]

    def _buildGraph(self):
        # Create nodes for each cell in the Sudoku grid
        self.nodes = {
            (r, c): SudokuGraphNode(r, c, set(range(1, self.size + 1)))
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
                node.adjacent_nodes.add(self.nodes[(pr, pc)])


class SudokuGraphNode:
    def __init__(self, r: int, c: int, value_range: set) -> None:
        self.position = (r, c)
        self.preassigned = False
        self.value = 0
        self.range = value_range
        self.adjacent_nodes = set()
    

class SudokuMatrix(SudokuStructure):
    def __init__(self, sub_size: int):
        super().__init__(sub_size)
        self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]  # Assigned values, initially all 0
        self.values = [[[True for _ in range(self.size)]  # Possible values for each cell, initially all True
                        for _ in range(self.size)]
                        for _ in range(self.size)]
        self.preassigned = [[False for _ in range(self.size)] for _ in range(self.size)]  # Track preassigned cells

    def getValue(self, r: int, c: int) -> int:
        return self.matrix[r][c]

    def checkValue(self, r: int, c: int, v: int) -> bool:
        if not (0 <= r < self.size and 0 <= c < self.size and 1 <= v <= self.size):
            raise ValueError("Invalid inputs")
        # Check row and column
        for i in range(self.size):
            if self.matrix[r][i] == v and i != c:  # Check row
                return False
            if self.matrix[i][c] == v and i != r:  # Check column
                return False
        # Check subgrid
        start_row = (r // self.sub_size) * self.sub_size
        start_col = (c // self.sub_size) * self.sub_size
        for rr, cc in product(range(start_row, start_row + self.sub_size), range(start_col, start_col + self.sub_size)):
            if self.matrix[rr][cc] == v and (rr, cc) != (r, c):
                return False
        return True
    
    def setValue(self, r: int, c: int, v: int, preassigned: bool = False) -> None:
        if not (0 <= r < self.size and 0 <= c < self.size and 1 <= v <= self.size):
            raise ValueError("Invalid inputs")
        
        if self.preassigned[r][c]:
            raise ValueError("Cannot change a preassigned value")
        
        # if self.values[r][c][v - 1] == False:
        #     raise ValueError("Value not possible for this cell")
        
        self.matrix[r][c] = v
        self.preassigned[r][c] = preassigned

        # if update:
        #     # Update possible values for the same row & column
        #     for i in range(self.size):
        #         if i != c:  # Same row
        #             self.values[r][i][v - 1] = False
        #         if i != r:  # Same column
        #             self.values[i][c][v - 1] = False
            
        #     # Update possible values for the same subgrid
        #     start_row = (r // self.sub_size) * self.sub_size
        #     start_col = (c // self.sub_size) * self.sub_size
        #     for rr, cc in product(range(start_row, start_row + self.sub_size), range(start_col, start_col + self.sub_size)):
        #         if (rr, cc) != (r, c):
        #             self.values[rr][cc][v - 1] = False
        return
    

    def clearValue(self, r: int, c: int) -> None:
        if not (0 <= r < self.size and 0 <= c < self.size):
            raise ValueError("Invalid inputs")
        if self.preassigned[r][c]:
            raise ValueError("Cannot remove a preassigned value")
        self.matrix[r][c] = 0
        return

    def getBlanks(self) -> list[tuple[int, int]]:
        return [(r, c) for r, c in product(range(self.size), repeat=2) if self.matrix[r][c] == 0]
    