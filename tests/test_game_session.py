# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,protected-access

import unittest
from unittest.mock import MagicMock, patch

from toetactic import play_game
from toetactic.board import Board
from toetactic.game import Game, HumanPlayer
from toetactic.player import Dikembe, Eleanor, Godzilla, Noober


class TestGameSetupAndPrompt(unittest.TestCase):

    def test_human_player_choose_move_not_implemented(self):
        player = HumanPlayer("Alice", "X")
        with self.assertRaises(NotImplementedError):
            player.choose_move(Board(3), "O")

    @patch("toetactic.game.click.prompt")
    def test_setup_with_blank_name_uses_default_and_godzilla(self, mock_prompt):
        game = Game()
        mock_prompt.side_effect = [4, "   ", "godzilla"]

        game.setup()

        assert game.board.dimension == 4
        assert game.human.name == "Player"
        assert game.human.mark == "X"
        assert isinstance(game.opponent, Godzilla)

    @patch("toetactic.game.click.prompt")
    def test_setup_with_dikembe_choice(self, mock_prompt):
        game = Game()
        mock_prompt.side_effect = [3, "Kai", "dikembe"]

        game.setup()

        assert game.human.name == "Kai"
        assert isinstance(game.opponent, Dikembe)

    @patch("toetactic.game.click.prompt")
    def test_setup_with_noober_choice(self, mock_prompt):
        game = Game()
        mock_prompt.side_effect = [3, "Kai", "noober"]

        game.setup()

        assert isinstance(game.opponent, Noober)
        assert game.opponent.name == "Noober"

    @patch("toetactic.game.click.prompt")
    def test_setup_with_eleanor_choice(self, mock_prompt):
        game = Game()
        mock_prompt.side_effect = [3, "Kai", "eleanor"]

        game.setup()

        assert isinstance(game.opponent, Eleanor)
        assert game.opponent.name == "Eleanor"

    @patch("toetactic.game.click.echo")
    @patch("toetactic.game.click.prompt")
    def test_prompt_human_move_retries_until_valid(self, mock_prompt, mock_echo):
        game = Game()
        game.board = Board(3)
        game.human = HumanPlayer("Alice", "X")
        game.board.place_mark(0, 0, "O")
        mock_prompt.side_effect = ["Z9", "A1", "B2"]

        move = game._prompt_human_move()

        assert move == (1, 1)
        mock_echo.assert_any_call("Move is out of board range")
        mock_echo.assert_any_call("Cell already occupied, choose another move.")


class TestGameRun(unittest.TestCase):

    @patch.object(Game, "setup")
    @patch("toetactic.game.click.echo")
    def test_run_human_wins(self, mock_echo, mock_setup):
        game = Game()
        game.board = Board(3)
        game.human = HumanPlayer("Alice", "X")
        game.opponent = Dikembe("Dikembe", "O")

        with patch.object(
            game,
            "_prompt_human_move",
            side_effect=[(0, 0), (0, 1), (0, 2)],
        ):
            with patch.object(
                game.opponent, "choose_move", side_effect=[(1, 0), (1, 1)]
            ):
                game.run()

        mock_setup.assert_called_once()
        mock_echo.assert_any_call("Alice wins!")

    @patch.object(Game, "setup")
    @patch("toetactic.game.click.echo")
    def test_run_draw(self, mock_echo, mock_setup):
        game = Game()
        game.board = Board(3)
        game.human = HumanPlayer("Alice", "X")
        game.opponent = Dikembe("Dikembe", "O")

        human_moves = [(0, 0), (0, 2), (1, 0), (2, 1), (2, 2)]
        opponent_moves = [(0, 1), (1, 1), (1, 2), (2, 0)]

        with patch.object(game, "_prompt_human_move", side_effect=human_moves):
            with patch.object(game.opponent, "choose_move", side_effect=opponent_moves):
                game.run()

        mock_setup.assert_called_once()
        mock_echo.assert_any_call("Draw game. No moves left.")

    @patch.object(Game, "setup")
    @patch("toetactic.game.click.echo")
    def test_run_opponent_wins(self, mock_echo, mock_setup):
        game = Game()
        game.board = Board(3)
        game.human = HumanPlayer("Alice", "X")
        game.opponent = Dikembe("Dikembe", "O")

        with patch.object(
            game, "_prompt_human_move", side_effect=[(0, 0), (2, 2), (0, 2)]
        ):
            with patch.object(
                game.opponent, "choose_move", side_effect=[(1, 0), (1, 1), (1, 2)]
            ):
                game.run()

        mock_setup.assert_called_once()
        mock_echo.assert_any_call("Dikembe wins!")

    @patch("toetactic.Game")
    def test_play_game_constructs_and_runs_game(self, mock_game_cls):
        game_instance = MagicMock()
        mock_game_cls.return_value = game_instance

        play_game()

        mock_game_cls.assert_called_once()
        game_instance.run.assert_called_once()
