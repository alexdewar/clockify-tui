"""Module for handling tasks."""

from clockify_api_client.models.project import Project

from .clockify import get_client
from .config import Config, try_read_config


def get_selected_project_id(config: Config) -> Project | None:
    """Get info about the user's selected project.

    If no project is selected, the first one will be used.
    """
    client = get_client(config.clockify.api_key)
    projects = client.projects.get_projects(config.clockify.workspace_id)

    if not config.clockify.project_id:
        return projects[0]

    try:
        return next(ws for ws in projects if ws["id"] == config.clockify.project_id)
    except StopIteration:
        print("Project not found.")
        return None


def list_tasks() -> None:
    """Get a list of available tasks."""
    config = try_read_config()
    if not config:
        return None

    client = get_client(config.clockify.api_key)
    tasks = client.tasks.get_tasks(
        config.clockify.workspace_id, config.clockify.project_id
    )
    for task in tasks:
        print(f"{task['name']}: {task['id']}")
