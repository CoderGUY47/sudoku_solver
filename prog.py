import numpy as np

class SudokuSolver:
  """
  An AI-powered Sudoku solver with features for hints, undo/redo, puzzle validation, and manual input interface.
  """

  def __init__(self, puzzle=None):
    # Initialize game board
    if puzzle is None:
      self.puzzle = np.zeros((9, 9), dtype=int)
    else:
      self.puzzle = np.array(puzzle)
    self.original_puzzle = self.puzzle.copy()
    self.history = []
    self.redo_history = []  # Stack for redo moves

  def solve_puzzle(self):
    """
    Uses a simple backtracking algorithm to solve the Sudoku puzzle.
    """
    def is_valid(row, col, num):
      # Check row
      if num in self.puzzle[row]:
        return False
      # Check column
      if num in self.puzzle[:, col]:
        return False
      # Check 3x3 box
      box_row = 3 * (row // 3)
      box_col = 3 * (col // 3)
      if num in self.puzzle[box_row:box_row+3 , box_col:box_col+3]:
        return False
      return True

    def solve(row, col):
      if row == 9:
        return True  # Solved!
      if col == 9:
        return solve(row+1, 0)

      if self.puzzle[row, col] != 0:
        return solve(row, col+1)

      for num in range(1, 10):
        if is_valid(row, col, num):
          self.puzzle[row, col] = num
          self.history.append((row, col, num))
          self.redo_history.clear()  # Clear redo history after each move
          if solve(row, col+1):
            return True
          # Backtrack
          self.puzzle[row, col] = 0
          self.history.pop()

      return False

    solve(0, 0)

  def get_hint(self):
    """
    Provides a hint for the current puzzle by suggesting a number for a specific cell.
    """
    for row in range(9):
      for col in range(9):
        if self.puzzle[row, col] == 0:  # Find an empty cell
          for num in range(1, 10):
            if self.is_valid(row, col, num):
              return (row, col, num)  # Return the first valid number as a hint
    return None  # No hint available

  def undo_move(self):
    """
    Reverts the last move made by the player.
    """
    if self.history:
      row, col, num = self.history.pop()
      self.puzzle[row, col] = 0  # Reset the cell to empty
      self.redo_history.append((row, col, num))  # Add to redo history

  def redo_move(self):
    """
    Re-applies the last undone move.
    """
    if self.redo_history:
      row, col, num = self.redo_history.pop()
      self.puzzle[row, col] = num  # Reapply the number to the cell
      self.history.append((row, col, num))  # Add to history for undoing again

  def validate_puzzle(self):
    """
    Checks if the current puzzle is valid according to Sudoku rules.
    """
    for row in range(9):
      for col in range(9):
        num = self.puzzle[row, col]
        if num != 0 and not self.is_valid(row, col, num):
          return False
    return True

  def manual_input(self, cell, number):
    """
    Allows the player to manually input a number into a specific cell.
    """
    row, col = cell
    if self.is_valid(row, col, number):
      self.puzzle[row, col] = number
      self.history.append((row, col, number))
      self.redo_history.clear()  # Clear redo history after a manual input

  def is_valid(self, row, col, num):
    # Check row
    if num in self.puzzle[row]:
      return False
    # Check column
    if num in self.puzzle[:, col]:
      return False
    # Check 3x3 box
    box_row = 3 * (row // 3)
    box_col = 3 * (col // 3)
    if num in self.puzzle[box_row:box_row+3, box_col:box_col+3]:
      return False
    return True

  def get_input(self):
    """
    Prompts the user for a Sudoku puzzle.
    """
    print("Enter your Sudoku puzzle (0 for empty cells):")
    puzzle = []
    for i in range(9):
      row = list(map(int, input(f"Row {i+1}: ").split()))
      puzzle.append(row)
    return np.array(puzzle)

  def display_puzzle(self):
    """
    Prints the Sudoku puzzle to the console.
    """
    for i in range(9):
      print(" ".join(str(x) for x in self.puzzle[i]))

if __name__ == "__main__":
  solver = SudokuSolver()
  puzzle = solver.get_input()
  solver.puzzle = puzzle
  solver.solve_puzzle()

  print("\nSolved Puzzle:")
  solver.display_puzzle()