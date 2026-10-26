
import sqlite3
from datetime import date

DB_NAME = "expenses.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_table():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL
                    CHECK(transaction_type IN ('Income', 'Expense')),
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                description TEXT,
                transaction_date TEXT NOT NULL
            )
        """)


def add_transaction():
    print("\n--- Add Transaction ---")
    transaction_type = input("Type (Income/Expense): ").strip().title()

    if transaction_type not in ("Income", "Expense"):
        print("Please enter Income or Expense.")
        return

    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid amount.")
        return

    category = input("Category: ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    description = input("Description: ").strip()
    transaction_date = input(
        f"Date (YYYY-MM-DD, default {date.today()}): "
    ).strip() or str(date.today())

    try:
        date.fromisoformat(transaction_date)
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    with connect_db() as conn:
        conn.execute("""
            INSERT INTO transactions
            (transaction_type, amount, category, description,
             transaction_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            transaction_type, amount, category,
            description, transaction_date
        ))

    print("Transaction saved successfully!")


def view_transactions():
    with connect_db() as conn:
        rows = conn.execute("""
            SELECT id, transaction_type, amount, category,
                   description, transaction_date
            FROM transactions
            ORDER BY transaction_date DESC, id DESC
        """).fetchall()

    if not rows:
        print("No transactions found.")
        return

    print("\n--- All Transactions ---")
    for row in rows:
        print(
            f"ID: {row[0]} | {row[5]} | {row[1]} | "
            f"{row[2]:.2f} | {row[3]} | {row[4] or '-'}"
        )


def show_summary():
    with connect_db() as conn:
        income = conn.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Income'
        """).fetchone()[0]

        expenses = conn.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Expense'
        """).fetchone()[0]

    print("\n--- Financial Summary ---")
    print(f"Total income:   {income:.2f}")
    print(f"Total expenses: {expenses:.2f}")
    print(f"Balance:        {income - expenses:.2f}")


def monthly_report():
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        date.fromisoformat(month + "-01")
    except ValueError:
        print("Invalid month. Use YYYY-MM.")
        return

    with connect_db() as conn:
        rows = conn.execute("""
            SELECT transaction_type, SUM(amount)
            FROM transactions
            WHERE transaction_date LIKE ?
            GROUP BY transaction_type
        """, (month + "-%",)).fetchall()

    totals = {"Income": 0.0, "Expense": 0.0}
    for transaction_type, amount in rows:
        totals[transaction_type] = amount

    print(f"\n--- Report for {month} ---")
    print(f"Income:   {totals['Income']:.2f}")
    print(f"Expenses: {totals['Expense']:.2f}")
    print(
        f"Balance:  "
        f"{totals['Income'] - totals['Expense']:.2f}"
    )


def main():
    create_table()

    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add transaction")
        print("2. View transactions")
        print("3. Financial summary")
        print("4. Monthly report")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            monthly_report()
        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Enter 1-5.")


if __name__ == "__main__":
    main()
