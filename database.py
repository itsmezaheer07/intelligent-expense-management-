"""
Database Module for Intelligent Expense Management System
Author: Zaheer Ansari (GUI Developer, BTech 1st Year AI & Data Science)
Description: Robust SQLite interface handling data persistence, schema management,
             CRUD operations, aggregations, and sample data seeding.
"""

import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Tuple

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "expense_database.db")

DEFAULT_CATEGORIES = [
    "Food",
    "Education",
    "Transport",
    "Shopping",
    "Entertainment",
    "Healthcare",
    "Bills",
    "Other"
]

@contextmanager
def get_db():
    """
    Context manager that yields an active SQLite connection with row factory
    and guarantees proper closing and transaction handling.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db(seed_if_empty: bool = True) -> None:
    """
    Initializes database tables and seeds sample data if database is empty.
    Preserves all existing data if already populated.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                payment_method TEXT DEFAULT 'UPI',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                icon TEXT,
                color TEXT
            )
        """)
        
        # App Settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        
        # Seed default categories if missing
        category_metadata = [
            ("Food", "🍔", "#F97316"),
            ("Education", "🎓", "#3B82F6"),
            ("Transport", "🚗", "#06B6D4"),
            ("Shopping", "🛍️", "#EC4899"),
            ("Entertainment", "🎬", "#8B5CF6"),
            ("Healthcare", "🏥", "#EF4444"),
            ("Bills", "💡", "#EAB308"),
            ("Other", "📦", "#6B7280"),
        ]
        for name, icon, color in category_metadata:
            cursor.execute("""
                INSERT OR IGNORE INTO categories (name, icon, color)
                VALUES (?, ?, ?)
            """, (name, icon, color))
            
        # Default settings
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('currency', '₹')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('theme', 'light')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('monthly_budget', '35000')")
        
        conn.commit()

        # Check if expenses table is empty; if so, optionally seed realistic sample records
        cursor.execute("SELECT COUNT(*) as count FROM expenses")
        row = cursor.fetchone()
        if seed_if_empty and row and row["count"] == 0:
            seed_sample_data_internal(cursor)
            conn.commit()

def seed_sample_data_internal(cursor: sqlite3.Cursor) -> None:
    """Internal helper to insert realistic sample expense records."""
    today = date.today()
    sample_records = [
        # (days_ago, amount, category, description, payment_method)
        (0, 350.0, "Food", "College Cafeteria Lunch & Coffee", "UPI"),
        (0, 180.0, "Transport", "Metro SmartCard Recharge", "UPI"),
        (1, 1450.0, "Education", "Python Data Science Handbook & Notebooks", "Debit Card"),
        (2, 620.0, "Food", "Dinner with Project Team", "UPI"),
        (3, 2199.0, "Shopping", "Wireless Ergonomic Mouse for Coding", "Credit Card"),
        (5, 450.0, "Entertainment", "Weekend Movie Ticket at PVR", "UPI"),
        (7, 1200.0, "Bills", "High-Speed Fiber Broadband Bill", "Net Banking"),
        (8, 250.0, "Transport", "Auto Rickshaw to University Campus", "Cash"),
        (10, 850.0, "Healthcare", "Doctor Consultation & Vitamins", "UPI"),
        (12, 1850.0, "Education", "Online AI & Machine Learning Course Certification", "Credit Card"),
        (14, 520.0, "Food", "Weekly Groceries & Fresh Fruits", "UPI"),
        (16, 950.0, "Shopping", "Backpack & Stationery for College", "UPI"),
        (18, 300.0, "Transport", "Fuel for Two-Wheeler", "Cash"),
        (20, 650.0, "Bills", "Mobile Postpaid Recharge", "UPI"),
        (22, 1100.0, "Food", "Weekend Family Restaurant Dinner", "Credit Card"),
        (25, 420.0, "Entertainment", "Music Streaming Subscription (Annual)", "UPI"),
        (27, 280.0, "Food", "Campus Snacks & Evening Tea", "Cash"),
        (28, 750.0, "Education", "AI Hackathon Registration Fee", "UPI"),
    ]
    
    for days_ago, amount, category, description, payment_method in sample_records:
        exp_date = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO expenses (amount, category, date, description, payment_method)
            VALUES (?, ?, ?, ?, ?)
        """, (amount, category, exp_date, description, payment_method))

def add_expense(amount: float, category: str, exp_date: str, description: str, payment_method: str = "UPI") -> int:
    """
    Inserts a validated expense record into the database.
    Returns the newly generated expense ID.
    """
    if amount <= 0:
        raise ValueError("Expense amount must be strictly greater than zero.")
    if not category:
        raise ValueError("Expense category is mandatory.")
    if not exp_date:
        raise ValueError("Expense date is mandatory.")
        
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (amount, category, date, description, payment_method)
            VALUES (?, ?, ?, ?, ?)
        """, (float(amount), str(category).strip(), str(exp_date).strip(), str(description or "").strip(), str(payment_method)))
        conn.commit()
        return cursor.lastrowid

def update_expense(expense_id: int, amount: float, category: str, exp_date: str, description: str, payment_method: str = "UPI") -> bool:
    """
    Updates an existing expense record by ID.
    Returns True on success, False if record not found.
    """
    if amount <= 0:
        raise ValueError("Expense amount must be strictly greater than zero.")
    if not category:
        raise ValueError("Expense category is mandatory.")
    if not exp_date:
        raise ValueError("Expense date is mandatory.")

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE expenses
            SET amount = ?, category = ?, date = ?, description = ?, payment_method = ?
            WHERE id = ?
        """, (float(amount), str(category).strip(), str(exp_date).strip(), str(description or "").strip(), str(payment_method), int(expense_id)))
        conn.commit()
        return cursor.rowcount > 0

def delete_expense(expense_id: int) -> bool:
    """
    Deletes an expense record by ID.
    Returns True if successfully deleted, False otherwise.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (int(expense_id),))
        conn.commit()
        return cursor.rowcount > 0

def get_expense_by_id(expense_id: int) -> Optional[Dict[str, Any]]:
    """Fetches a single expense record by ID as a dictionary."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (int(expense_id),))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_expenses() -> List[Dict[str, Any]]:
    """Returns all expenses ordered by date descending, then id descending."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC, id DESC")
        return [dict(row) for row in cursor.fetchall()]

def get_filtered_expenses(
    search_query: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    sort_by: str = "date_desc"
) -> List[Dict[str, Any]]:
    """
    Returns filtered and sorted expenses matching criteria.
    Supports search across description, category, and payment method.
    """
    query = "SELECT * FROM expenses WHERE 1=1"
    params: List[Any] = []
    
    if search_query and search_query.strip():
        term = f"%{search_query.strip()}%"
        query += " AND (description LIKE ? OR category LIKE ? OR payment_method LIKE ? OR CAST(amount AS TEXT) LIKE ?)"
        params.extend([term, term, term, term])
        
    if category and category != "All Categories":
        query += " AND category = ?"
        params.append(category)
        
    if start_date:
        query += " AND date >= ?"
        params.append(str(start_date))
        
    if end_date:
        query += " AND date <= ?"
        params.append(str(end_date))
        
    sort_map = {
        "date_desc": "date DESC, id DESC",
        "date_asc": "date ASC, id ASC",
        "amount_desc": "amount DESC, date DESC",
        "amount_asc": "amount ASC, date DESC"
    }
    order_clause = sort_map.get(sort_by, "date DESC, id DESC")
    query += f" ORDER BY {order_clause}"
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def get_statistics() -> Dict[str, Any]:
    """
    Computes key summary statistics using actual database records:
    1. Total Expenses
    2. Today's Expenses
    3. This Month's Expenses
    4. Total Transactions
    5. Highest Spending Category
    6. Average Spending Per Transaction
    """
    today_str = date.today().strftime("%Y-%m-%d")
    current_month_prefix = date.today().strftime("%Y-%m")
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Total Expenses & Total Transactions
        cursor.execute("SELECT COALESCE(SUM(amount), 0) as total, COUNT(*) as count FROM expenses")
        row_total = cursor.fetchone()
        total_expenses = float(row_total["total"]) if row_total else 0.0
        total_transactions = int(row_total["count"]) if row_total else 0
        
        # 2. Today's Expenses
        cursor.execute("SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE date = ?", (today_str,))
        row_today = cursor.fetchone()
        today_expenses = float(row_today["total"]) if row_today else 0.0
        
        # 3. This Month's Expenses
        cursor.execute("SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE date LIKE ?", (f"{current_month_prefix}%",))
        row_month = cursor.fetchone()
        month_expenses = float(row_month["total"]) if row_month else 0.0
        
        # 4. Highest Category
        cursor.execute("""
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
            LIMIT 1
        """)
        row_highest = cursor.fetchone()
        highest_category = row_highest["category"] if row_highest else "None"
        highest_category_amount = float(row_highest["total"]) if row_highest else 0.0
        
        avg_transaction = (total_expenses / total_transactions) if total_transactions > 0 else 0.0
        
        return {
            "total_expenses": total_expenses,
            "today_expenses": today_expenses,
            "this_month_expenses": month_expenses,
            "total_transactions": total_transactions,
            "highest_category": highest_category,
            "highest_category_amount": highest_category_amount,
            "avg_transaction": avg_transaction
        }

def get_category_breakdown() -> List[Dict[str, Any]]:
    """Returns category spending totals and percentages ordered by total descending."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, SUM(amount) as total, COUNT(*) as count
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        """)
        rows = cursor.fetchall()
        
        total_sum = sum(float(r["total"]) for r in rows) if rows else 0.0
        result = []
        for r in rows:
            amount = float(r["total"])
            pct = (amount / total_sum * 100.0) if total_sum > 0 else 0.0
            result.append({
                "category": r["category"],
                "total": amount,
                "count": int(r["count"]),
                "percentage": round(pct, 1)
            })
        return result

def get_monthly_trend(limit_months: int = 6) -> List[Dict[str, Any]]:
    """
    Returns monthly spending trends aggregated by YYYY-MM.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUBSTR(date, 1, 7) as month, SUM(amount) as total, COUNT(*) as count
            FROM expenses
            GROUP BY month
            ORDER BY month ASC
            LIMIT ?
        """, (limit_months,))
        rows = cursor.fetchall()
        return [{"month": r["month"], "total": float(r["total"]), "count": int(r["count"])} for r in rows]

def get_daily_trend(days: int = 14) -> List[Dict[str, Any]]:
    """Returns daily spending aggregated over the last N days."""
    start_date = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, SUM(amount) as total, COUNT(*) as count
            FROM expenses
            WHERE date >= ?
            GROUP BY date
            ORDER BY date ASC
        """, (start_date,))
        rows = cursor.fetchall()
        return [{"date": r["date"], "total": float(r["total"]), "count": int(r["count"])} for r in rows]

def get_setting(key: str, default: str = "") -> str:
    """Retrieves a setting value by key."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row["value"] if row else default

def set_setting(key: str, value: str) -> None:
    """Sets or updates a setting key-value pair."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (key, str(value)))
        conn.commit()

def clear_all_expenses() -> bool:
    """Wipes all records from the expenses table."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses")
        conn.commit()
        return True

def reset_and_seed_data() -> None:
    """Clears all records and re-seeds realistic sample data."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses")
        seed_sample_data_internal(cursor)
        conn.commit()
