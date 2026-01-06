"""Connect to the Clockify API."""

from threading import Thread
from time import sleep

from clockify_api_client.client import ClockifyAPIClient
from clockify_api_client.models.time_entry import TimeEntry
from clockify_api_client.models.workspace import Workspace
from pubsub import pub

from clockify_tui.config import Config

API_URL = "api.clockify.me/v1"


def get_client(api_key: str) -> ClockifyAPIClient:
    """Get an API client using the specified API key."""
    return ClockifyAPIClient().build(api_key, API_URL)


def get_selected_workspace_or_default(
    client: ClockifyAPIClient, workspace_id: str
) -> Workspace:
    """Get info about the selected workspace.

    If no workspace is selected, the first one will be used.
    """
    workspaces = client.workspaces.get_workspaces()

    try:
        # If no workspace specified, just use the first one
        if not workspace_id:
            return workspaces[0]

        return next(ws for ws in workspaces if ws["id"] == workspace_id)
    except (IndexError, StopIteration):
        raise RuntimeError("Workspace not found")


def get_user_id(client: ClockifyAPIClient) -> str:
    """Get the ID of the current user."""
    return client.users.get_current_user()["id"]


class ClockifyClient:
    """Manages interaction with Clockify API."""

    def __init__(self, config: Config) -> None:
        """Create a new ClockifyClient."""
        self._client = get_client(config.clockify.api_key)
        self._workspace_id = get_selected_workspace_or_default(
            self._client, config.clockify.workspace_id
        )["id"]
        self._user_id = get_user_id(self._client)
        self._projects = self._get_projects()
        self._update_thread = Thread(
            target=lambda: self._update_time_entry(config.update_interval)
        )
        self._last_time_entry: TimeEntry | None = None
        self._update_thread.start()

    def _update_time_entry(self, update_interval: int) -> None:
        while True:
            time_entries = self._client.time_entries.get_time_entries(
                self._workspace_id, self._user_id
            )
            cur_time_entry = time_entries[0] if time_entries else None
            if cur_time_entry != self._last_time_entry:
                self._last_time_entry = cur_time_entry
                pub.sendMessage(
                    "clockify.time_entry_changed", time_entry=cur_time_entry
                )

            sleep(update_interval)

    def get_most_recent_time_entry(self) -> TimeEntry | None:
        """Get the most recent time entry logged.

        May be running or stopped.
        """
        return self._last_time_entry

    def get_project_name(self, project_id: str) -> str:
        """Get the name of the project corresponding to the given ID."""
        return self._projects[project_id]

    def _get_projects(self) -> dict[str, str]:
        """Get all projects for this client's workspace."""
        out: dict[str, str] = {}
        page = 1
        while True:
            # Load projects, one page at a time
            new = {
                project["id"]: project["name"]
                for project in self._client.projects.get_projects(
                    self._workspace_id, params={"page": page, "page-size": 1000}
                )
            }
            if not new:
                break
            out |= new
            page += 1
        return out
