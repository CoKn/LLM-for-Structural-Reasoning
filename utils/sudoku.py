import random


class SudokuEnvironment:
    def __init__(self, grid=None):
        if grid is None:
            self.grid = [[0 for _ in range(4)] for _ in range(4)]
        else:
            self.grid = [row[:] for row in grid]
        self.solution = None

    def display(self):
        """Display the 4x4 Sudoku grid in a readable format."""
        print("+-------+-------+")
        for i, row in enumerate(self.grid):
            line = "| "
            for j, cell in enumerate(row):
                line += f"{cell if cell != 0 else '.'} "
                if j == 1:
                    line += "| "
            line += "|"
            print(line)
            if i == 1:
                print("+-------+-------+")
        print("+-------+-------+")

    def get_valid_numbers(self, row, col):
        """Get valid numbers for a given cell position."""
        if self.grid[row][col] != 0:
            return []

        valid = set(range(1, 5))

        # Remove numbers in row
        valid -= set(self.grid[row])

        # Remove numbers in column
        valid -= set(self.grid[r][col] for r in range(4))

        # Remove numbers in 2x2 block
        block_row, block_col = (row // 2) * 2, (col // 2) * 2
        for r in range(block_row, block_row + 2):
            for c in range(block_col, block_col + 2):
                valid.discard(self.grid[r][c])

        return sorted(list(valid))

    def is_valid_placement(self, row, col, value):
        """Check if placing a value at position is valid."""
        return value in self.get_valid_numbers(row, col)

    def get_empty_cells(self):
        """Get all empty cell positions."""
        return [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]

    def get_unit_cells(self, unit_type, unit_id):
        """Get cells in a unit (row, column, or block)."""
        if unit_type == "row":
            return [(unit_id, c) for c in range(4)]
        elif unit_type == "column":
            return [(r, unit_id) for r in range(4)]
        elif unit_type == "block":
            block_row, block_col = unit_id
            return [(r, c) for r in range(block_row, block_row + 2)
                    for c in range(block_col, block_col + 2)]

    def find_deductions(self, apply_changes=False, unique_only=True):
        """
        Find logical deductions. Can either apply them or just return explanations.

        Args:
            apply_changes: If True, apply deductions to grid. If False, return explanations.
            unique_only: If True, return only unique cell assignments. If False, return all reasoning paths.

        Returns:
            If apply_changes=True: bool indicating if any changes were made
            If apply_changes=False: list of deduction explanations
        """
        deductions = []
        changes_made = False
        found_deductions = set() if unique_only else None  # Track (row, col, value) to avoid duplicates

        while True:
            iteration_changes = False

            # Single candidate deductions
            for row in range(4):
                for col in range(4):
                    if self.grid[row][col] == 0:
                        valid_values = self.get_valid_numbers(row, col)
                        if len(valid_values) == 1:
                            value = valid_values[0]
                            if apply_changes:
                                self.grid[row][col] = value
                                iteration_changes = True
                            else:
                                deduction_key = (row, col, value)
                                if deduction_key not in found_deductions:
                                    found_deductions.add(deduction_key)
                                    deductions.append(
                                        f"Position ({row},{col}) must be {value} "
                                        f"(only valid value)"
                                    )

            # Hidden singles
            units = (
                    [("row", i) for i in range(4)] +
                    [("column", i) for i in range(4)] +
                    [("block", (r, c)) for r in range(0, 4, 2) for c in range(0, 4, 2)]
            )

            for unit_type, unit_id in units:
                cells = self.get_unit_cells(unit_type, unit_id)

                for value in range(1, 5):
                    valid_positions = []
                    for r, c in cells:
                        if self.grid[r][c] == 0 and value in self.get_valid_numbers(r, c):
                            valid_positions.append((r, c))

                    if len(valid_positions) == 1:
                        r, c = valid_positions[0]
                        if self.grid[r][c] == 0:  # Still empty
                            if apply_changes:
                                self.grid[r][c] = value
                                iteration_changes = True
                            else:
                                deduction_key = (r, c, value)
                                if deduction_key not in found_deductions:
                                    found_deductions.add(deduction_key)
                                    unit_desc = self._get_unit_description(unit_type, unit_id)
                                    deductions.append(
                                        f"Position ({r},{c}) must be {value} "
                                        f"(only position in {unit_desc} for {value})"
                                    )

            if apply_changes:
                if iteration_changes:
                    changes_made = True
                else:
                    break
            else:
                break

        return changes_made if apply_changes else deductions

    def _get_unit_description(self, unit_type, unit_id):
        """Get human-readable description of a unit."""
        if unit_type == "row":
            return f"row {unit_id}"
        elif unit_type == "column":
            return f"column {unit_id}"
        elif unit_type == "block":
            block_row, block_col = unit_id
            return f"block ({block_row // 2},{block_col // 2})"

    def make_deductions(self):
        """Apply logical deductions to fill cells."""
        return self.find_deductions(apply_changes=True)

    def get_explicit_deductions(self):
        """Get explanations of possible deductions without applying them."""
        return self.find_deductions(apply_changes=False)

    def solve(self):
        """Solve the puzzle using backtracking."""
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return True

        # Choose cell with minimum remaining values (MRV heuristic)
        row, col = min(empty_cells, key=lambda pos: len(self.get_valid_numbers(*pos)))

        for value in self.get_valid_numbers(row, col):
            self.grid[row][col] = value
            if self.solve():
                return True
            self.grid[row][col] = 0

        return False

    def fill_random_cell(self):
        """Fill a random empty cell with a random valid number."""
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return False, None, None

        row, col = random.choice(empty_cells)
        valid_numbers = self.get_valid_numbers(row, col)

        if not valid_numbers:
            return False, (row, col), None

        value = random.choice(valid_numbers)
        self.grid[row][col] = value
        return True, (row, col), value

    def generate_full_solution(self):
        """Generate a complete valid Sudoku grid."""
        # Use backtracking for more reliable generation
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        return self.solve()

    def create_puzzle(self, difficulty='medium'):
        """Create a puzzle by removing numbers from a complete solution."""
        if not self.generate_full_solution():
            return False

        self.solution = [row[:] for row in self.grid]

        cells_to_keep = {'easy': 10, 'medium': 8, 'hard': 6}.get(difficulty, 8)
        cells_to_remove = 16 - cells_to_keep

        # Get all filled positions and randomly remove
        filled_positions = [(r, c) for r in range(4) for c in range(4)]
        positions_to_remove = random.sample(filled_positions, cells_to_remove)

        for row, col in positions_to_remove:
            self.grid[row][col] = 0

        return True

    def is_complete(self):
        """Check if the grid is completely filled."""
        return all(cell != 0 for row in self.grid for cell in row)

    def is_valid(self):
        """Check if the current grid state is valid."""
        # Check all units for duplicates
        units = (
                [self.grid[i] for i in range(4)] +  # rows
                [[self.grid[r][c] for r in range(4)] for c in range(4)] +  # columns
                [[self.grid[r][c] for r in range(br, br + 2) for c in range(bc, bc + 2)]  # blocks
                 for br in range(0, 4, 2) for bc in range(0, 4, 2)]
        )

        for unit in units:
            non_zero = [x for x in unit if x != 0]
            if len(non_zero) != len(set(non_zero)):
                return False

        return True


if __name__ == "__main__":
    sudoku = SudokuEnvironment()
    if sudoku.create_puzzle(difficulty='easy'):
        sudoku.display()

        print("\nLogical deductions:")
        deductions = sudoku.get_explicit_deductions()
        for d in deductions:
            print(f"- {d}")

        print(f"\nPuzzle is valid: {sudoku.is_valid()}")
        print(f"Puzzle is complete: {sudoku.is_complete()}")
    else:
        print("Failed to generate puzzle")