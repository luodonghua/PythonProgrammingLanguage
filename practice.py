"""Helpers used by the assignment tests.

By default tests import ``starter.py`` (your code). CI sets
``PRACTICE_TARGET=solution`` to check that the published solutions pass.
"""

import importlib.util
import os
from pathlib import Path
from types import ModuleType


def load(test_file: str) -> ModuleType:
    """Load starter.py (or solution.py) from the folder of ``test_file``."""
    folder = Path(test_file).resolve().parent
    target = os.environ.get("PRACTICE_TARGET", "starter")
    path = folder / f"{target}.py"
    spec = importlib.util.spec_from_file_location(f"{folder.name}_{target}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pg_dsn() -> str:
    """Connection string for the practice PostgreSQL server (see compose.yaml)."""
    return os.environ.get(
        "PRACTICE_PG_DSN", "postgresql://postgres:postgres@localhost:5432/postgres"
    )
