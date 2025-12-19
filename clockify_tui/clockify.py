"""Connect to the Clockify API."""

from clockify_api_client.client import ClockifyAPIClient
from clockify_api_client.models.workspace import Workspace
from clockify_api_client.models.time_entry import TimeEntry

API_URL = "api.clockify.me/v1"


def get_client(api_key: str) -> ClockifyAPIClient:
    """Get an API client using the specified API key."""
    return ClockifyAPIClient().build(api_key, API_URL)


def get_selected_workspace_or_default(
    client: ClockifyAPIClient, workspace_id: str
) -> Workspace | None:
    """Get info about the selected workspace.

    If no workspace is selected, the first one will be used.
    """
    workspaces = client.workspaces.get_workspaces()

    # If no workspace specified, just use the first one
    if not workspace_id:
        # **TODO**: Check there is at least one workspace?
        return workspaces[0]

    try:
        return next(ws for ws in workspaces if ws["id"] == workspace_id)
    except StopIteration:
        print("Workspace not found.")
        return None


def get_user_id(client: ClockifyAPIClient) -> str:
    """Get the ID of the current user."""
    return client.users.get_current_user()["id"]


def get_most_recent_time_entry(
    client: ClockifyAPIClient, workspace_id: str, user_id: str
) -> TimeEntry | None:
    time_entries = client.time_entries.get_time_entries(workspace_id, user_id)
    if not time_entries:
        return None

    return time_entries[0]


class ClockifyClient:
    def __init__(self) -> None:
        pass
