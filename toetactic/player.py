"""Players and AI strategies for toetactic."""

from __future__ import annotations

import random
from abc import ABC, abstractmethod

from .board import Board


class Player(ABC):  # pylint: disable=too-few-public-methods
    """Represent a Tic Tac Toe player."""

    def __init__(self, name: str, mark: str) -> None:
        """Initialize player attributes."""
        self.name = name
        self.mark = mark

    @abstractmethod
    def choose_move(self, board: Board, opponent_mark: str) -> tuple[int, int]:
        """Return board coordinates for the next move."""


class Dikembe(Player):  # pylint: disable=too-few-public-methods
    """Defensive opponent that prioritizes preventing player wins."""

    def choose_move(self, board: Board, opponent_mark: str) -> tuple[int, int]:
        """Choose a move by blocking first, then choosing safe central options."""
        block = _find_immediate_line_move(board, opponent_mark)
        if block is not None:
            return block

        center = _center_move(board)
        if center is not None:
            return center

        corner = _corner_move(board)
        if corner is not None:
            return corner

        return board.available_moves()[0]


class Godzilla(Player):  # pylint: disable=too-few-public-methods
    """Attacking opponent that seeks immediate wins each turn."""

    def choose_move(self, board: Board, opponent_mark: str) -> tuple[int, int]:
        """Choose a move by winning first, then taking strong positional moves."""
        winning = _find_immediate_line_move(board, self.mark)
        if winning is not None:
            return winning

        center = _center_move(board)
        if center is not None:
            return center

        corner = _corner_move(board)
        if corner is not None:
            return corner

        return board.available_moves()[0]


class Noober(Player):  # pylint: disable=too-few-public-methods
    """Opponent that picks any legal move at random, hoping for luck."""

    def choose_move(self, board: Board, opponent_mark: str) -> tuple[int, int]:
        """Choose a uniformly random move among all legal moves."""
        return random.choice(board.available_moves())


class Eleanor(Player):  # pylint: disable=too-few-public-methods
    """Opponent that builds rows and columns, avoiding diagonals if possible."""

    def choose_move(self, board: Board, opponent_mark: str) -> tuple[int, int]:
        """Choose a move by favouring row/column lines over diagonals."""
        candidates = _non_diagonal_moves(board)
        if not candidates:
            candidates = board.available_moves()

        winning = _find_immediate_line_move(board, self.mark, candidates)
        if winning is not None:
            return winning

        block = _find_immediate_line_move(board, opponent_mark, candidates)
        if block is not None:
            return block

        return _best_line_building_move(board, self.mark, candidates)


def _find_immediate_line_move(
    board: Board, mark: str, moves: list[tuple[int, int]] | None = None
) -> tuple[int, int] | None:
    """Find a move that creates a winning line for a mark in one turn."""
    for row, col in moves if moves is not None else board.available_moves():
        board.cells[row][col] = mark
        is_winning = board.has_winner(mark)
        board.cells[row][col] = " "
        if is_winning:
            return row, col
    return None


def _non_diagonal_moves(board: Board) -> list[tuple[int, int]]:
    """Return available moves that do not sit on either diagonal."""
    max_index = board.dimension - 1
    return [
        (row, col)
        for row, col in board.available_moves()
        if row != col and row + col != max_index
    ]


def _line_progress(cells: list[str], mark: str) -> int:
    """Count a mark's occupancy of a line, or -1 if the opponent blocks it."""
    if any(cell not in (" ", mark) for cell in cells):
        return -1
    return cells.count(mark)


def _best_line_building_move(
    board: Board, mark: str, moves: list[tuple[int, int]]
) -> tuple[int, int]:
    """Return the move that most advances an open row or column line."""
    best_move = moves[0]
    best_score = -1
    for row, col in moves:
        row_cells = board.cells[row]
        col_cells = [board.cells[r][col] for r in range(board.dimension)]
        score = max(_line_progress(row_cells, mark), _line_progress(col_cells, mark))
        if score > best_score:
            best_score = score
            best_move = (row, col)
    return best_move


def _center_move(board: Board) -> tuple[int, int] | None:
    """Return center move when board dimension is odd and center is empty."""
    if board.dimension % 2 == 0:
        return None
    center = board.dimension // 2
    if board.is_cell_empty(center, center):
        return center, center
    return None


def _corner_move(board: Board) -> tuple[int, int] | None:
    """Return first available corner by deterministic order."""
    max_index = board.dimension - 1
    corners = [(0, 0), (0, max_index), (max_index, 0), (max_index, max_index)]
    for row, col in corners:
        if board.is_cell_empty(row, col):
            return row, col
    return None
