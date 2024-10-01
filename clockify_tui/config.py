"""Code for loading and parsing the config file."""

import tomllib
from importlib import resources
from pathlib import Path
from shutil import copyfile

from platformdirs import user_config_path
from pydantic import BaseModel, ConfigDict, field_validator


class Clockify(BaseModel):
    """The clockify section of the configuration file."""

    api_key: str

    @field_validator("api_key")
    @classmethod
    def api_key_must_not_be_empty(cls, v: str) -> str:
        """Ensure that the user has not provided an empty API key."""
        if not v:
            raise ValueError("API key cannot be empty")
        return v


class Config(BaseModel):
    """The program configuration."""

    model_config = ConfigDict(from_attributes=True)
    clockify: Clockify


def _get_config_template_path() -> Path:
    """Get the path to the config template file."""
    return (
        Path(str(resources.files("clockify_tui").joinpath()))
        / "data"
        / "config_template.toml"
    )


def _get_or_create_config_file_path() -> Path:
    """Get the path to the config file, creating it if it doesn't exist.

    The data/config_template.toml file will be used as a template.
    """
    path = user_config_path("clockify-tui", ensure_exists=True) / "config.toml"
    if not path.exists():
        template_path = _get_config_template_path()
        copyfile(template_path, path)
    return path


def read_config() -> Config:
    """Read the program's configuration file from the default location.

    If the file does not exist, a default one will be created.
    """
    with _get_or_create_config_file_path().open("rb") as file:
        config = tomllib.load(file)

    return Config.model_validate(config)
