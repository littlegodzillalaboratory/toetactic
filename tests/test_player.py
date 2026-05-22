# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import unittest

from toetactic.board import Board
from toetactic.player import (
    Dikembe,
    Godzilla,
    _center_move,
    _corner_move,
    _find_immediate_line_move,
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
