# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code
import unittest

from click.testing import CliRunner

from toetactic import cli


class TestCliIntegration(unittest.TestCase):

    def test_cli_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage: cli [OPTIONS]", result.output)
        self.assertIn("Play a Tic Tac Toe game in your terminal.", result.output)

    def test_cli_with_invalid_arg(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--some-invalid-arg"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Error: No such option: --some-invalid-arg", result.output)

    def test_cli_full_session_draw_or_win(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            input="\nAlice\ndikembe\nA1\nA2\nC2\nB1\nB3\n",
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Board dimension (3-26) [3]:", result.output)
        self.assertIn("Your name [Player]:", result.output)
        self.assertIn("Choose opponent (dikembe/godzilla)", result.output)
        self.assertIn("Toetactic begins!", result.output)
        self.assertTrue(
            "wins!" in result.output or "Draw game. No moves left." in result.output
        )
