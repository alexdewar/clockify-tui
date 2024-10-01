"""Module for handling workspaces."""

from .config import try_read_config
from .connect import client

config = try_read_config()


def list_workspaces() -> None:
    """Get a list of available workspaces."""
    workspaces = client.workspaces.get_workspaces()
    for workspace in workspaces:
        print(f"{workspace['name']}: {workspace['id']}")


def workspace_info() -> None:
    """Get info about a specific workspace."""
    if config is None:
        raise ValueError("Config file not found.")
    workspace_id = config.clockify.workspace_id
    workspaces = client.workspaces.get_workspaces()
    workspace = next(
        (workspace for workspace in workspaces if workspace["id"] == workspace_id),
        None,
    )

    if workspace:
        for key, value in workspace.items():
            print(f"{key}: {value}")
    else:
        print("Workspace not found.")
