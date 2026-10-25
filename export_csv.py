
import csv
from pathlib import Path

from expenses import get_expenses


def export_expenses_to_csv():
    """Export all expenses to a CSV file."""

    expenses = get_expenses()

    csv_file = Path(__file__).with_name("expenses.csv")

    fieldnames = [
        "id",
        "amount",
        "category",
        "description",
        "date",
    ]

    try:
        with csv_file.open(
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
                extrasaction="ignore",
            )

            writer.writeheader()
            writer.writerows(expenses)

    except OSError as error:
        raise RuntimeError(
            f"Could not export expenses: {error}"
        ) from error

    return csv_file
