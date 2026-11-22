"""
Unit & Integration Test Suite for Intelligent Expense Management System
Author: Zaheer Ansari (GUI Developer, BTech 1st Year AI & Data Science)
Description: Verifies all backend, database, validation, statistics, and chart rendering logic.
"""

import sys
import os
import unittest
from datetime import date, datetime

import database
import backend
import styles

class TestExpenseManagementSystem(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Initialize database before running tests."""
        database.init_db(seed_if_empty=True)
        
    def test_01_database_initialization(self):
        """Test database tables and default records exist."""
        stats = database.get_statistics()
        self.assertIn("total_expenses", stats)
        self.assertIn("total_transactions", stats)
        self.assertGreaterEqual(stats["total_transactions"], 0)
        
    def test_02_add_expense_valid(self):
        """Test adding a valid expense."""
        today_str = date.today().strftime("%Y-%m-%d")
        new_id = database.add_expense(
            amount=500.0,
            category="Food",
            exp_date=today_str,
            description="Unit Test Lunch",
            payment_method="UPI"
        )
        self.assertIsInstance(new_id, int)
        self.assertGreater(new_id, 0)
        
        # Verify fetched
        rec = database.get_expense_by_id(new_id)
        self.assertIsNotNone(rec)
        self.assertEqual(rec["amount"], 500.0)
        self.assertEqual(rec["category"], "Food")
        self.assertEqual(rec["description"], "Unit Test Lunch")
        self.assertEqual(rec["payment_method"], "UPI")
        
    def test_03_add_expense_validation_zero_negative(self):
        """Test that zero or negative amount raises ValueError."""
        today_str = date.today().strftime("%Y-%m-%d")
        with self.assertRaises(ValueError):
            database.add_expense(0.0, "Food", today_str, "Zero amount test")
        with self.assertRaises(ValueError):
            database.add_expense(-150.0, "Food", today_str, "Negative amount test")
            
    def test_04_add_expense_validation_category_date(self):
        """Test that missing category or date raises ValueError."""
        today_str = date.today().strftime("%Y-%m-%d")
        with self.assertRaises(ValueError):
            database.add_expense(100.0, "", today_str, "Missing category")
        with self.assertRaises(ValueError):
            database.add_expense(100.0, "Food", "", "Missing date")
            
    def test_05_update_expense(self):
        """Test updating an existing expense."""
        today_str = date.today().strftime("%Y-%m-%d")
        new_id = database.add_expense(200.0, "Transport", today_str, "Pre-update", "Cash")
        
        success = database.update_expense(
            expense_id=new_id,
            amount=350.0,
            category="Education",
            exp_date=today_str,
            description="Post-update",
            payment_method="Debit Card"
        )
        self.assertTrue(success)
        
        updated = database.get_expense_by_id(new_id)
        self.assertEqual(updated["amount"], 350.0)
        self.assertEqual(updated["category"], "Education")
        self.assertEqual(updated["description"], "Post-update")
        self.assertEqual(updated["payment_method"], "Debit Card")
        
    def test_06_delete_expense(self):
        """Test deleting an expense."""
        today_str = date.today().strftime("%Y-%m-%d")
        new_id = database.add_expense(120.0, "Other", today_str, "To be deleted")
        self.assertIsNotNone(database.get_expense_by_id(new_id))
        
        deleted = database.delete_expense(new_id)
        self.assertTrue(deleted)
        self.assertIsNone(database.get_expense_by_id(new_id))
        
    def test_07_filter_and_search(self):
        """Test search and filter functionality."""
        today_str = date.today().strftime("%Y-%m-%d")
        test_tag = f"SpecialSearchTag_{int(datetime.now().timestamp())}"
        database.add_expense(888.0, "Shopping", today_str, test_tag)
        
        # Search by unique keyword
        results = database.get_filtered_expenses(search_query=test_tag)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["description"], test_tag)
        
        # Filter by category
        shopping_res = database.get_filtered_expenses(category="Shopping")
        for r in shopping_res:
            self.assertEqual(r["category"], "Shopping")
            
    def test_08_statistics_calculations(self):
        """Test summary statistics calculation."""
        stats = database.get_statistics()
        self.assertGreater(stats["total_expenses"], 0)
        self.assertGreater(stats["total_transactions"], 0)
        self.assertIn("highest_category", stats)
        self.assertGreaterEqual(stats["avg_transaction"], 0)
        
    def test_09_backend_charts_generation(self):
        """Test that all Plotly figures render without error."""
        fig_bar = backend.create_category_bar_chart(is_dark=False)
        self.assertIsNotNone(fig_bar)
        
        fig_pie = backend.create_category_pie_chart(is_dark=False)
        self.assertIsNotNone(fig_pie)
        
        fig_trend = backend.create_monthly_trend_chart(is_dark=False)
        self.assertIsNotNone(fig_trend)
        
        fig_pm = backend.create_payment_methods_chart(is_dark=False)
        self.assertIsNotNone(fig_pm)
        
    def test_10_ai_insights(self):
        """Test AI insight generation."""
        insights = backend.generate_ai_insights()
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        for ins in insights:
            self.assertIn("title", ins)
            self.assertIn("text", ins)
            self.assertIn("type", ins)
            
    def test_11_styles_theme_css(self):
        """Test CSS styles for light and dark modes."""
        light_css = styles.get_theme_css("light")
        self.assertIn("#F5F7FB", light_css)
        self.assertIn("#0B1220", light_css)
        self.assertIn("#2563EB", light_css)
        
        dark_css = styles.get_theme_css("dark")
        self.assertIn("#0B1220", dark_css)
        self.assertIn("#2563EB", dark_css)
        
    def test_12_export_dataframe(self):
        """Test export to pandas dataframe."""
        df = backend.export_expenses_to_dataframe()
        self.assertFalse(df.empty)
        self.assertIn("Amount (₹)", df.columns)
        self.assertIn("Category", df.columns)

if __name__ == "__main__":
    unittest.main()

