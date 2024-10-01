"""The main module for Clockify TUI."""

import sys
from importlib.metadata import version

import click

from .ui import UI

__version__ = version(__name__)


def main() -> None:
    """The main entry point to the program."""
    # If the user doesn't supply a command, launch the TUI
    if len(sys.argv) < 2:
        tui()
    else:
        cli()


@click.group()
def cli() -> None:
    """The top-level group containing all the commands for Clockify TUI."""


@cli.command()
def tui() -> None:
    """Launch the TUI."""
    ui = UI()
    ui.run()
