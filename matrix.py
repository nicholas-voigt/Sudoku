from itertools import product

class SudokuMatrix:
    def __init__(self, sub_size: int):
        self.sub_size = sub_size
        self.size = sub_size * sub_size
        self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]  # Assigned values, initially all 0
        self.values = [[[True for _ in range(self.size)]  # Possible values for each cell, initially all True
                        for _ in range(self.size)]
                        for _ in range(self.size)]
        self.preassigned = [[False for _ in range(self.size)] for _ in range(self.size)]  # Track preassigned cells
    

    def set_value(self, r: int, c: int, num: int, update: bool = False, preassigned: bool = False) -> None:
        """Sets the value of a cell and updates the possible values of its neighbors if flag is True."""
        if not (0 <= r < self.size and 0 <= c < self.size and 1 <= num <= self.size):
            raise ValueError("Invalid inputs")
        
        if self.preassigned[r][c]:
            raise ValueError("Cannot change a preassigned value")
        
        if self.values[r][c][num - 1] == False:
            raise ValueError("Value not possible for this cell")
        
        self.matrix[r][c] = num
        self.preassigned[r][c] = preassigned

        if update:
            # Update possible values for the same row & column
            for i in range(self.size):
                if i != c:  # Same row
                    self.values[r][i][num - 1] = False
                if i != r:  # Same column
                    self.values[i][c][num - 1] = False
            
            # Update possible values for the same subgrid
            start_row = (r // self.sub_size) * self.sub_size
            start_col = (c // self.sub_size) * self.sub_size
            for rr, cc in product(range(start_row, start_row + self.sub_size), range(start_col, start_col + self.sub_size)):
                if (rr, cc) != (r, c):
                    self.values[rr][cc][num - 1] = False
        return
    

    def remove_value(self, r: int, c: int) -> None:
        """Removes the value of a cell and resets the possible values of its neighbors if it was not preassigned."""
        if not (0 <= r < self.size and 0 <= c < self.size):
            raise ValueError("Invalid inputs")
        
        if self.preassigned[r][c]:
            raise ValueError("Cannot remove a preassigned value")
        
        self.matrix[r][c] = 0
        return
    

    def check_value(self, r: int, c: int, num: int) -> bool:
        """Checks if a value is possible for a cell based on the current state of the matrix."""
        if not (0 <= r < self.size and 0 <= c < self.size and 1 <= num <= self.size):
            raise ValueError("Invalid inputs")
        
        for i in range(self.size):
            if self.matrix[r][i] == num and i != c:  # Check row
                return False
            if self.matrix[i][c] == num and i != r:  # Check column
                return False
            
        start_row = (r // self.sub_size) * self.sub_size
        start_col = (c // self.sub_size) * self.sub_size
        for rr, cc in product(range(start_row, start_row + self.sub_size), range(start_col, start_col + self.sub_size)):
            if self.matrix[rr][cc] == num and (rr, cc) != (r, c):  # Check subgrid
                return False
            
        return True
    

    def get_blanks(self) -> list[tuple[int, int]]:
        """Returns a list of coordinates for cells that are still blank (value 0)."""
        blanks = []
        for r, c in product(range(self.size), repeat=2):
            if self.matrix[r][c] == 0:
                blanks.append((r, c))
        return blanks
    

    def check_solution(self) -> bool:
        """Checks if the current matrix is a valid solution."""
        for r, c in product(range(self.size), repeat=2):
            num = self.matrix[r][c]
            if num == 0 or not self.check_value(r, c, num):
                return False
        return True
    
    
    def __repr__(self) -> str:
        value_length = len(str(self.size))
        row_border = '+' + '-+'.join(['-' * (1 + value_length) * self.sub_size] * self.sub_size) + '-+\n'

        s = ''
        s += row_border

        for r in range(self.size):
            s += '|' 

            for c in range(self.size):
                value = self.matrix[r][c]
                value_str = str(value) if value != 0 else ' '
                s += f' {value_str:^{value_length}}{' |' if (c + 1) % self.sub_size == 0 else ''}'
            
            s += f'\n{row_border if (r + 1) % self.sub_size == 0 else ""}'  # End of row and add border after subgrid
        
        return s
