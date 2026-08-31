"""Shared paths for Tu (2008) sheath analysis scripts."""
from __future__ import annotations

import os


def project_root() -> str:
    """projects/tu2008-sheath"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def repo_root() -> str:
    """Collab repo root (full PFFDtd tree)."""
    env = os.environ.get("PFFDtd_ROOT")
    if env:
        return os.path.abspath(env)
    return os.path.abspath(os.path.join(project_root(), "..", ".."))


def pffdtd_root() -> str:
    return repo_root()


def analysis_dir() -> str:
    return os.path.join(project_root(), "analysis")
