"""The main module for Clockify TUI."""

import sys
from importlib.metadata import version

import click

from .ui import UI

__version__ = version(__name__)
from .config import edit_config
from .config import read_config as read_config_file


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
def read_config() -> None:
    """A command to test reading in the config file."""
    # Load the config file which includes the API key. Unused for now.
    read_config_file()
    print("Loaded config successfully")


cli.add_command(cli.command(edit_config))


@cli.command()
def tui() -> None:
    """Launch the TUI."""
    ui = UI()
    ui.run()
