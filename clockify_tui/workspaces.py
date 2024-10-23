"""Module for handling workspaces."""

from .clockify import client
from .config import try_read_config

workspaces = client.workspaces.get_workspaces()


def list_workspaces() -> None:
    """Get a list of available workspaces."""
    for workspace in workspaces:
        print(f"{workspace['name']}: {workspace['id']}")


def workspace_info() -> None:
    """Get info about a specific workspace."""
    config = try_read_config()
    if config is None:
        raise ValueError("Config file not found.")
    workspace_id = config.clockify.workspace_id or workspaces[0]["id"]

    workspace = next(
        (workspace for workspace in workspaces if workspace["id"] == workspace_id),
        None,
    )

    if workspace:
        for key, value in workspace.items():
            print(f"{key}: {value}")
    else:
        print("Workspace not found.")
