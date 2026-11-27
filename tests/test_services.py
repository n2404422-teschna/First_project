from app.services import (
    deduplicate_days,
    filter_records,
    get_day_alerts,
    summarize_records,
    validate_day_entry,
)


def test_deduplicate_days_keeps_latest_and_orders_week():
    records = [
        {"day": "Понеділок", "hours_slept": 8, "coffee_cups": 2},
        {"day": "Четвер", "hours_slept": 7, "coffee_cups": 3},
        {"day": "Понеділок", "hours_slept": 6, "coffee_cups": 1},
    ]
    cleaned = deduplicate_days(records)
    assert len(cleaned) == 2
    assert cleaned[0] == {"day": "Понеділок", "hours_slept": 6, "coffee_cups": 1}
    assert cleaned[1] == {"day": "Четвер", "hours_slept": 7, "coffee_cups": 3}


def test_validate_day_entry():
    assert validate_day_entry(7, 2) is None
    assert validate_day_entry(0, 10) is None
    assert validate_day_entry(25, 1) is not None
    assert validate_day_entry(-1, 1) is not None
    assert validate_day_entry(7, -2) is not None


def test_filter_and_summarize_five_days():
    five_days = [
        {"day": "Понеділок", "hours_slept": 8, "coffee_cups": 2},
        {"day": "Вівторок", "hours_slept": 6, "coffee_cups": 4},
        {"day": "Середа", "hours_slept": 2, "coffee_cups": 0},
        {"day": "Четвер", "hours_slept": 7, "coffee_cups": 3},
        {"day": "П'ятниця", "hours_slept": 5, "coffee_cups": 6},
    ]
    summary = summarize_records(five_days)
    assert summary["days_count"] == 5
    assert summary["avg_sleep"] == 5.6
    assert summary["total_coffee"] == 15

    filtered = filter_records(
        five_days,
        selected_days=["Понеділок", "Четвер", "П'ятниця"],
        min_sleep=6,
    )
    assert len(filtered) == 2
    assert [r["day"] for r in filtered] == ["Понеділок", "Четвер"]


def test_get_day_alerts():
    zombie_row = {"day": "Середа", "hours_slept": 2, "coffee_cups": 0}
    zombie_alerts = get_day_alerts(zombie_row)
    assert len(zombie_alerts) == 1
    assert "ЗОМБІ-РЕЖИМ" in zombie_alerts[0]

    low_sleep_row = {"day": "Вівторок", "hours_slept": 2, "coffee_cups": 8}
    low_sleep_alerts = get_day_alerts(low_sleep_row)
    assert len(low_sleep_alerts) == 2

    friday_row = {"day": "П'ятниця", "hours_slept": 5, "coffee_cups": 6}
    friday_alerts = get_day_alerts(friday_row)
    assert len(friday_alerts) == 3