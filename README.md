<!-- BEGIN:AVATAR -->
![Avatar](avatar.jpg)
<!-- END:AVATAR -->

<!-- BEGIN:BADGES -->
[![Build Status](https://github.com/littlegodzillalaboratory/toetactic/workflows/CI/badge.svg)](https://github.com/littlegodzillalaboratory/toetactic/actions?query=workflow%3ACI)
[![Code Scanning Status](https://github.com/littlegodzillalaboratory/toetactic/workflows/CodeQL/badge.svg)](https://github.com/littlegodzillalaboratory/toetactic/actions?query=workflow%3ACodeQL)
[![Dependencies Status](https://img.shields.io/librariesio/release/pypi/toetactic)](https://libraries.io/npm/toetactic)
[![Security Status](https://snyk.io/test/github/littlegodzillalaboratory/toetactic/badge.svg)](https://snyk.io/test/github/littlegodzillalaboratory/toetactic)
[![Published Version](https://img.shields.io/pypi/v/toetactic.svg)](https://pypi.python.org/pypi/toetactic)
<!-- END:BADGES -->

# Toetactic

A terminal Tic Tac Toe game where you can battle five AI opponents:

* Dikembe: purely defensive, focused on blocking your lines.
* Godzilla: aggressive, always looking for direct winning opportunities.
* Noober: picks any legal move at random, hoping for luck.
* Eleanor: builds rows and columns, avoiding diagonals unless it has no other legal move.
* Lisa: uses a trained neural policy published by TicTacToe Models.

![Toetactic Board Screenshot](screenshots/board.png)

## Installation

```shell
pip3 install toetactic
```

## Usage

Run the game:

```shell
toetactic
```

The game will prompt you for:

1. Board dimension (default: 3)
2. Your player name
3. Opponent (`dikembe`, `godzilla`, `noober`, `eleanor`, or `lisa`)

Then enter your moves using chess-like coordinates such as `A1`, `B3`, `C2`.

Show help guide:

```shell
toetactic --help
```

Lisa downloads the model matching the selected board dimension from the
TicTacToe Models 1.0.0 release on her first turn. Models are cached under
`~/.cache/toetactic/models/`. Set `TOETACTIC_MODEL_DIR` to use a different
cache directory or pre-populate models for offline play.

## Colophon

<!-- BEGIN:DEVELOPERS_GUIDE -->
[Developer's Guide](https://littlegodzillalaboratory.github.io/developers-guide-python.html)
<!-- END:DEVELOPERS_GUIDE -->

<!-- BEGIN:BUILD_REPORTS -->
Build reports:

* [Lint report](https://littlegodzillalaboratory.github.io/toetactic/lint/pylint/index.html)
* [Code complexity report](https://littlegodzillalaboratory.github.io/toetactic/complexity/radon/index.html)
* [Unit tests report](https://littlegodzillalaboratory.github.io/toetactic/test/pytest/index.html)
* [Test coverage report](https://littlegodzillalaboratory.github.io/toetactic/coverage/coverage/index.html)
* [Integration tests report](https://littlegodzillalaboratory.github.io/toetactic/test-integration/pytest/index.html)
* [API Documentation](https://littlegodzillalaboratory.github.io/toetactic/doc/sphinx/index.html)

<!-- END:BUILD_REPORTS -->
