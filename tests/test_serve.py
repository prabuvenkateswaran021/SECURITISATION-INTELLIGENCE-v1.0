"""FastAPI service smoke tests."""

from __future__ import annotations

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from matrisk.serve.app import app, _state  # noqa: E402


@pytest.fixture(scope="module")
def client():
    _state.cache_clear()
    return TestClient(app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["loans"] == 500


def test_kpis(client):
    r = client.get("/kpis")
    assert r.status_code == 200
    assert "pool_factor" in r.json()


def test_ecl(client):
    r = client.get("/ecl")
    assert r.status_code == 200
    assert r.json()["total_ecl"] > 0


def test_stress_default(client):
    r = client.get("/stress")
    assert r.status_code == 200
    assert len(r.json()["scenarios"]) == 5


def test_stress_custom(client):
    r = client.get("/stress", params={"pd_mult": 2.0, "lgd_mult": 1.5})
    assert r.status_code == 200
    assert r.json()["custom"]["uplift_vs_base"] > 0
