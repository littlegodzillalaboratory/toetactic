# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import unittest

from toetactic.board import Board


class TestBoard(unittest.TestCase):

    def test_default_dimension(self):
        board = Board()
        assert board.dimension == 3
        assert len(board.available_moves()) == 9

    def test_invalid_dimension(self):
        with self.assertRaises(ValueError):
            Board(2)

    def test_parse_move(self):
        board = Board(3)
        assert board.parse_move("B3") == (1, 2)

    def test_parse_move_out_of_range(self):
        board = Board(3)
        with self.assertRaises(ValueError):
            board.parse_move("D1")

    def test_parse_move_invalid_short(self):
        board = Board(3)
        with self.assertRaises(ValueError):
            board.parse_move("A")

    def test_parse_move_invalid_pattern(self):
        board = Board(3)
        with self.assertRaises(ValueError):
            board.parse_move("1A")

    def test_parse_move_out_of_range_column(self):
        board = Board(3)
        with self.assertRaises(ValueError):
            board.parse_move("A4")

    def test_move_to_label(self):
        board = Board(3)
        assert board.move_to_label(2, 1) == "C2"

    def test_is_cell_empty_false(self):
        board = Board(3)
        board.place_mark(0, 0, "X")
        assert board.is_cell_empty(0, 0) is False

    def test_available_moves_reduced_after_mark(self):
        board = Board(3)
        board.place_mark(0, 0, "X")
        assert len(board.available_moves()) == 8

    def test_place_mark_on_occupied_cell(self):
        board = Board(3)
        board.place_mark(0, 0, "X")
        with self.assertRaises(ValueError):
            board.place_mark(0, 0, "O")

    def test_has_winner_row(self):
        board = Board(3)
        board.place_mark(0, 0, "X")
        board.place_mark(0, 1, "X")
        board.place_mark(0, 2, "X")
        assert board.has_winner("X") is True

    def test_has_winner_column(self):
        board = Board(3)
        board.place_mark(0, 1, "O")
        board.place_mark(1, 1, "O")
        board.place_mark(2, 1, "O")
        assert board.has_winner("O") is True

    def test_has_winner_diagonal(self):
        board = Board(3)
        board.place_mark(0, 0, "X")
        board.place_mark(1, 1, "X")
        board.place_mark(2, 2, "X")
        assert board.has_winner("X") is True

    def test_has_winner_reverse_diagonal(self):
        board = Board(3)
        board.place_mark(0, 2, "O")
        board.place_mark(1, 1, "O")
        board.place_mark(2, 0, "O")
        assert board.has_winner("O") is True

    def test_has_winner_false(self):
        board = Board(3)
        board.place_mark(0, 0, "X")
        board.place_mark(1, 1, "O")
        assert board.has_winner("X") is False

    def test_is_full(self):
        board = Board(3)
        for row in range(3):
            for col in range(3):
                board.place_mark(row, col, "X")
        assert board.is_full() is True

    def test_render_contains_coordinates(self):
        board = Board(3)
        output = board.render()
        assert "1" in output.splitlines()[0]
        assert "2" in output.splitlines()[0]
        assert "3" in output.splitlines()[0]
        assert "A" in output
        assert "C" in output

    def test_render_contains_grid_lines(self):
        board = Board(3)
        output = board.render()
        assert "+---+---+---+" in output
        assert "|" in output

    def test_render_shows_placed_marks(self):
        board = Board(3)
        board.place_mark(0, 0, "X")
        board.place_mark(1, 1, "O")
        output = board.render()
        assert "| X |" in output
        assert "| O |" in output
