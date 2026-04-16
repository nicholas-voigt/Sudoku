# Script to generate a large number of Sudoku puzzles and save them as JSON files for later use in benchmarking.

import json
import argparse
from sudoku import Sudoku

def generate_sudokus(count: int, sub_size: int = 3, difficulty: float = 0.5) -> list[list[list[int | None]]]:
    """Generates a list of Sudoku puzzles using the py-sudoku library."""
    sudokus = []
    for _ in range(count):
        sudoku = Sudoku(sub_size).difficulty(difficulty)
        sudokus.append(sudoku.board)  # Store the board representation for later use
    return sudokus


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Sudoku puzzles and save them to a JSON file.")
    parser.add_argument("--count", type=int, default=100, help="Number of Sudoku puzzles to generate")
    parser.add_argument("--sub-size", type=int, default=3, help="Size of the Sudoku subgrids")
    parser.add_argument("--difficulty", type=float, default=0.5, help="Difficulty level of the puzzles")
    parser.add_argument("--output", type=str, default="sudokus.json", help="Output JSON file name")
    args = parser.parse_args()

    print(f"Generating {args.count} Sudoku puzzles with subgrid size {args.sub_size} and difficulty {args.difficulty}...")
    sudokus = generate_sudokus(args.count, args.sub_size, args.difficulty)

    print(f"Saving generated puzzles to {args.output}...")
    with open(args.output, 'w') as f:
        json.dump(sudokus, f)
