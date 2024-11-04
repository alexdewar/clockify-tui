"""Module for handling workspaces."""

from .clockify import get_client, get_selected_workspace_or_default
from .config import try_read_config


def list_workspaces() -> None:
    """Get a list of available workspaces."""
    config = try_read_config()
    if not config:
        return None

    client = get_client(config.clockify.api_key)
    workspaces = client.workspaces.get_workspaces()
    for workspace in workspaces:
        print(f"{workspace['name']}: {workspace['id']}")


def workspace_info() -> None:
    """Get info about a specific workspace."""
    config = try_read_config()
    if not config:
        return
    client = get_client(config.clockify.api_key)

    if workspace := get_selected_workspace_or_default(
        client, config.clockify.workspace_id
    ):
        for key, value in workspace.items():
            print(f"{key}: {value}")


def list_projects() -> None:
    """Get list of projects."""
    config = try_read_config()

    if not config:
        return None

    client = get_client(config.clockify.api_key)
    projects = client.projects.get_projects(config.clockify.workspace_id)
    for project in projects:
        print(f"{project['name']}: {project['id']}")
