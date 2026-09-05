"""CLI entrypoint for toetactic."""

import click

from .game import Game


def play_game() -> None:
    """Start an interactive Tic Tac Toe game session.

    Constructs a new :class:`~toetactic.game.Game` and runs it to
    completion, prompting for setup, taking turns, and reporting the
    outcome on the terminal.
    """
    game = Game()
    game.run()


@click.command()
@click.version_option(package_name="toetactic", prog_name="toetactic")
def cli() -> None:
    """Play a Tic Tac Toe game in your terminal."""
    play_game()
