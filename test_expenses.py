
import pytest
import storage

from expenses import add_expense, get_expenses, get_total ,filter_by_category,filter_by_date


@pytest.fixture
def test_storage(tmp_path, monkeypatch):
    """Use a temporary JSON file for each test."""
    test_file = tmp_path / "test_expenses.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)


def test_add_expense(test_storage):
    expense = add_expense(
        150, "Food", "Lunch", "2026-10-18"
    )

    assert expense["id"] == 1
    assert expense["amount"] == 150.0
    assert expense["category"] == "Food"
    assert expense["description"] == "Lunch"

    saved = get_expenses()
    assert len(saved) == 1
    assert saved[0]["amount"] == 150.0


def test_reject_negative_amount(test_storage):
    with pytest.raises(ValueError):
        add_expense(
            -50, "Food", "Lunch", "2026-10-18"
        )

    assert get_expenses() == []


def test_reject_empty_category(test_storage):
    with pytest.raises(ValueError):
        add_expense(
            100, "  ", "Lunch", "2026-10-18"
        )

    assert get_expenses() == []


def test_calculate_total(test_storage):
    add_expense(150, "Food", "Lunch", "2026-10-18")
    add_expense(200, "Travel", "Bus", "2026-10-18")

    assert get_total() == 350.0


def test_empty_expense_list(test_storage):
    assert get_expenses() == []
    assert get_total() == 0



from expenses import delete_expense


def test_delete_expense(test_storage):
    add_expense(150, "Food", "Lunch", "2026-10-18")
    add_expense(200, "Travel", "Bus", "2026-10-18")

    result = delete_expense(1)

    assert result is True
    expenses = get_expenses()
    assert len(expenses) == 1
    assert expenses[0]["id"] == 2
    assert expenses[0]["category"] == "Travel"


def test_delete_missing_expense(test_storage):
    result = delete_expense(999)

    assert result is False
    assert get_expenses() == []


def test_delete_invalid_id(test_storage):
    with pytest.raises(ValueError):
        delete_expense("hello")

    assert get_expenses() == []

def test_filter_by_category(test_storage):
    add_expense(150, "Food & Groceries", "Lunch", "2026-10-19")
    add_expense(200, "Travel & Transport", "Bus", "2026-10-19")
    add_expense(100, "Food & Groceries", "Snacks", "2026-10-19")

    results = filter_by_category("food & groceries")

    assert len(results) == 2
    assert sum(item["amount"] for item in results) == 250.0


def test_filter_by_category_no_matches(test_storage):
    add_expense(150, "Food & Groceries", "Lunch", "2026-10-19")

    assert filter_by_category("Shopping") == []


def test_filter_by_date(test_storage):
    add_expense(150, "Food & Groceries", "Lunch", "2026-10-19")
    add_expense(200, "Travel & Transport", "Bus", "2026-10-20")
    add_expense(100, "Food & Groceries", "Snacks", "2026-10-19")

    results = filter_by_date("2026-10-19")

    assert len(results) == 2
    assert sum(item["amount"] for item in results) == 250.0


def test_filter_by_date_no_matches(test_storage):
    add_expense(150, "Food & Groceries", "Lunch", "2026-10-19")

    assert filter_by_date("2026-10-21") == []
