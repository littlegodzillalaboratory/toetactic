"""Game session orchestration for toetactic CLI."""

from __future__ import annotations

import click

from .board import Board
from .player import Dikembe, Godzilla, Player


class HumanPlayer(Player):  # pylint: disable=too-few-public-methods
    """Represent the human player."""

    def choose_move(self, board: Board, opponent_mark: str) -> tuple[int, int]:
        """Human move is provided by prompt in Game; this method is not used."""
        raise NotImplementedError("Human move is collected from CLI prompt")


class Game:  # pylint: disable=too-few-public-methods
    """Represent a single CLI Tic Tac Toe game session."""

    def __init__(self) -> None:
        """Initialize game state placeholders."""
        self.board = Board(3)
        self.human = HumanPlayer(name="Player", mark="X")
        self.opponent: Player = Dikembe(name="Dikembe", mark="O")

    def setup(self) -> None:
        """Prompt for board size, player name, and opponent selection."""
        dimension = click.prompt(
            "Board dimension (3-26)", default=3, type=click.IntRange(3, 26)
        )
        player_name = click.prompt("Your name", default="Player", type=str).strip()
        opponent_choice = click.prompt(
            "Choose opponent (dikembe/godzilla)",
            default="dikembe",
            type=click.Choice(["dikembe", "godzilla"], case_sensitive=False),
        )

        self.board = Board(dimension)
        self.human = HumanPlayer(name=player_name or "Player", mark="X")
        self.opponent = (
            Dikembe(name="Dikembe", mark="O")
            if opponent_choice.lower() == "dikembe"
            else Godzilla(name="Godzilla", mark="O")
        )

    def run(self) -> None:
        """Run the game loop until win or draw."""
        self.setup()
        click.echo("")
        click.echo("Toetactic begins!")

        current: Player = self.human
        while True:
            click.echo("")
            click.echo(self.board.render())

            if current is self.human:
                row, col = self._prompt_human_move()
            else:
                row, col = current.choose_move(self.board, self.human.mark)
                click.echo(f"{current.name} plays {self.board.move_to_label(row, col)}")

            self.board.place_mark(row, col, current.mark)

            if self.board.has_winner(current.mark):
                click.echo("")
                click.echo(self.board.render())
                click.echo(f"{current.name} wins!")
                return

            if self.board.is_full():
                click.echo("")
                click.echo(self.board.render())
                click.echo("Draw game. No moves left.")
                return

            current = self.opponent if current is self.human else self.human

    def _prompt_human_move(self) -> tuple[int, int]:
        """Prompt and validate human move input."""
        while True:
            move = click.prompt(f"{self.human.name}, enter move (e.g. A1)", type=str)
            try:
                row, col = self.board.parse_move(move)
                if not self.board.is_cell_empty(row, col):
                    click.echo("Cell already occupied, choose another move.")
                    continue
                return row, col
            except ValueError as err:
                click.echo(str(err))
