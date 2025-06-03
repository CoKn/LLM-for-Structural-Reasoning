import random


class SudokuEnvironment:
    def __init__(self, grid=None):
        if grid is None:
            self.grid = [[0 for _ in range(4)] for _ in range(4)]
        else:
            self.grid = [row[:] for row in grid]
        self.solution = None

    def display(self, print_game=True):
        """Display the 4x4 Sudoku grid in a readable format and return the string."""
        lines = []
        lines.append("+-------+-------+")
        for i, row in enumerate(self.grid):
            line = "| "
            for j, cell in enumerate(row):
                line += f"{cell if cell != 0 else '_'} "
                if j == 1:
                    line += "| "
            line += "|"
            lines.append(line)
            if i == 1:
                lines.append("+-------+-------+")
        lines.append("+-------+-------+")

        display_string = "\n".join(lines)
        if print_game:
            print(display_string)
        return display_string

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
        deduction_statement = []
        deduction_evidence = []
        data = []
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
                                if not unique_only or deduction_key not in found_deductions:
                                    if unique_only:
                                        found_deductions.add(deduction_key)

                                    # Generate calculation explanation
                                    calc_explanation = self._get_single_candidate_calculation(row, col, value)
                                    deductions.append(
                                        f"Position ({row},{col}) must be {value} (only valid value {calc_explanation})"
                                    )
                                    deduction_statement.append(f"Position ({row},{col}) must be {value}")
                                    deduction_evidence.append(f"Only valid value{calc_explanation}")
                                    data.append({"row": row,
                                                 "col": col,
                                                 "value": value,
                                                 "full_deduction": f"Position ({row},{col}) must be {value} (only valid value {calc_explanation})",
                                                 "statement": f"Position ({row},{col}) must be {value}",
                                                 "evidence": f"Only valid value{calc_explanation}"
                                                 })

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
                                if not unique_only or deduction_key not in found_deductions:
                                    if unique_only:
                                        found_deductions.add(deduction_key)

                                    # Generate calculation explanation
                                    unit_desc = self._get_unit_description(unit_type, unit_id)
                                    calc_explanation = self._get_hidden_single_calculation(unit_type, unit_id, value)
                                    deductions.append(
                                        f"Position ({r},{c}) must be {value} (only position in {unit_desc} for {value}{calc_explanation})"
                                    )
                                    deduction_statement.append(f"Position ({r},{c}) must be {value}")
                                    deduction_evidence.append(f"Only position in {unit_desc} for {value}{calc_explanation})")
                                    data.append({"row": r,
                                                 "col": c,
                                                 "value": value,
                                                 "full_deduction": f"Position ({r},{c}) must be {value} (only valid value {calc_explanation})",
                                                 "statement": f"Position ({r},{c}) must be {value}",
                                                 "evidence": f"Only valid value{calc_explanation}"
                                                 })

            if apply_changes:
                if iteration_changes:
                    changes_made = True
                else:
                    break
            else:
                break

        return changes_made if apply_changes else deductions, deduction_statement, deduction_evidence, data

    def _get_unit_description(self, unit_type, unit_id):
        """Get human-readable description of a unit."""
        if unit_type == "row":
            return f"row {unit_id}"
        elif unit_type == "column":
            return f"column {unit_id}"
        elif unit_type == "block":
            block_row, block_col = unit_id
            return f"block ({block_row // 2},{block_col // 2})"

    def _get_single_candidate_calculation(self, row, col, value):
        """Generate calculation explanation for single candidate deductions."""
        # Get numbers present in row, column, and block
        row_numbers = set(self.grid[row]) - {0}
        col_numbers = set(self.grid[r][col] for r in range(4)) - {0}

        block_row, block_col = (row // 2) * 2, (col // 2) * 2
        block_numbers = set()
        for r in range(block_row, block_row + 2):
            for c in range(block_col, block_col + 2):
                if self.grid[r][c] != 0:
                    block_numbers.add(self.grid[r][c])

        # Combine all constraints
        all_used = row_numbers | col_numbers | block_numbers
        if all_used:
            used_list = sorted(list(all_used))
            used_sum = sum(used_list)
            calculation = f" because 10 - {' - '.join(map(str, used_list))} = {10 - used_sum}"
        else:
            calculation = ""

        return calculation

    def _get_hidden_single_calculation(self, unit_type, unit_id, value):
        """Generate calculation explanation for hidden single deductions."""
        cells = self.get_unit_cells(unit_type, unit_id)

        # Get numbers already present in the unit
        unit_numbers = set()
        empty_positions = []
        for r, c in cells:
            if self.grid[r][c] != 0:
                unit_numbers.add(self.grid[r][c])
            else:
                empty_positions.append((r, c))

        # Find which empty positions can contain the value
        valid_positions_for_value = []
        blocked_positions = []

        for r, c in empty_positions:
            if value in self.get_valid_numbers(r, c):
                valid_positions_for_value.append((r, c))
            else:
                # Find what's blocking this position for this value
                blocking_constraints = []

                # Check row constraint
                if value in set(self.grid[r]) - {0}:
                    blocking_constraints.append(f"row {r}")

                # Check column constraint
                if value in set(self.grid[row][c] for row in range(4)) - {0}:
                    blocking_constraints.append(f"col {c}")

                # Check block constraint
                block_row, block_col = (r // 2) * 2, (c // 2) * 2
                block_values = set()
                for br in range(block_row, block_row + 2):
                    for bc in range(block_col, block_col + 2):
                        if self.grid[br][bc] != 0:
                            block_values.add(self.grid[br][bc])
                if value in block_values:
                    blocking_constraints.append(f"block ({block_row // 2},{block_col // 2})")

                if blocking_constraints:
                    blocked_positions.append(f"({r},{c}) blocked by {', '.join(blocking_constraints)}")

        # Build explanation
        explanation_parts = []

        # Show what's missing from this unit
        if unit_numbers:
            used_list = sorted(list(unit_numbers))
            missing_numbers = sorted(list(set(range(1, 5)) - unit_numbers))
            explanation_parts.append(f"missing {', '.join(map(str, missing_numbers))} from unit")

        # Show why other positions can't contain this value
        if blocked_positions:
            explanation_parts.append(f"{value} can't go in {'; '.join(blocked_positions)}")

        if explanation_parts:
            return f" because " + "; ".join(explanation_parts)
        else:
            return ""

    def make_deductions(self):
        """Apply logical deductions to fill cells."""
        return self.find_deductions(apply_changes=True)

    def get_explicit_deductions(self, unique_only=True):
        """Get explanations of possible deductions without applying them.

        Args:
            unique_only: If True, return only unique cell assignments.
                        If False, return all reasoning paths.
        """
        return self.find_deductions(apply_changes=False, unique_only=unique_only)

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

    def get_all_units_as_strings(sudoku):
        """
        Get all rows, columns, and squares of the Sudoku grid as strings.
        Empty cells (0s) are represented as '.'

        Args:
            sudoku: A SudokuEnvironment object

        Returns:
            dict: A dictionary with keys 'rows', 'columns', and 'squares',
                  each containing a list of strings representing the units
        """
        grid = sudoku.grid
        result = {'rows': [], 'columns': [], 'squares': []}

        # Get rows as strings
        for row in grid:
            row_str = ' '.join(str(cell) if cell != 0 else '_' for cell in row)
            result['rows'].append(row_str)

        # Get columns as strings
        for col in range(4):
            col_str = ' '.join(str(grid[row][col]) if grid[row][col] != 0 else '_' for row in range(4))
            result['columns'].append(col_str)

        # Get squares (2x2 blocks) as strings
        for block_row in range(0, 4, 2):
            for block_col in range(0, 4, 2):
                square_str = ' '
                for r in range(block_row, block_row + 2):
                    for c in range(block_col, block_col + 2):
                        square_str += str(grid[r][c]) if grid[r][c] != 0 else '_'
                result['squares'].append(square_str)

        return result


if __name__ == "__main__":
    sudoku = SudokuEnvironment()
    if sudoku.create_puzzle(difficulty='easy'):
        sudoku.display()

        print("Logical deductions:")
        deductions = sudoku.get_explicit_deductions(unique_only=True)
        print(len(deductions[0]))
        for d in deductions[-1]:
            print(f"- {d}")

        print(f"\nPuzzle is valid: {sudoku.is_valid()}")
        print(f"Puzzle is complete: {sudoku.is_complete()}")
    else:
        print("Failed to generate puzzle")