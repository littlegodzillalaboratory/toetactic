"""Board model and move parsing for toetactic."""

from __future__ import annotations


class Board:
    """Represent an N x N Tic Tac Toe board."""

    def __init__(self, dimension: int = 3) -> None:
        """Initialize an empty board.

        Args:
            dimension: Board size. Must be in range 3-26.

        Raises:
            ValueError: If dimension is out of allowed range.
        """
        if not 3 <= dimension <= 26:
            raise ValueError("Board dimension must be between 3 and 26")
        self.dimension = dimension
        self.cells = [[" " for _ in range(dimension)] for _ in range(dimension)]

    def render(self) -> str:
        """Render the board with chess-like coordinates."""
        header = "   " + " ".join(f"{col:>2}" for col in range(1, self.dimension + 1))
        lines = [header]
        for row_index, row in enumerate(self.cells):
            row_label = chr(ord("A") + row_index)
            row_cells = " ".join(f"{cell:>2}" for cell in row)
            lines.append(f"{row_label} {row_cells}")
        return "\n".join(lines)

    def parse_move(self, move: str) -> tuple[int, int]:
        """Parse a move like 'A1' into (row_index, col_index)."""
        raw_move = move.strip().upper()
        if len(raw_move) < 2:
            raise ValueError("Move must be in the format A1")

        row_char = raw_move[0]
        col_str = raw_move[1:]

        if not row_char.isalpha() or not col_str.isdigit():
            raise ValueError("Move must be in the format A1")

        row = ord(row_char) - ord("A")
        col = int(col_str) - 1
        if row < 0 or row >= self.dimension or col < 0 or col >= self.dimension:
            raise ValueError("Move is out of board range")
        return row, col

    def move_to_label(self, row: int, col: int) -> str:
        """Convert board coordinates to a label like 'A1'."""
        return f"{chr(ord('A') + row)}{col + 1}"

    def is_cell_empty(self, row: int, col: int) -> bool:
        """Return True if a board cell is empty."""
        return self.cells[row][col] == " "

    def place_mark(self, row: int, col: int, mark: str) -> None:
        """Place a mark in a cell.

        Raises:
            ValueError: If the target cell is not empty.
        """
        if not self.is_cell_empty(row, col):
            raise ValueError("Cell is already occupied")
        self.cells[row][col] = mark

    def available_moves(self) -> list[tuple[int, int]]:
        """Return all currently available board coordinates."""
        return [
            (row, col)
            for row in range(self.dimension)
            for col in range(self.dimension)
            if self.is_cell_empty(row, col)
        ]

    def has_winner(self, mark: str) -> bool:
        """Return True when a mark completes a row, column, or diagonal."""
        rows = any(all(cell == mark for cell in row) for row in self.cells)
        cols = any(
            all(self.cells[row][col] == mark for row in range(self.dimension))
            for col in range(self.dimension)
        )
        diag_lr = all(self.cells[i][i] == mark for i in range(self.dimension))
        diag_rl = all(
            self.cells[i][self.dimension - i - 1] == mark for i in range(self.dimension)
        )
        return rows or cols or diag_lr or diag_rl

    def is_full(self) -> bool:
        """Return True when no moves are left."""
        return len(self.available_moves()) == 0
