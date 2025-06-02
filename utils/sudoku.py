import random


class SudokuEnvironment:

    def __init__(self, grid=None):
        if grid is None:
            self.grid = [[0 for _ in range(4)] for _ in range(4)]
        else:
            self.grid = [row[:] for row in grid]

        self.solution = None

    def display(self):
        """
        Display the 4x4 Sudoku grid in a readable format.
        Empty cells (0) are displayed as dots.
        """
        # Print the top border
        print("+-------+-------+")
        # Iterate through each row
        for i, row in enumerate(self.grid):
            line = "| "
            for j, cell in enumerate(row):
                if cell == 0:
                    line += ". "
                else:
                    line += f"{cell} "
                if j == 1:
                    line += "| "
            line += "|"
            print(line)
            if i == 1:
                print("+-------+-------+")
        print("+-------+-------+")

    def make_deductions(self):
        """
        Apply logical deduction rules to fill in cells that can be determined without guessing.
        Returns:
            bool: True if any deductions were made, False otherwise
        """
        made_deduction = False

        # Keep making deductions until no more can be made
        while True:
            # Track if we made any deductions in this iteration
            deduction_made = False

            # Try single candidate deductions
            if self._fill_single_candidates():
                deduction_made = True

            # Try hidden singles in rows, columns, and blocks
            if self._fill_hidden_singles():
                deduction_made = True

            # If no deductions were made in this iteration, we're done
            if not deduction_made:
                break

            made_deduction = True

        return made_deduction

    def _fill_single_candidates(self):
        """
        Fill in cells that have only one possible value based on row, column, and block constraints.
        Returns:
            bool: True if any cells were filled, False otherwise
        """
        filled_any = False

        for row in range(4):
            for col in range(4):
                if self.grid[row][col] == 0:  # Empty cell
                    valid_values = self._get_valid_numbers(row, col)
                    if len(valid_values) == 1:
                        self.grid[row][col] = valid_values[0]
                        filled_any = True

        return filled_any

    def _fill_hidden_singles(self):
        """
        Find values that can only go in one position within a row, column, or block.
        Returns:
            bool: True if any cells were filled, False otherwise
        """
        filled_any = False

        # Check rows
        for row in range(4):
            filled_any |= self._check_hidden_singles_in_unit("row", row)

        # Check columns
        for col in range(4):
            filled_any |= self._check_hidden_singles_in_unit("column", col)

        # Check blocks
        for block_row in range(0, 4, 2):
            for block_col in range(0, 4, 2):
                filled_any |= self._check_hidden_singles_in_unit("block", (block_row, block_col))

        return filled_any

    def _check_hidden_singles_in_unit(self, unit_type, unit_id):
        """
        Check for hidden singles in a specific unit (row, column, or block).

        Args:
            unit_type: "row", "column", or "block"
            unit_id: row index, column index, or (block_row, block_col) tuple

        Returns:
            bool: True if any cells were filled, False otherwise
        """
        filled_any = False

        # Get the cells in the unit
        cells = []
        if unit_type == "row":
            cells = [(unit_id, col) for col in range(4)]
        elif unit_type == "column":
            cells = [(row, unit_id) for row in range(4)]
        elif unit_type == "block":
            block_row, block_col = unit_id
            cells = [(r, c) for r in range(block_row, block_row + 2)
                     for c in range(block_col, block_col + 2)]

        # Count possible positions for each value
        for value in range(1, 5):
            positions = []
            for row, col in cells:
                if self.grid[row][col] == 0 and value in self._get_valid_numbers(row, col):
                    positions.append((row, col))

            # If a value can only go in one position, fill it
            if len(positions) == 1:
                row, col = positions[0]
                if self.grid[row][col] == 0:  # Double check it's still empty
                    self.grid[row][col] = value
                    filled_any = True

        return filled_any

    def get_explicit_deductions(self):
        """
        Generate human-readable explanations of possible deductions.
        Returns:
            list: List of string explanations of deductions
        """
        deductions = []

        # Check for single candidates
        for row in range(4):
            for col in range(4):
                if self.grid[row][col] == 0:  # Empty cell
                    valid_values = self._get_valid_numbers(row, col)
                    if len(valid_values) == 1:
                        deductions.append(
                            f"Position ({row},{col}) must be {valid_values[0]} as it's the only valid value.")

        # Check for hidden singles in rows
        for row in range(4):
            for value in range(1, 5):
                valid_positions = []
                for col in range(4):
                    if self.grid[row][col] == 0 and value in self._get_valid_numbers(row, col):
                        valid_positions.append((row, col))
                if len(valid_positions) == 1:
                    r, c = valid_positions[0]
                    deductions.append(
                        f"Position ({r},{c}) must be {value} as it's the only position in row {row} that can contain {value}.")

        # Check for hidden singles in columns
        for col in range(4):
            for value in range(1, 5):
                valid_positions = []
                for row in range(4):
                    if self.grid[row][col] == 0 and value in self._get_valid_numbers(row, col):
                        valid_positions.append((row, col))
                if len(valid_positions) == 1:
                    r, c = valid_positions[0]
                    deductions.append(
                        f"Position ({r},{c}) must be {value} as it's the only position in column {col} that can contain {value}.")

        # Check for hidden singles in blocks
        for block_row in range(0, 4, 2):
            for block_col in range(0, 4, 2):
                for value in range(1, 5):
                    valid_positions = []
                    for r in range(block_row, block_row + 2):
                        for c in range(block_col, block_col + 2):
                            if self.grid[r][c] == 0 and value in self._get_valid_numbers(r, c):
                                valid_positions.append((r, c))
                    if len(valid_positions) == 1:
                        r, c = valid_positions[0]
                        deductions.append(
                            f"Position ({r},{c}) must be {value} as it's the only position in the {block_row // 2},{block_col // 2} block that can contain {value}.")

        return deductions

    def solve(self):
        """
        Solve the Sudoku puzzle using backtracking.
        Returns:
            bool: True if solved successfully, False otherwise
        """
        # Find an empty cell
        empty_cell = self._find_empty_cell()

        # If no empty cell is found, the puzzle is solved
        if empty_cell is None:
            return True

        row, col = empty_cell

        # Try each possible value
        for value in range(1, 5):
            # Check if value is valid for this cell
            if self._is_valid_placement(row, col, value):
                # Place the value
                self.grid[row][col] = value

                # Recursively solve the rest of the puzzle
                if self.solve():
                    return True

                # If placing this value didn't lead to a solution, backtrack
                self.grid[row][col] = 0

        # No valid value was found for this cell
        return False

    def _find_empty_cell(self):
        """
        Find an empty cell (containing 0) in the grid.
        Returns:
            tuple: (row, col) of the empty cell or None if no empty cells
        """
        for row in range(4):
            for col in range(4):
                if self.grid[row][col] == 0:
                    return row, col
        return None

    def _is_valid_placement(self, row, col, value):
        """
        Check if placing a value at the given position is valid.
        Args:
            row: Row index
            col: Column index
            value: Value to place
        Returns:
            bool: True if placement is valid, False otherwise
        """
        # Check row
        for c in range(4):
            if self.grid[row][c] == value:
                return False

        # Check column
        for r in range(4):
            if self.grid[r][col] == value:
                return False

        # Check 2x2 block
        block_row, block_col = (row // 2) * 2, (col // 2) * 2
        for r in range(block_row, block_row + 2):
            for c in range(block_col, block_col + 2):
                if self.grid[r][c] == value:
                    return False

        return True

    def fill_next(self):
        """
        Find a random empty cell and fill it with a random valid number.
        Returns:
            tuple: (success, position, value)
                - success: Boolean indicating whether a cell was filled
                - position: (row, col) of the filled cell or None if no cell was filled
                - value: The value placed in the cell or None if no cell was filled
        """
        # Find all empty cells
        empty_cells = self._find_all_empty_cells()
        if not empty_cells:
            # No empty cells, the grid is full
            return False, None, None

        # Choose a random empty cell
        row, col = random.choice(empty_cells)

        # Get valid numbers for this cell
        valid_numbers = self._get_valid_numbers(row, col)

        if not valid_numbers:
            # No valid numbers for this cell
            return False, (row, col), None

        # Choose a random valid number
        value = random.choice(valid_numbers)

        # Fill the cell
        self.grid[row][col] = value

        return True, (row, col), value

    def _find_all_empty_cells(self):
        """
        Find all empty cells (containing 0) in the grid.
        Returns:
            list: List of (row, col) tuples for all empty cells
        """
        empty_cells = []
        for row in range(4):
            for col in range(4):
                if self.grid[row][col] == 0:
                    empty_cells.append((row, col))
        return empty_cells

    def _get_valid_numbers(self, row, col):
        """
        Get a list of valid numbers for a given cell position.
        Args:
            row: Row index
            col: Column index
        Returns:
            list: List of valid numbers (1-4) for this cell
        """
        # All possible numbers in a 4x4 Sudoku
        valid = set(range(1, 5))

        # Remove numbers already in the row
        for c in range(4):
            if self.grid[row][c] != 0:
                valid.discard(self.grid[row][c])

        # Remove numbers already in the column
        for r in range(4):
            if self.grid[r][col] != 0:
                valid.discard(self.grid[r][col])

        # Remove numbers already in the 2x2 block
        block_row, block_col = (row // 2) * 2, (col // 2) * 2
        for r in range(block_row, block_row + 2):
            for c in range(block_col, block_col + 2):
                if self.grid[r][c] != 0:
                    valid.discard(self.grid[r][c])

        return list(valid)

    def generate_full_solution(self):
        """Generate a completely filled valid Sudoku grid"""
        # Clear the grid first
        self.grid = [[0 for _ in range(4)] for _ in range(4)]

        # Keep filling until the grid is complete
        attempts = 0
        while attempts < 100:  # Prevent infinite loops
            success, _, _ = self.fill_next()
            if not success:
                # If we get stuck, reset and try again
                self.grid = [[0 for _ in range(4)] for _ in range(4)]
                attempts += 1
            elif self._is_grid_full():
                return True

        return False

    def create_puzzle(self, difficulty='medium'):
        """Create a playable puzzle by removing numbers from a full solution"""
        # First generate a full solution
        if not self.generate_full_solution():
            return False

        # Make a copy of the full solution
        self.solution = [row[:] for row in self.grid]

        # Determine how many cells to keep based on difficulty
        cells_to_keep = {
            'easy': 10,
            'medium': 8,
            'hard': 6
        }.get(difficulty, 8)

        # Calculate how many to remove
        cells_to_remove = 16 - cells_to_keep

        # Remove random cells
        removed = 0
        while removed < cells_to_remove:
            row, col = random.randint(0, 3), random.randint(0, 3)
            if self.grid[row][col] != 0:
                self.grid[row][col] = 0
                removed += 1

        return True

    def _is_grid_full(self):
        """Check if the grid is completely filled"""
        for row in self.grid:
            if 0 in row:
                return False
        return True


if __name__ == "__main__":
    sudoku = SudokuEnvironment()
    sudoku.create_puzzle(difficulty='easy')
    sudoku.display()

    # Get and display deductions
    deductions = sudoku.get_explicit_deductions()
    print("\nLogical deductions:")
    for d in deductions:
        print("- " + d)
        sudoku.display()

