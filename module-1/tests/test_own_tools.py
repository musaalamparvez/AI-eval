"""Tests for the student-added HW1 tools in agent/tools.py."""

from __future__ import annotations

from agent import tools
from agent.auth import AuthContext

SHOPPER_1 = AuthContext(user_id=1, role="shopper")
MERCHANT_9002 = AuthContext(user_id=9002, role="merchant", store_id=2)
SUPPORT = AuthContext(user_id=9501, role="support")


def test_get_store_info_store_override(world: dict) -> None:
    result = tools.get_store_info(SHOPPER_1, "Juniper Home Goods")
    assert result["ok"] is True
    store = result["store"]
    assert store["store_id"] == 2
    assert store["return_window_days"] == 14
    assert store["return_window_source"] == "store_override"
    assert store["platform_default_days"] == 30
    assert store["policy_id"] == "store-juniper-home-goods-policy"


def test_get_store_info_platform_default(world: dict) -> None:
    store = tools.get_store_info(SUPPORT, "blue-heron-ceramics")["store"]
    assert store["store_id"] == 1
    assert store["return_window_days"] == 30
    assert store["return_window_source"] == "platform_default"
    assert store["policy_id"] == "cw-returns"


def test_get_store_info_by_numeric_id(world: dict) -> None:
    assert tools.get_store_info(SUPPORT, "2")["store"]["name"] == "Juniper Home Goods"


def test_get_store_info_merchant_defaults_to_own_store(world: dict) -> None:
    store = tools.get_store_info(MERCHANT_9002)["store"]
    assert store["store_id"] == 2
    assert store["return_window_days"] == 14


def test_get_store_info_errors(world: dict) -> None:
    missing = tools.get_store_info(SHOPPER_1)
    assert missing["ok"] is False and missing["error"] == "invalid_argument"

    unknown = tools.get_store_info(SHOPPER_1, "No Such Store")
    assert unknown["ok"] is False and unknown["error"] == "not_found"


def _juniper_order(world: dict, min_age: int, max_age: int) -> int:
    """A delivered store-2 order delivered between min_age and max_age days ago."""
    import sqlite3

    conn = sqlite3.connect(world["db"])
    try:
        row = conn.execute(
            "SELECT o.id FROM orders o, meta m WHERE m.key = 'world_asof' "
            "AND o.store_id = 2 AND o.status = 'delivered' "
            "AND julianday(m.value) - julianday(o.delivered_at) BETWEEN ? AND ? "
            "ORDER BY o.id LIMIT 1",
            (min_age, max_age),
        ).fetchone()
    finally:
        conn.close()
    assert row, "fixture world has no matching Juniper order"
    return row[0]


def test_check_return_eligibility_within_window(world: dict) -> None:
    result = tools.check_return_eligibility(SHOPPER_1, 4127)
    assert result["ok"] is True
    assert result["eligible"] is True
    assert result["days_since_delivery"] == 12  # delivered 2026-06-19, as of 2026-07-01
    assert result["return_window_days"] == 30
    assert result["days_remaining"] == 18
    assert result["window_source"] == "platform_default"
    assert result["policy_id"] == "cw-returns"


def test_check_return_eligibility_outside_window(world: dict) -> None:
    result = tools.check_return_eligibility(SHOPPER_1, 3980)
    assert result["eligible"] is False
    assert result["days_since_delivery"] == 45  # delivered 2026-05-17
    assert result["days_remaining"] == 0
    assert "ended 15 days ago" in result["reason"]


def test_check_return_eligibility_store_override(world: dict) -> None:
    # 20 days old: inside the 30-day default but outside Juniper's 14-day override.
    order_id = _juniper_order(world, 15, 29)
    result = tools.check_return_eligibility(MERCHANT_9002, order_id)
    assert result["eligible"] is False
    assert result["return_window_days"] == 14
    assert result["window_source"] == "store_override"
    assert result["policy_id"] == "store-juniper-home-goods-policy"

    recent = tools.check_return_eligibility(MERCHANT_9002, _juniper_order(world, 0, 14))
    assert recent["eligible"] is True


def test_check_return_eligibility_not_delivered(world: dict) -> None:
    import sqlite3

    conn = sqlite3.connect(world["db"])
    try:
        order_id = conn.execute("SELECT id FROM orders WHERE status = 'placed' LIMIT 1").fetchone()[0]
    finally:
        conn.close()
    result = tools.check_return_eligibility(SUPPORT, order_id)
    assert result["eligible"] is False
    assert result["days_since_delivery"] is None
    assert "only delivered orders" in result["reason"]


def test_check_return_eligibility_scope_and_missing(world: dict) -> None:
    denied = tools.check_return_eligibility(MERCHANT_9002, 4127)  # store 1's order
    assert denied == {
        "ok": False,
        "error": "permission_denied",
        "reason": "role 'merchant' (user 9002) may not view order #4127",
    }
    assert tools.check_return_eligibility(SHOPPER_1, 999999)["error"] == "not_found"
