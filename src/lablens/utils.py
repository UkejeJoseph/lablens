"""Utility functions for Lab Lens."""

import tomllib
from pathlib import Path

import tiktoken

# from lablens.config import get_papers_folder


# def ensure_directories() -> None:
#     """Create necessary directories if they don't exist."""
#     directories = [
#         "data/vector_store",
#         "data/sessions",
#         get_papers_folder(),
#     ]

#     for directory in directories:
#         Path(directory).mkdir(parents=True, exist_ok=True)


def get_project_version() -> str:
    """Get project version from pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    try:
        with open(pyproject_path, "rb") as file:
            pyproject_data = tomllib.load(file)
            return pyproject_data.get("project", {}).get("version", "0.1.0")
    except (FileNotFoundError, tomllib.TOMLDecodeError):
        return "0.1.0"  # Fallback version


def count_tokens(text: str, model: str = "gpt-5") -> int:
    """Count tokens of a text using a given model"""
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))
