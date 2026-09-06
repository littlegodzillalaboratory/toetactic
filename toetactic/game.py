"""Game session orchestration for toetactic CLI."""

from __future__ import annotations

import click

from .board import Board
from .player import Dikembe, Eleanor, Godzilla, Noober, Player

#: Map of opponent selection keywords (as entered at the setup prompt) to
#: the :class:`~toetactic.player.Player` subclass that implements them.
OPPONENTS: dict[str, type[Player]] = {
    "dikembe": Dikembe,
    "godzilla": Godzilla,
    "noober": Noober,
    "eleanor": Eleanor,
}


class HumanPlayer(Player):  # pylint: disable=too-few-public-methods
    """Represent the human player."""

    def choose_move(self, board: Board, opponent_mark: str) -> tuple[int, int]:
        """Human move is provided by prompt in Game; this method is not used.

        :param board: Current board state. Unused.
        :param opponent_mark: Mark used by the opposing player. Unused.
        :raises NotImplementedError: Always. Human moves are collected via
            :meth:`Game._prompt_human_move` instead.
        """
        raise NotImplementedError("Human move is collected from CLI prompt")


class Game:  # pylint: disable=too-few-public-methods
    """Represent a single CLI Tic Tac Toe game session.

    :ivar board: Board being played on.
    :vartype board: toetactic.board.Board
    :ivar human: The human player, always marked ``"X"``.
    :vartype human: HumanPlayer
    :ivar opponent: The AI opponent, always marked ``"O"``.
    :vartype opponent: toetactic.player.Player
    """

    def __init__(self) -> None:
        """Initialize game state placeholders.

        Sets up a default 3x3 board with a human player and a Dikembe
        opponent; :meth:`setup` replaces these based on user input before
        :meth:`run` starts the game loop.
        """
        self.board = Board(3)
        self.human = HumanPlayer(name="Player", mark="X")
        self.opponent: Player = Dikembe(name="Dikembe", mark="O")

    def setup(self) -> None:
        """Prompt for board size, player name, and opponent selection.

        Populates :attr:`board`, :attr:`human`, and :attr:`opponent` from
        the collected input, replacing the defaults set in
        :meth:`__init__`.
        """
        dimension = click.prompt(
            "Board dimension (3-26)", default=3, type=click.IntRange(3, 26)
        )
        player_name = click.prompt("Your name", default="Player", type=str).strip()
        opponent_choice = click.prompt(
            f"Choose opponent ({'/'.join(OPPONENTS)})",
            default="dikembe",
            type=click.Choice(list(OPPONENTS), case_sensitive=False),
        )

        self.board = Board(dimension)
        self.human = HumanPlayer(name=player_name or "Player", mark="X")
        opponent_cls = OPPONENTS[opponent_choice.lower()]
        self.opponent = opponent_cls(name=opponent_choice.capitalize(), mark="O")

    def run(self) -> None:
        """Run the game loop until win or draw.

        Calls :meth:`setup` first, then alternates turns between the
        human and the opponent, redrawing the board after every move,
        until a player wins or the board fills up.
        """
        self.setup()

        current: Player = self.human
        status = "Toetactic begins!"
        while True:
            self._render(status)

            if current is self.human:
                row, col = self._prompt_human_move()
            else:
                row, col = current.choose_move(self.board, self.human.mark)
            status = f"{current.name} plays {self.board.move_to_label(row, col)}"

            self.board.place_mark(row, col, current.mark)

            if self.board.has_winner(current.mark):
                self._render(status)
                click.echo(f"{current.name} wins!")
                return

            if self.board.is_full():
                self._render(status)
                click.echo("Draw game. No moves left.")
                return

            current = self.opponent if current is self.human else self.human

    def _render(self, status: str) -> None:
        """Clear the terminal and redraw the board in the same place.

        :param status: Message shown beneath the board, e.g. whose turn
            it is or what move was just played.
        """
        click.clear()
        click.echo("Toetactic")
        click.echo("")
        click.echo(self.board.render())
        click.echo("")
        click.echo(status)

    def _prompt_human_move(self) -> tuple[int, int]:
        """Prompt and validate human move input.

        Re-prompts on invalid or occupied moves until a legal move is
        entered.

        :returns: Zero-based ``(row, col)`` coordinates of the human's
            move.
        """
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
