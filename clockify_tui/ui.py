"""The main module for the UI."""

import signal
import sys
from collections.abc import Callable
from threading import Lock

from blessed import Terminal
from clockify_api_client.models.time_entry import TimeEntry
from pubsub import pub

from clockify_tui.clockify import ClockifyClient


class UI:
    """Represents the terminal user interface."""

    def __init__(self, client: ClockifyClient) -> None:
        """Create a new UI."""
        self._client = client
        self._term = Terminal()
        self._keypress_handlers: dict[str, Callable[[], None]] = {}
        self._should_quit = False
        self._time_entry: TimeEntry | None = None
        self._render_lock = Lock()

        # Set up keyboard shortcuts
        self.add_keypress_handler("q", self.quit)

        pub.subscribe(self._update_time_entry, "clockify.time_entry_changed")

    def quit(self) -> None:
        """Quit the program."""
        self._should_quit = True

    def add_keypress_handler(
        self,
        key: str,
        action: Callable[[], None],
    ) -> None:
        """Add a keypress handler to the UI."""
        if not action.__doc__:
            raise ValueError(f"{action.__name__} doesn't have a docstring")

        self._keypress_handlers[key] = action

    def get_keypress_handler(self, key: str) -> None | Callable[[], None]:
        """Get the keypress handler, if any, for the specified key.

        If there is no handler registered, return None.
        """
        return self._keypress_handlers.get(key)

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

    def _update_time_entry(self, time_entry: TimeEntry | None) -> None:
        """Update the currently displayed time entry."""
        self._time_entry = time_entry
        self._render()

    def _render(self) -> None:
        """The main render function."""
        with self._render_lock:
            print(self._term.clear, end="")

            # At bottom of screen
            self._print_keyboard_shortcuts()

            # Reset position to top
            print(self._term.home, end="")

            # Print title at top
            self._print_title()

            self._print_last_entry()

    def _print_title(self) -> None:
        """Print the program's title."""
        txt = "Clockify TUI"
        print(
            f"{self._term.darkolivegreen}{self._term.center(txt)}{self._term.normal}\n"
        )

    def _print_keyboard_shortcuts(self) -> None:
        """Print a list of keyboard shortcuts at the bottom of the screen."""
        print(
            self._term.blue
            + self._term.move_y(self._term.height - len(self._keypress_handlers)),
            end="",
        )
        for key, action in self._keypress_handlers.items():
            print(f"{key}: {action.__doc__}")
        print(self._term.normal)

    def _print_last_entry(self) -> None:
        if not self._time_entry:
            return

        project = self._client.get_project_name(self._time_entry["projectId"])
        status = "Stopped" if self._time_entry["timeInterval"]["end"] else "Running"
        print(f"{project} - {status}")
