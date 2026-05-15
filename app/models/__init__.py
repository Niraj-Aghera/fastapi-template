"""Model base and loading utilities."""

import importlib
import pkgutil
from collections.abc import Iterable
from pathlib import Path

from app.models.base_model import Base, BigIntMixin, TimestampMixin, UUIDMixin

def _discover_model_module_paths() -> list[str]:
    """Locate ORM model modules under ``app.models`` and return import paths."""
    package_path = Path(__file__).parent
    discovered: list[str] = []
    for module_info in pkgutil.walk_packages([str(package_path)], prefix=f"{__name__}."):
        if module_info.ispkg:
            continue
        module_name = module_info.name
        if module_name.endswith(".base_model") or module_name.endswith(".__init__"):
            continue
        discovered.append(module_name)
    return discovered

def load_all_models(modules: Iterable[str] | None = None) -> None:
    """Import model modules (explicit list or auto-discovered under ``app.models``)."""
    module_paths = list(modules) if modules is not None else _discover_model_module_paths()

    for module_path in module_paths:
        importlib.import_module(module_path)

# Define core exports first
__all__ = [
    "Base",
    "BigIntMixin",
    "TimestampMixin",
    "UUIDMixin",
    "load_all_models",
]