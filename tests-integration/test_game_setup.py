# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
import unittest

from click.testing import CliRunner

from toetactic import cli


class TestGameSetupIntegration(unittest.TestCase):

    def test_cli_custom_dimension_and_godzilla(self):
        runner = CliRunner()
        move_stream = "\n".join(
            [
                "A1",
                "A2",
                "A3",
                "A4",
                "B1",
                "B2",
                "B3",
                "B4",
                "C1",
                "C2",
                "C3",
                "C4",
                "D1",
                "D2",
                "D3",
                "D4",
            ]
        )
        result = runner.invoke(
            cli,
            input=f"4\nKai\ngodzilla\n{move_stream}\n",
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Board dimension (3-26) [3]: 4", result.output)
        self.assertIn("Your name [Player]: Kai", result.output)
        self.assertIn("Godzilla plays", result.output)
        self.assertTrue(
            "wins!" in result.output or "Draw game. No moves left." in result.output
        )
