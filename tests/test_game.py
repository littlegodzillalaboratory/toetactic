# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from unittest.mock import patch
import unittest

from click.testing import CliRunner

from toetactic import cli


class TestCli(unittest.TestCase):

    def test_cli_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage: cli [OPTIONS]", result.output)
        self.assertIn("Play a Tic Tac Toe game in your terminal.", result.output)

    @patch("toetactic.play_game")
    def test_cli_invokes_game(self, mock_play_game):
        runner = CliRunner()
        result = runner.invoke(cli, [])

        self.assertEqual(result.exit_code, 0)
        mock_play_game.assert_called_once()
