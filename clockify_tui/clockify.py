"""Connect to the Clockify API."""

from clockify_api_client.client import ClockifyAPIClient
from clockify_api_client.models.time_entry import TimeEntry
from clockify_api_client.models.workspace import Workspace

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
    def __init__(self, config: Config) -> None:
        self._client = get_client(config.clockify.api_key)
        self._workspace_id = get_selected_workspace_or_default(
            self._client, config.clockify.workspace_id
        )["id"]
        self._user_id = get_user_id(self._client)
        self._projects = self._get_projects()

    def get_most_recent_time_entry(self) -> TimeEntry | None:
        time_entries = self._client.time_entries.get_time_entries(
            self._workspace_id, self._user_id
        )
        if not time_entries:
            return None

        return time_entries[0]

    def get_project_name(self, project_id: str) -> str:
        return self._projects[project_id]

    def _get_projects(self) -> dict[str, str]:
        return {
            project["id"]: project["name"]
            for project in self._client.projects.get_projects(self._workspace_id)
        }
