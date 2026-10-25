
from storage import load_expenses, save_expenses


def get_expenses():
    """Return all saved expenses."""
    return load_expenses()


def add_expense(amount, category, description, date):
    """Validate and save a new expense."""

    # Validate amount
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a valid number.")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    # Validate text fields
    if not isinstance(category, str) or not category.strip():
        raise ValueError("Category cannot be empty.")

    if not isinstance(description, str) or not description.strip():
        raise ValueError("Description cannot be empty.")

    if not isinstance(date, str) or not date.strip():
        raise ValueError("Date cannot be empty.")

    # Load existing expenses
    expenses = load_expenses()

    # Generate the next ID
    next_id = max(
        (expense.get("id", 0) for expense in expenses),
        default=0
    ) + 1

    # Create the new expense
    expense = {
        "id": next_id,
        "amount": amount,
        "category": category.strip(),
        "description": description.strip(),
        "date": date.strip()
    }

    # Add and save
    expenses.append(expense)
    save_expenses(expenses)

    return expense


def delete_expense(expense_id):
    """Delete an expense using its unique ID."""

    try:
        expense_id = int(expense_id)
    except (TypeError, ValueError):
        raise ValueError("Expense ID must be a valid integer.")

    if expense_id <= 0:
        raise ValueError("Expense ID must be greater than zero.")

    expenses = load_expenses()

    for expense in expenses:
        if expense.get("id") == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)
            return True

    return False

def get_total():
    """Calculate the total amount spent."""
    expenses = load_expenses()
    return sum(expense["amount"] for expense in expenses)


def filter_by_category(category):
    """Return expenses matching the selected category."""

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Category cannot be empty.")

    expenses = load_expenses()
    selected_category = category.strip().casefold()

    return [
        expense
        for expense in expenses
        if expense.get("category", "").strip().casefold()
        == selected_category
    ]

def filter_by_date(date):
    """Return expenses matching the selected date."""

    if not isinstance(date, str) or not date.strip():
        raise ValueError("Date cannot be empty.")

    selected_date = date.strip()

    expenses = load_expenses()

    return [
        expense
        for expense in expenses
        if expense.get("date") == selected_date
    ]

def get_monthly_report(month):
    """Return expenses for a month and totals by category."""

    if not isinstance(month, str) or not month.strip():
        raise ValueError("Month cannot be empty.")

    selected_month = month.strip()

    expenses = load_expenses()

    monthly_expenses = [
        expense
        for expense in expenses
        if expense.get("date", "").startswith(selected_month + "-")
    ]

    category_totals = {}

    for expense in monthly_expenses:
        category = expense["category"]
        amount = float(expense["amount"])

        category_totals[category] = (
            category_totals.get(category, 0) + amount
        )

    total = sum(
        float(expense["amount"])
        for expense in monthly_expenses
    )

    return {
        "month": selected_month,
        "expenses": monthly_expenses,
        "total": total,
        "category_totals": category_totals,
    }
