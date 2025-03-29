# Sudoku Optimizer

This project implements an optimization algorithm for solving Sudoku puzzles. The Sudoku optimizer aims to provide an efficient way to solve Sudoku grids using various optimization techniques.

## Project Structure

```
sudoku-optimizer
├── src
│   ├── __init__.py
│   ├── sudoku_solver.py
│   ├── algorithms
│   │   ├── __init__.py
│   │   └── optimization.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── grid_utils.py
├── tests
│   ├── __init__.py
│   ├── test_sudoku_solver.py
│   └── test_optimization.py
├── requirements.txt
└── README.md
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To solve a Sudoku puzzle, you can use the `SudokuSolver` class from the `sudoku_solver.py` file. Here is a basic example:

```python
from src.sudoku_solver import SudokuSolver

solver = SudokuSolver()
grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

if solver.solve(grid):
    print("Sudoku solved!")
else:
    print("No solution exists.")
```

## Running Tests

To run the tests for the project, use the following command:

```
pytest
```

This will execute all unit tests defined in the `tests` directory.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.