from expenses import add_expense, get_expenses, delete_expense , get_total , filter_by_category,filter_by_date,get_monthly_report
from budget import set_monthly_budget, get_budget_status
from export_csv import export_expenses_to_csv

def show_menu():
    print("\n===== PERSONAL EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. View Total Spending")
    print("4. Delete Expense")
    print("5. Filter by Category")
    print("6. Filter by Date")
    print("7. Monthly Expense Report")
    print("8. Set Monthly Budget")
    print("9. View Budget Status")
    print("10. Export to csv")
    print("11. Exit")

CATEGORIES = [
    "Food & Groceries",
    "Travel & Transport",
    "Shopping",
    "Education & Fees",
    "Recharge & Internet",
    "Bills & Household",
    "Health & Medical",
    "Entertainment & Outings",
    "Personal Care",
    "Family & Gifts",
    "Other",
]


def choose_category():
    while True:
        print("\n===== SELECT CATEGORY =====")

        for number, category in enumerate(CATEGORIES, start=1):
            print(f"{number}. {category}")

        choice = input("Choose category (1-11): ").strip()

        if not choice.isdigit():
            print("Please enter a number from 1 to 11.")
            continue

        number = int(choice)

        if not 1 <= number <= len(CATEGORIES):
            print("Invalid selection. Try again.")
            continue

        category = CATEGORIES[number - 1]

        if category == "Other":
            custom_category = input("Enter your category: ").strip()

            if not custom_category:
                print("Category cannot be empty.")
                continue

            return custom_category

        return category

def handle_add_expense():
    try:
        amount = input("Enter amount: ₹")
        category = choose_category()
        description = input("Enter description: ")
        date = input("Enter date (YYYY-MM-DD): ")

        expense = add_expense(
            amount, category, description, date
        )

        print("\nExpense added successfully!")
        print(f"Expense ID: {expense['id']}")

    except ValueError as error:
        print(f"Invalid input: {error}")

    except RuntimeError as error:
        print(f"Storage error: {error}")


def handle_view_expenses():
    try:
        expenses = get_expenses()

        if not expenses:
            print("\nNo expenses found.")
            return

        print("\n===== YOUR EXPENSES =====")

        for expense in expenses:
            print(
                f"ID: {expense['id']} | "
                f"Date: {expense['date']} | "
                f"Category: {expense['category']} | "
                f"Description: {expense['description']} | "
                f"Amount: ₹{expense['amount']:.2f}"
            )

    except RuntimeError as error:
        print(f"Storage error: {error}")


def handle_delete_expense():
    try:
        expense_id = input("Enter expense ID to delete: ").strip()

        deleted = delete_expense(expense_id)

        if deleted:
            print("Expense deleted successfully!")
        else:
            print("No expense found with that ID.")

    except ValueError as error:
        print(f"Invalid input: {error}")

    except RuntimeError as error:
        print(f"Storage error: {error}")

def handle_total():
    try:
        total = get_total()
        print(f"\nTotal spending: ₹{total:.2f}")

    except RuntimeError as error:
        print(f"Storage error: {error}")

def handle_filter_by_category():
    try:
        category = choose_category()

        matching_expenses = filter_by_category(category)

        if not matching_expenses:
            print(f"\nNo expenses found for {category}.")
            return

        print(f"\n===== EXPENSES: {category} =====")

        for expense in matching_expenses:
            print(
                f"ID: {expense['id']} | "
                f"Date: {expense['date']} | "
                f"Description: {expense['description']} | "
                f"Amount: ₹{expense['amount']:.2f}"
            )

        total = sum(
            expense["amount"]
            for expense in matching_expenses
        )

        print(f"\nCategory total: ₹{total:.2f}")

    except ValueError as error:
        print(f"Invalid input: {error}")

    except RuntimeError as error:
        print(f"Storage error: {error}")

def handle_filter_by_date():
    try:
        selected_date = input(
            "Enter date (YYYY-MM-DD): "
        ).strip()

        matching_expenses = filter_by_date(selected_date)

        if not matching_expenses:
            print(f"\nNo expenses found for {selected_date}.")
            return

        print(f"\n===== EXPENSES ON {selected_date} =====")

        for expense in matching_expenses:
            print(
                f"ID: {expense['id']} | "
                f"Category: {expense['category']} | "
                f"Description: {expense['description']} | "
                f"Amount: ₹{expense['amount']:.2f}"
            )

        total = sum(
            expense["amount"]
            for expense in matching_expenses
        )

        print(f"\nDaily total: ₹{total:.2f}")

    except ValueError as error:
        print(f"Invalid input: {error}")

    except RuntimeError as error:
        print(f"Storage error: {error}")


def handle_monthly_report():
    try:
        month = input(
            "Enter month (YYYY-MM, e.g. 2026-10): "
        ).strip()

        report = get_monthly_report(month)

        if not report["expenses"]:
            print(f"\nNo expenses found for {month}.")
            return

        print(f"\n===== MONTHLY REPORT: {month} =====")

        print("\nCategory-wise Spending:")

        for category, total in report["category_totals"].items():
            print(f"{category}: ₹{total:.2f}")

        print(f"\nTotal Monthly Spending: ₹{report['total']:.2f}")
        print(f"Number of Expenses: {len(report['expenses'])}")

    except ValueError as error:
        print(f"Invalid input: {error}")

    except RuntimeError as error:
        print(f"Storage error: {error}")


def handle_set_monthly_budget():
    try:
        month = input(
            "Enter month (YYYY-MM, e.g. 2026-10): "
        ).strip()

        amount_input = input("Enter your monthly budget (₹): ").strip()
        amount = float(amount_input)

        saved_amount = set_monthly_budget(month, amount)

        print(
            f"\nMonthly budget for {month} "
            f"set to ₹{saved_amount:.2f}"
        )

    except ValueError as error:
        print(f"Invalid input: {error}")

    except RuntimeError as error:
        print(f"Storage error: {error}")

def handle_view_budget_status():
    try:
        month = input(
            "Enter month (YYYY-MM, e.g. 2026-10): "
        ).strip()

        status = get_budget_status(month)

        print(f"\n===== BUDGET STATUS: {status['month']} =====")
        print(f"Monthly Budget: ₹{status['budget']:.2f}")
        print(f"Total Spent: ₹{status['spent']:.2f}")
        print(f"Remaining Balance: ₹{status['remaining']:.2f}")

        if status["exceeded"]:
            print("WARNING: You have exceeded your monthly budget!")
        else:
            print("Good job! You are within your monthly budget.")

        if status["budget"] > 0:
            percentage = (status["spent"] / status["budget"]) * 100
            print(f"Budget Used: {percentage:.1f}%")

    except ValueError as error:
        print(f"Invalid input: {error}")

    except RuntimeError as error:
        print(f"Storage error: {error}")
def handle_export_csv():
    try:
        csv_file = export_expenses_to_csv()
        print(f"\nExpenses exported successfully to: {csv_file}")

    except RuntimeError as error:
        print(f"Export failed: {error}")

def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-11): ").strip()

        if choice == "1":
            handle_add_expense()

        elif choice == "2":
            handle_view_expenses()

        elif choice == "3":
            handle_total()

        elif choice == "4":
            handle_delete_expense()

        elif choice == "5":
            handle_filter_by_category()

        elif choice == "6":
            handle_filter_by_date()

        elif choice == "7":
            handle_monthly_report()
        elif choice == "8":
            handle_set_monthly_budget()
        
        elif choice == "9":    
         handle_view_budget_status()
        
        elif choice == "10":
            handle_export_csv()

        elif choice == "11":
         print("Thank you for using Expense Tracker. Goodbye!")
         break
        
        else:
         print("Invalid choice. Please enter 1-10.")


if __name__ == "__main__":
    main()

