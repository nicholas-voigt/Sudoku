### Script to create sudokus and solve them with the respective algorithms

from argparse import ArgumentParser
from sudoku_graph import SudokuGraph
from matrix import SudokuMatrix
from filler import fill_sudoku
from solver import solve_sudoku


def generate_sudoku(sub_size: int, difficulty: float, type: str) -> SudokuGraph | SudokuMatrix:
    """Generates a Sudoku puzzle with the specified parameters."""
    if type == "graph":
        sudoku = SudokuGraph(sub_size)
    elif type == "matrix":
        sudoku = SudokuMatrix(sub_size)
    else:
        raise ValueError("Invalid type. Supported types are 'graph' and 'matrix'.")

    fill_sudoku(sudoku, method=0, difficulty=difficulty)
    print(f"Generated Sudoku {type} with subgrid size {sub_size} and difficulty {difficulty}:")
    return sudoku


if __name__ == "__main__":
    parser = ArgumentParser(description="Generate & solve a Sudoku puzzle")
    parser.add_argument("--type", type=str, choices=["graph", "matrix"], default="graph", help="Type of Sudoku representation")
    parser.add_argument("--sub-size", type=int, default=3, help="Size of the Sudoku subgrids")
    parser.add_argument("--difficulty", type=float, default=0.7, help="Difficulty level of the puzzle")
    parser.add_argument("--solving-method", type=str, default='standard', help="Method to solve the Sudoku puzzle")
    args = parser.parse_args()

    sudoku = generate_sudoku(args.sub_size, args.difficulty, args.type)
    print(sudoku)

    print("Solving Sudoku...")
    if solve_sudoku(sudoku, method=args.solving_method):
        print("Sudoku solved successfully!")
    else:
        print("Failed to solve the Sudoku.")
    print(sudoku)
