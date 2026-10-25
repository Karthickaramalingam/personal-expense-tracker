
import pytest
import budget
import storage
from expenses import add_expense


@pytest.fixture
def test_budget_storage(tmp_path, monkeypatch):
    budget_file = tmp_path / "budgets.json"
    expense_file = tmp_path / "expenses.json"

    monkeypatch.setattr(budget, "BUDGET_FILE", budget_file)
    monkeypatch.setattr(storage, "DATA_FILE", expense_file)


def test_set_monthly_budget(test_budget_storage):
    result = budget.set_monthly_budget("2026-10", 5000)

    assert result == 5000.0
    assert budget.load_budgets()["2026-10"] == 5000.0


def test_reject_zero_budget(test_budget_storage):
    with pytest.raises(ValueError):
        budget.set_monthly_budget("2026-10", 0)


def test_get_budget_status(test_budget_storage):
    budget.set_monthly_budget("2026-10", 5000)

    add_expense(
        1500, "Food & Groceries", "Groceries", "2026-10-10"
    )
    add_expense(
        500, "Travel & Transport", "Bus", "2026-10-12"
    )

    status = budget.get_budget_status("2026-10")

    assert status["budget"] == 5000.0
    assert status["spent"] == 2000.0
    assert status["remaining"] == 3000.0
    assert status["exceeded"] is False


def test_budget_exceeded(test_budget_storage):
    budget.set_monthly_budget("2026-10", 1000)

    add_expense(
        1200, "Shopping", "Shoes", "2026-10-15"
    )

    status = budget.get_budget_status("2026-10")

    assert status["remaining"] == -200.0
    assert status["exceeded"] is True


def test_missing_budget(test_budget_storage):
    with pytest.raises(ValueError):
        budget.get_budget_status("2026-10")
