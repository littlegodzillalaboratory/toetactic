# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import unittest
from unittest.mock import patch

from toetactic.board import Board
from toetactic.player import (
    Dikembe,
    Eleanor,
    Godzilla,
    Noober,
    _best_line_building_move,
    _center_move,
    _corner_move,
    _find_immediate_line_move,
    _non_diagonal_moves,
)


class TestPlayerHelpers(unittest.TestCase):

    def test_find_immediate_line_move_returns_none(self):
        board = Board(3)
        board.place_mark(0, 0, "X")
        assert _find_immediate_line_move(board, "X") is None

    def test_center_move_on_even_board_returns_none(self):
        board = Board(4)
        assert _center_move(board) is None

    def test_center_move_on_occupied_center_returns_none(self):
        board = Board(3)
        board.place_mark(1, 1, "X")
        assert _center_move(board) is None

    def test_corner_move_none_when_all_corners_taken(self):
        board = Board(3)
        for row, col in ((0, 0), (0, 2), (2, 0), (2, 2)):
            board.place_mark(row, col, "X")
        assert _corner_move(board) is None

    def test_non_diagonal_moves_excludes_both_diagonals(self):
        board = Board(3)
        moves = _non_diagonal_moves(board)
        assert moves == [(0, 1), (1, 0), (1, 2), (2, 1)]

    def test_best_line_building_move_prefers_open_line_progress(self):
        board = Board(3)
        board.place_mark(0, 0, "O")
        moves = [(0, 1), (2, 1)]
        assert _best_line_building_move(board, "O", moves) == (0, 1)

    def test_best_line_building_move_skips_blocked_lines(self):
        board = Board(3)
        board.place_mark(0, 0, "O")
        board.place_mark(0, 1, "X")
        moves = [(0, 2), (2, 1)]
        assert _best_line_building_move(board, "O", moves) == (0, 2)


class TestPlayers(unittest.TestCase):

    def test_dikembe_blocks_immediate_threat(self):
        board = Board(3)
        board.place_mark(0, 0, "X")
        board.place_mark(0, 1, "X")

        dikembe = Dikembe("Dikembe", "O")
        move = dikembe.choose_move(board, opponent_mark="X")
        assert move == (0, 2)

    def test_dikembe_takes_center_when_no_threat(self):
        board = Board(3)
        dikembe = Dikembe("Dikembe", "O")
        assert dikembe.choose_move(board, opponent_mark="X") == (1, 1)

    def test_dikembe_takes_corner_when_center_occupied(self):
        board = Board(3)
        board.place_mark(1, 1, "X")
        dikembe = Dikembe("Dikembe", "O")
        assert dikembe.choose_move(board, opponent_mark="X") == (0, 0)

    def test_dikembe_falls_back_to_first_available(self):
        board = Board(4)
        for row, col in ((0, 0), (0, 3), (3, 0), (3, 3)):
            board.place_mark(row, col, "X")
        dikembe = Dikembe("Dikembe", "O")
        assert dikembe.choose_move(board, opponent_mark="X") == (0, 1)

    def test_godzilla_takes_winning_move(self):
        board = Board(3)
        board.place_mark(1, 0, "O")
        board.place_mark(1, 1, "O")

        godzilla = Godzilla("Godzilla", "O")
        move = godzilla.choose_move(board, opponent_mark="X")
        assert move == (1, 2)

    def test_godzilla_takes_center_when_no_win(self):
        board = Board(3)
        godzilla = Godzilla("Godzilla", "O")
        assert godzilla.choose_move(board, opponent_mark="X") == (1, 1)

    def test_godzilla_takes_corner_when_center_occupied(self):
        board = Board(3)
        board.place_mark(1, 1, "X")
        godzilla = Godzilla("Godzilla", "O")
        assert godzilla.choose_move(board, opponent_mark="X") == (0, 0)

    def test_godzilla_falls_back_to_first_available(self):
        board = Board(4)
        for row, col in ((0, 0), (0, 3), (3, 0), (3, 3)):
            board.place_mark(row, col, "X")
        godzilla = Godzilla("Godzilla", "O")
        assert godzilla.choose_move(board, opponent_mark="X") == (0, 1)

    def test_noober_picks_a_legal_move(self):
        board = Board(3)
        board.place_mark(0, 0, "X")
        noober = Noober("Noober", "O")
        move = noober.choose_move(board, opponent_mark="X")
        assert move in board.available_moves()

    @patch("toetactic.player.random.choice")
    def test_noober_delegates_to_random_choice(self, mock_choice):
        board = Board(3)
        mock_choice.return_value = (1, 1)
        noober = Noober("Noober", "O")
        move = noober.choose_move(board, opponent_mark="X")
        assert move == (1, 1)
        mock_choice.assert_called_once_with(board.available_moves())

    def test_eleanor_avoids_diagonal_when_alternative_exists(self):
        board = Board(3)
        eleanor = Eleanor("Eleanor", "O")
        row, col = eleanor.choose_move(board, opponent_mark="X")
        assert row != col
        assert row + col != board.dimension - 1

    def test_eleanor_takes_winning_row_move(self):
        board = Board(3)
        board.place_mark(2, 0, "O")
        board.place_mark(2, 2, "O")
        eleanor = Eleanor("Eleanor", "O")
        move = eleanor.choose_move(board, opponent_mark="X")
        assert move == (2, 1)

    def test_eleanor_blocks_opponent_line(self):
        board = Board(3)
        board.place_mark(0, 0, "X")
        board.place_mark(0, 2, "X")
        eleanor = Eleanor("Eleanor", "O")
        move = eleanor.choose_move(board, opponent_mark="X")
        assert move == (0, 1)

    def test_eleanor_uses_diagonal_when_no_other_move_available(self):
        board = Board(3)
        for row, col in ((0, 1), (1, 0), (1, 2), (2, 1)):
            board.place_mark(row, col, "X")
        eleanor = Eleanor("Eleanor", "O")
        row, col = eleanor.choose_move(board, opponent_mark="X")
        assert row == col or row + col == board.dimension - 1
