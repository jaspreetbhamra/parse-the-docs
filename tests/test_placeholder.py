"""Placeholder tests for initial scaffold."""

from importlib import import_module


def test_package_importable() -> None:
    """Package should be importable after editable install."""

    module = import_module("parse_the_docs")
    assert hasattr(module, "__version__")
