"""The main module for Clockify TUI."""

import sys
from importlib.metadata import version

import click

from .ui import UI

__version__ = version(__name__)
from .config import edit_config, try_read_config
from .task import list_tasks
from .workspaces import list_projects, list_workspaces, workspace_info


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
    if try_read_config():
        print("Loaded config successfully")


cli.add_command(cli.command(edit_config))
cli.add_command(cli.command(list_workspaces))
cli.add_command(cli.command(workspace_info))
cli.add_command(cli.command(list_projects))
cli.add_command(cli.command(list_tasks))


@cli.command()
def tui() -> None:
    """Launch the TUI."""
    ui = UI()
    ui.run()
