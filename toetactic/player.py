"""Players and AI strategies for toetactic."""

from __future__ import annotations

from abc import ABC, abstractmethod
import os
from pathlib import Path
import random
import shutil
from urllib.error import URLError
from urllib.request import urlopen

from tictactoe_policy import TicTacToePolicy

from .board import Board
from .logger import init

logger = init()

#: Published model release used by Lisa.
MODEL_VERSION = "0.10.0"
#: GitHub release asset URL for a model matching a board dimension.
MODEL_URL = (
    "https://github.com/littlegodzillalaboratory/tictactoe-models/"
    "releases/download/{version}/tictactoe-{size}x{size}-{version}.pt"
)


class Player(ABC):  # pylint: disable=too-few-public-methods
    """Represent a Tic Tac Toe player.

    :ivar name: Display name shown in prompts and status messages.
    :vartype name: str
    :ivar mark: Single-character mark the player places on the board, e.g.
        ``"X"`` or ``"O"``.
    :vartype mark: str
    """

    def __init__(self, name: str, mark: str) -> None:
        """Initialize player attributes.

        :param name: Display name shown in prompts and status messages.
        :param mark: Single-character mark the player places on the
            board.
        """
        self.name = name
        self.mark = mark

    @abstractmethod
    def choose_move(self, board: Board, opponent_mark: str) -> tuple[int, int]:
        """Return board coordinates for the next move.

        :param board: Current board state.
        :param opponent_mark: Mark used by the opposing player.
        :returns: Zero-based ``(row, col)`` coordinates of the chosen
            move.
        """


class Dikembe(Player):  # pylint: disable=too-few-public-methods
    """Defensive opponent that prioritizes preventing player wins."""

    def choose_move(self, board: Board, opponent_mark: str) -> tuple[int, int]:
        """Choose a move by blocking first, then choosing safe central options.

        :param board: Current board state.
        :param opponent_mark: Mark used by the opposing player.
        :returns: Zero-based ``(row, col)`` coordinates of the chosen
            move: a block of the opponent's immediate winning line if one
            exists, otherwise the center, otherwise a corner, otherwise
            the first available cell.
        """
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
        """Choose a move by winning first, then taking strong positional moves.

        :param board: Current board state.
        :param opponent_mark: Mark used by the opposing player.
        :returns: Zero-based ``(row, col)`` coordinates of the chosen
            move: an immediate winning move if one exists, otherwise the
            center, otherwise a corner, otherwise the first available
            cell.
        """
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
        """Choose a uniformly random move among all legal moves.

        :param board: Current board state.
        :param opponent_mark: Mark used by the opposing player. Unused,
            since Noober's choice does not depend on board strategy.
        :returns: Zero-based ``(row, col)`` coordinates of a randomly
            chosen, currently empty cell.
        """
        # Gameplay randomness only, no security or cryptographic use.
        return random.choice(board.available_moves())  # nosec B311


class Eleanor(Player):  # pylint: disable=too-few-public-methods
    """Opponent that builds rows and columns, avoiding diagonals if possible."""

    def choose_move(self, board: Board, opponent_mark: str) -> tuple[int, int]:
        """Choose a move by favouring row/column lines over diagonals.

        Restricts itself to non-diagonal cells whenever any remain: among
        those, it takes an immediate win, then blocks an immediate
        opponent win, then advances whichever open row or column line it
        has already made the most progress on. Diagonal cells are only
        used once no non-diagonal cell is available.

        :param board: Current board state.
        :param opponent_mark: Mark used by the opposing player.
        :returns: Zero-based ``(row, col)`` coordinates of the chosen
            move.
        """
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


class Lisa(Player):  # pylint: disable=too-few-public-methods
    """Neural-policy opponent backed by a published TicTacToe model."""

    def __init__(self, name: str, mark: str) -> None:
        """Initialize a Lisa player with lazy model loading.

        :param name: Display name shown in prompts and status messages.
        :param mark: Single-character mark placed by Lisa.
        """
        super().__init__(name, mark)
        self._policy: TicTacToePolicy | None = None

    def choose_move(self, board: Board, opponent_mark: str) -> tuple[int, int]:
        """Choose the highest-scoring legal move from the matching model.

        The model is downloaded and loaded on Lisa's first turn, then reused
        for the remainder of the game.

        :param board: Current board state.
        :param opponent_mark: Mark used by the opposing player. Unused because
            the policy infers the player to move from the board.
        :returns: Zero-based ``(row, col)`` coordinates of the selected move.
        """
        del opponent_mark
        if self._policy is None:
            self._policy = TicTacToePolicy.load(_get_model(board.dimension))
        values = {"X": 1, "O": -1, " ": 0}
        model_board = [values[cell] for row in board.cells for cell in row]
        return divmod(self._policy.choose_move(model_board), board.dimension)


def _get_model(board_size: int) -> Path:
    """Return a cached model path, downloading the release asset when absent.

    :param board_size: Width and height of the model's board.
    :returns: Local path to the matching published model.
    :raises RuntimeError: If the model cannot be downloaded or cached.
    """
    model_dir = Path(
        os.environ.get(
            "TOETACTIC_MODEL_DIR",
            Path.home() / ".cache" / "toetactic" / "models",
        )
    )
    filename = f"tictactoe-{board_size}x{board_size}-{MODEL_VERSION}.pt"
    model_path = model_dir / filename
    if model_path.is_file():
        return model_path

    model_dir.mkdir(parents=True, exist_ok=True)
    temporary_path = model_path.with_suffix(".pt.tmp")
    model_url = MODEL_URL.format(version=MODEL_VERSION, size=board_size)
    logger.info("Downloading Lisa model from %s", model_url)
    try:
        with urlopen(model_url, timeout=60) as response:  # nosec B310
            with temporary_path.open("wb") as model_file:
                shutil.copyfileobj(response, model_file)
        temporary_path.replace(model_path)
    except (OSError, URLError) as err:
        temporary_path.unlink(missing_ok=True)
        raise RuntimeError(f"Unable to download Lisa model: {model_url}") from err
    return model_path


def _find_immediate_line_move(
    board: Board, mark: str, moves: list[tuple[int, int]] | None = None
) -> tuple[int, int] | None:
    """Find a move that creates a winning line for a mark in one turn.

    :param board: Current board state. Temporarily mutated and restored
        while testing each candidate move.
    :param mark: Single-character mark to test for an immediate win.
    :param moves: Candidate moves to test, in order. Defaults to every
        currently available move on ``board`` when not given.
    :returns: The first candidate move that would complete a row, column,
        or diagonal for ``mark``, or None if no such move exists.
    """
    for row, col in moves if moves is not None else board.available_moves():
        board.cells[row][col] = mark
        is_winning = board.has_winner(mark)
        board.cells[row][col] = " "
        if is_winning:
            return row, col
    return None


def _non_diagonal_moves(board: Board) -> list[tuple[int, int]]:
    """Return available moves that do not sit on either diagonal.

    :param board: Current board state.
    :returns: List of zero-based ``(row, col)`` tuples for empty cells
        that lie on neither the main diagonal nor the anti-diagonal.
    """
    max_index = board.dimension - 1
    return [
        (row, col)
        for row, col in board.available_moves()
        if row != col and row + col != max_index
    ]


def _line_progress(cells: list[str], mark: str) -> int:
    """Count a mark's occupancy of a line, or -1 if the opponent blocks it.

    :param cells: Marks along one row or column, in order.
    :param mark: Single-character mark whose progress is being measured.
    :returns: Number of cells in ``cells`` occupied by ``mark`` when every
        other cell is either empty or also ``mark``; -1 if any cell holds
        a different, opposing mark.
    """
    if any(cell not in (" ", mark) for cell in cells):
        return -1
    return cells.count(mark)


def _best_line_building_move(
    board: Board, mark: str, moves: list[tuple[int, int]]
) -> tuple[int, int]:
    """Return the move that most advances an open row or column line.

    :param board: Current board state.
    :param mark: Single-character mark whose line progress is being
        advanced.
    :param moves: Non-empty list of candidate ``(row, col)`` moves to
        choose from.
    :returns: The candidate move whose row or column has the most
        existing ``mark`` occupancy among lines not already blocked by
        the opponent. Ties keep the earliest candidate in ``moves``.
    """
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
    """Return center move when board dimension is odd and center is empty.

    :param board: Current board state.
    :returns: Zero-based ``(row, col)`` coordinates of the center cell,
        or None if the board has an even dimension (no single center
        cell) or the center is already occupied.
    """
    if board.dimension % 2 == 0:
        return None
    center = board.dimension // 2
    if board.is_cell_empty(center, center):
        return center, center
    return None


def _corner_move(board: Board) -> tuple[int, int] | None:
    """Return first available corner by deterministic order.

    :param board: Current board state.
    :returns: Zero-based ``(row, col)`` coordinates of the first empty
        corner, checked in top-left, top-right, bottom-left, bottom-right
        order, or None if every corner is occupied.
    """
    max_index = board.dimension - 1
    corners = [(0, 0), (0, max_index), (max_index, 0), (max_index, max_index)]
    for row, col in corners:
        if board.is_cell_empty(row, col):
            return row, col
    return None
