import json
import time
from argparse import ArgumentParser
from structure import SudokuGraph, SudokuMatrix
from filler import fill_sudoku
from solver import solve_sudoku


def benchmark(type: str, solver: str, subsize: int, puzzles: str):
    """Benchmark the solving of Sudoku puzzles using the specified solver and representation type.
    Args:
        type: 'graph' or 'matrix' to specify the representation of the Sudoku puzzle.
        solver: 'standard' or 'advanced' to specify the solving strategy.
        subsize: The size of each subgrid in the Sudoku puzzle.
        puzzles: Path to a JSON file containing a list of Sudoku puzzles to solve.
    """
    print(f"Loading puzzles from {puzzles}...")
    with open(puzzles, 'r') as f:
        puzzle_boards = json.load(f)

    sudokus = []
    for board in puzzle_boards:
        if type == 'graph':
            sudoku = SudokuGraph(subsize)
        elif type == 'matrix':
            sudoku = SudokuMatrix(subsize)
        else:
            raise ValueError("Invalid type. Supported types are 'graph' and 'matrix'.")
        fill_sudoku(sudoku, method=1, sudoku_board=board)
        sudokus.append(sudoku)

    print("Starting benchmarking runs...")
    t0 = time.perf_counter()
    for sudoku in sudokus:
        ok = solve_sudoku(sudoku, method=solver)
        assert ok
    print(f"Completed {len(sudokus)} runs on {type} Sudokus with method '{solver}' in {time.perf_counter() - t0:.4f} seconds.")


if __name__ == "__main__":
    parser = ArgumentParser(description="Benchmark Sudoku solvers")
    parser.add_argument("--type", type=str, choices=["graph", "matrix"], default="graph", help="Type of Sudoku representation")
    parser.add_argument("--sub-size", type=int, default=3, help="Size of the Sudoku subgrids")
    parser.add_argument("--solving-method", type=str, default='standard', help="Method to solve the Sudoku puzzle")
    parser.add_argument("--puzzles", type=str, default="sudokus/1000_3x3_07.json", help="Path to JSON file containing Sudoku puzzles")
    args = parser.parse_args()

    benchmark(args.type, args.solving_method, args.sub_size, args.puzzles)