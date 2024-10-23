"""Module for handling workspaces."""

from clockify_api_client.models.workspace import Workspace

from .clockify import get_client
from .config import Config, try_read_config


def list_workspaces() -> None:
    """Get a list of available workspaces."""
    config = try_read_config()
    if not config:
        return None

    client = get_client(config.clockify.api_key)
    workspaces = client.workspaces.get_workspaces()
    for workspace in workspaces:
        print(f"{workspace['name']}: {workspace['id']}")


def get_selected_workspace(config: Config) -> Workspace | None:
    """Get info about the user's selected workspace.

    If no workspace is selected, the first one will be used.
    """
    client = get_client(config.clockify.api_key)
    workspaces = client.workspaces.get_workspaces()

    # If no workspace specified, just use the first one
    if not config.clockify.workspace_id:
        # **TODO**: Check there is at least one workspace?
        return workspaces[0]

    try:
        return next(ws for ws in workspaces if ws["id"] == config.clockify.workspace_id)
    except StopIteration:
        print("Workspace not found.")
        return None


def workspace_info() -> None:
    """Get info about a specific workspace."""
    config = try_read_config()
    if not config:
        return

    if workspace := get_selected_workspace(config):
        for key, value in workspace.items():
            print(f"{key}: {value}")
