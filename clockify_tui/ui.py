"""The main module for the UI."""

import signal

from blessed import Terminal


class UI:
    """Represents the terminal user interface."""

    def __init__(self) -> None:
        """Create a new UI."""
        self._term = Terminal()

    def run(self) -> None:
        """Run the UI forever."""
        with self._term.fullscreen(), self._term.cbreak():
            self._render()
            signal.signal(signal.SIGWINCH, lambda sig, action: self._render())

            self._term.inkey()

    def _render(self) -> None:
        print(self._term.home + self._term.clear, end="")

        self._print_title()

        print("Press any key to exit")

    def _print_title(self) -> None:
        txt = "Clockify TUI"
        print(f"{self._term.darkolivegreen}{self._term.center(txt)}{self._term.normal}")
