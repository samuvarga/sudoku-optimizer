class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid

    def solve(self):
        empty_pos = self.find_empty()
        if not empty_pos:
            return True  # Solved
        row, col = empty_pos

        for num in range(1, 10):
            if self.is_valid(num, row, col):
                self.grid[row][col] = num

                if self.solve():
                    return True

                self.grid[row][col] = 0  # Backtrack

        return False  # Trigger backtracking

    def is_valid(self, num, row, col):
        # Check row
        if num in self.grid[row]:
            return False

        # Check column
        if num in [self.grid[r][col] for r in range(9)]:
            return False

        # Check 3x3 box
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if self.grid[r][c] == num:
                    return False

        return True

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    return (r, c)  # Row, Column
        return None