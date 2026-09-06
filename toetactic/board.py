"""Board model and move parsing for toetactic."""

from __future__ import annotations


class Board:
    """Represent an N x N Tic Tac Toe board.

    :ivar dimension: Number of rows/columns on the board.
    :vartype dimension: int
    :ivar cells: ``dimension`` x ``dimension`` grid of cell marks, where
        each cell holds ``" "`` (empty), ``"X"``, or ``"O"``.
    :vartype cells: list[list[str]]
    """

    def __init__(self, dimension: int = 3) -> None:
        """Initialize an empty board.

        :param dimension: Board size. Must be in range 3-26.
        :raises ValueError: If dimension is out of allowed range.
        """
        if not 3 <= dimension <= 26:
            raise ValueError("Board dimension must be between 3 and 26")
        self.dimension = dimension
        self.cells = [[" " for _ in range(dimension)] for _ in range(dimension)]

    def render(self) -> str:
        """Render the board as a grid with chess-like coordinates.

        :returns: Multi-line string showing column numbers along the top,
            row letters down the left side, and ``+``/``-``/``|`` grid
            lines around each cell.
        """
        cell_width = 3
        label_width = 2
        prefix = " " * (label_width + 1)
        separator = (
            " " * label_width
            + "+"
            + "+".join("-" * cell_width for _ in range(self.dimension))
            + "+"
        )

        header = prefix + " ".join(
            f"{col:^{cell_width}}" for col in range(1, self.dimension + 1)
        )
        lines = [header, separator]
        for row_index, row in enumerate(self.cells):
            row_label = chr(ord("A") + row_index)
            row_cells = "|".join(f"{cell:^{cell_width}}" for cell in row)
            lines.append(f"{row_label:<{label_width}}|{row_cells}|")
            lines.append(separator)
        return "\n".join(lines)

    def parse_move(self, move: str) -> tuple[int, int]:
        """Parse a move like 'A1' into (row_index, col_index).

        :param move: Chess-like move label, e.g. ``"A1"`` or ``"c3"``.
            Leading/trailing whitespace and letter case are ignored.
        :returns: Zero-based ``(row, col)`` coordinates for the move.
        :raises ValueError: If ``move`` is not in the ``<letter><number>``
            format, or if it refers to a cell outside the board.
        """
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
        """Convert board coordinates to a label like 'A1'.

        :param row: Zero-based row index.
        :param col: Zero-based column index.
        :returns: Chess-like move label, e.g. ``"A1"``.
        """
        return f"{chr(ord('A') + row)}{col + 1}"

    def is_cell_empty(self, row: int, col: int) -> bool:
        """Return True if a board cell is empty.

        :param row: Zero-based row index.
        :param col: Zero-based column index.
        :returns: True if the cell holds no mark, False otherwise.
        """
        return self.cells[row][col] == " "

    def place_mark(self, row: int, col: int, mark: str) -> None:
        """Place a mark in a cell.

        :param row: Zero-based row index.
        :param col: Zero-based column index.
        :param mark: Single-character mark to place, e.g. ``"X"`` or
            ``"O"``.
        :raises ValueError: If the target cell is not empty.
        """
        if not self.is_cell_empty(row, col):
            raise ValueError("Cell is already occupied")
        self.cells[row][col] = mark

    def available_moves(self) -> list[tuple[int, int]]:
        """Return all currently available board coordinates.

        :returns: List of zero-based ``(row, col)`` tuples for every empty
            cell, in row-major order.
        """
        return [
            (row, col)
            for row in range(self.dimension)
            for col in range(self.dimension)
            if self.is_cell_empty(row, col)
        ]

    def has_winner(self, mark: str) -> bool:
        """Return True when a mark completes a row, column, or diagonal.

        :param mark: Single-character mark to check for, e.g. ``"X"`` or
            ``"O"``.
        :returns: True if every cell in at least one row, column, or
            diagonal holds ``mark``, False otherwise.
        """
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
        """Return True when no moves are left.

        :returns: True if every cell on the board is occupied, False
            otherwise.
        """
        return len(self.available_moves()) == 0
