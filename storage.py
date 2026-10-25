
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.json")


def load_expenses():
    """Load expenses from the JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            expenses = json.load(file)

        if not isinstance(expenses, list):
            raise ValueError("Expense data must be a JSON list.")

        return expenses

    except (json.JSONDecodeError, OSError, ValueError) as error:
        raise RuntimeError(
            f"Could not load expenses safely: {error}"
        ) from error


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)

    except OSError as error:
        raise RuntimeError(
            f"Could not save expenses: {error}"
        ) from error
