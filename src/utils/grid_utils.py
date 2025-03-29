def print_grid(grid):
    for row in grid:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def generate_grid():
    # This function can be expanded to generate a valid Sudoku grid
    return [[0 for _ in range(9)] for _ in range(9)]