# 💰 Personal Expense Tracker

A command-line expense management application built with Python to help track daily spending, manage monthly budgets, and organize financial records.

## ✨ Features

- ➕ Add and view expenses
- 🗑️ Delete expenses
- 🔎 Filter expenses by category and date
- 📅 Generate monthly expense reports
- 💵 Set monthly budgets
- 📊 View spending, remaining balance, and budget status
- 📁 Export expenses to CSV
- 💾 Store expenses and budgets in JSON files
- 🧪 Automated tests using pytest

## 🛠️ Technologies Used

- Python
- JSON for data storage
- CSV for exporting records
- pytest for automated testing
- Git and GitHub for version control

## 📂 Project Structure

```text
personal-expense-tracker/
├── main.py
├── expenses.py
├── storage.py
├── budget.py
├── export_csv.py
├── test_expenses.py
├── test_budget.py
├── README.md
└── .gitignore
```

## 🚀 How to Run

1. Install Python.
2. Clone this repository:

   ```bash
   git clone https://github.com/Karthickaramalingam/personal-expense-tracker.git
   ```

3. Open the project folder:

   ```bash
   cd personal-expense-tracker
   ```

4. Start the application:

   ```bash
   python main.py
   ```

## 🧪 Run Tests

Install pytest if needed:

```bash
python -m pip install pytest
```

Run the test suite:

```bash
python -m pytest -v
```

## 🔐 Data Privacy

Expense and budget records are stored locally in JSON files. The `.gitignore` file excludes personal data files and generated CSV exports from Git tracking.

**Important:** Do not upload real financial records or other sensitive information.

## 🎯 Project Goal

This project was developed to practise Python programming, modular application design, file handling, data validation, and automated testing.

## 👩‍💻 Author

**Karthickaramalingam**

- GitHub: [@Karthickaramalingam](https://github.com/Karthickaramalingam)
