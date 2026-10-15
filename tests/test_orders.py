from datetime import datetime
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_uses_runtime_environment(monkeypatch):
    monkeypatch.setenv("APP_ENVIRONMENT", "test")
    assert client.get("/health").json() == {"status": "ok", "environment": "test"}


def test_create_order_contract():
    response = client.post("/orders", json={"product_code": "DEMO-001", "quantity": 2})
    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"order_id", "product_code", "quantity", "created_at"}
    assert body["product_code"] == "DEMO-001"
    assert body["quantity"] == 2
    assert UUID(body["order_id"])
    assert datetime.fromisoformat(body["created_at"].replace("Z", "+00:00")).utcoffset().total_seconds() == 0
    assert UUID(response.headers["X-Correlation-ID"])
    assert response.headers["Cache-Control"] == "no-store"


@pytest.mark.parametrize("quantity", [0, -1, 101, "2", True, 1.5, None])
def test_invalid_quantities_are_rejected(quantity):
    assert client.post("/orders", json={"product_code": "DEMO-001", "quantity": quantity}).status_code == 422


@pytest.mark.parametrize("code", ["", "lowercase", "A B", "A" * 41])
def test_invalid_product_codes_are_rejected(code):
    assert client.post("/orders", json={"product_code": code, "quantity": 1}).status_code == 422


def test_unexpected_fields_are_rejected():
    assert client.post("/orders", json={"product_code": "A", "quantity": 1, "price": 99}).status_code == 422


def test_each_request_creates_a_distinct_identifier():
    first = client.post("/orders", json={"product_code": "A", "quantity": 1})
    second = client.post("/orders", json={"product_code": "A", "quantity": 1})
    assert first.json()["order_id"] != second.json()["order_id"]
    assert first.headers["X-Correlation-ID"] != second.headers["X-Correlation-ID"]


def test_missing_fields_are_rejected():
    assert client.post("/orders", json={}).status_code == 422
