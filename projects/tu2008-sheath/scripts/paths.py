"""Shared paths for Tu (2008) sheath analysis scripts."""
from __future__ import annotations

import os


def project_root() -> str:
    """projects/tu2008-sheath"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def repo_root() -> str:
    """Collab repo root (solver + results/)."""
    return os.path.abspath(os.path.join(project_root(), "..", ".."))


def pffdtd_root() -> str:
    return repo_root()


def results_dir(name: str) -> str:
    """e.g. results_dir('sheath_cw_tu') -> <repo>/results/sheath_cw_tu"""
    return os.path.join(repo_root(), "results", name)


def analysis_dir() -> str:
    return os.path.join(project_root(), "analysis")
