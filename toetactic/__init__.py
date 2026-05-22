"""CLI entrypoint for toetactic."""

import click

from .game import Game


def play_game() -> None:
    """Start an interactive Tic Tac Toe game session."""
    game = Game()
    game.run()


@click.command()
@click.version_option(package_name="toetactic", prog_name="toetactic")
def cli() -> None:
    """Play a Tic Tac Toe game in your terminal."""
    play_game()
