"""The main module for Clockify TUI."""

from importlib.metadata import version

from .ui import UI

__version__ = version(__name__)


def main() -> None:
    """The main entry point to the program."""
    ui = UI()
    ui.run()
