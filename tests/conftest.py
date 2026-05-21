"""Shared fixtures: a generated pool in a temp dir, loaded once per session."""

from __future__ import annotations

import pytest

from matrisk.config import load_config
from matrisk.data import generate, loaders


@pytest.fixture(scope="session")
def cfg():
    return load_config()


@pytest.fixture(scope="session")
def raw_dir(tmp_path_factory, cfg):
    d = tmp_path_factory.mktemp("raw")
    generate.write_all(cfg, d)
    return d


@pytest.fixture(scope="session")
def tables(cfg, raw_dir):
    return loaders.load_tables(cfg, raw_dir)


@pytest.fixture(scope="session")
def loans(tables):
    return tables["fact_loan"]
