
import json
from pathlib import Path

BUDGET_FILE = Path(__file__).with_name("budgets.json")


def load_budgets():
    """Load saved monthly budgets."""

    if not BUDGET_FILE.exists():
        return {}

    try:
        with BUDGET_FILE.open("r", encoding="utf-8") as file:
            budgets = json.load(file)

        if not isinstance(budgets, dict):
            raise ValueError("Budget data must be a JSON object.")

        return budgets

    except (json.JSONDecodeError, OSError, ValueError) as error:
        raise RuntimeError(
            f"Could not load budgets safely: {error}"
        ) from error


def save_budgets(budgets):
    """Save monthly budgets."""

    try:
        with BUDGET_FILE.open("w", encoding="utf-8") as file:
            json.dump(budgets, file, indent=4)

    except OSError as error:
        raise RuntimeError(
            f"Could not save budgets: {error}"
        ) from error

def set_monthly_budget(month, amount):
    """Set or update a budget for a specific month."""

    if not isinstance(month, str):
        raise ValueError("Month must be in YYYY-MM format.")

    month = month.strip()

    try:
        from datetime import datetime
        datetime.strptime(month, "%Y-%m")
    except ValueError as error:
        raise ValueError(
            "Invalid month. Use YYYY-MM format, such as 2026-10."
        ) from error

    try:
        amount = float(amount)
    except (TypeError, ValueError) as error:
        raise ValueError("Budget must be a valid number.") from error

    if amount <= 0:
        raise ValueError("Budget must be greater than zero.")

    budgets = load_budgets()
    budgets[month] = amount
    save_budgets(budgets)

    return amount
set_monthly_budget("2026-10", 5000)



from expenses import get_monthly_report


def get_budget_status(month):
    """Calculate budget, spending, and remaining balance."""

    budgets = load_budgets()

    if month not in budgets:
        raise ValueError(f"No budget set for {month}.")

    budget = budgets[month]
    report = get_monthly_report(month)
    spent = report["total"]
    remaining = budget - spent

    return {
        "month": month,
        "budget": budget,
        "spent": spent,
        "remaining": remaining,
        "exceeded": spent > budget,
    }
