"""The main module for the UI."""

import signal
import sys
from collections.abc import Callable
from dataclasses import dataclass

from blessed import Terminal


@dataclass
class KeypressHandler:
    """Describes an action that can be invoked via a keypress."""

    description: str
    """A human-readable description of the action."""
    action: Callable[[], None]
    """The function to invoke."""


class UI:
    """Represents the terminal user interface."""

    def __init__(self) -> None:
        """Create a new UI."""
        self._term = Terminal()
        self._keypress_handlers: dict[str, KeypressHandler] = {}
        self._should_quit = False

        # Set up keyboard shortcuts
        self.add_keypress_handler("q", "Quit the program", self.quit)

    def quit(self) -> None:
        """Exit the program."""
        self._should_quit = True

    def add_keypress_handler(
        self,
        key: str,
        description: str,
        action: Callable[[], None],
    ) -> None:
        """Add a keypress handler to the UI."""
        self._keypress_handlers[key] = KeypressHandler(description, action)

    def get_keypress_handler(self, key: str) -> None | Callable[[], None]:
        """Get the keypress handler, if any, for the specified key.

        If there is no handler registered, return None.
        """
        if handler := self._keypress_handlers.get(key):
            return handler.action

        return None

    def run(self) -> None:
        """Run the UI forever."""
        with self._term.fullscreen(), self._term.cbreak(), self._term.hidden_cursor():
            self._render()

            # Re-render on terminal resize (this doesn't work on Windows)
            if sys.platform != "win32":
                signal.signal(
                    signal.SIGWINCH,  # type: ignore[attr-defined]
                    lambda sig, action: self._render(),
                )

            while not self._should_quit:
                key = self._term.inkey()
                if handler := self.get_keypress_handler(key):
                    handler()

    def _render(self) -> None:
        """The main render function."""
        print(self._term.clear, end="")

        # At bottom of screen
        self._print_keyboard_shortcuts()

        # Reset position to top
        print(self._term.home, end="")

        # Print title at top
        self._print_title()

    def _print_title(self) -> None:
        """Print the program's title."""
        txt = "Clockify TUI"
        print(f"{self._term.darkolivegreen}{self._term.center(txt)}{self._term.normal}")

    def _print_keyboard_shortcuts(self) -> None:
        """Print a list of keyboard shortcuts at the bottom of the screen."""
        print(
            self._term.blue
            + self._term.move_y(self._term.height - len(self._keypress_handlers)),
            end="",
        )
        for key, handler in self._keypress_handlers.items():
            print(f"{key}: {handler.description}")
        print(self._term.normal)
