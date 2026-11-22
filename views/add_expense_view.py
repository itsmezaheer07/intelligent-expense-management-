"""
Add Expense View for Intelligent Expense Management System
Author: Zaheer Ansari (GUI Developer, BTech 1st Year AI & Data Science)
Description: High-conversion, fintech-styled expense entry form with strict validation,
             currency formatting, instant feedback notifications, and state resetting.
"""

import streamlit as st
from datetime import date, datetime
import database
import backend
import styles

CATEGORY_OPTIONS = [
    ("Food", "🍔 Food"),
    ("Education", "🎓 Education"),
    ("Transport", "🚗 Transport"),
    ("Shopping", "🛍️ Shopping"),
    ("Entertainment", "🎬 Entertainment"),
    ("Healthcare", "🏥 Healthcare"),
    ("Bills", "💡 Bills"),
    ("Other", "📦 Other"),
]

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]

def render_add_expense(is_dark: bool = False):
    """Renders the Add Expense form with validation and feedback."""
    st.markdown(f"""
    <div class="fintech-header">
        <div>
            <h1>Record New Expense</h1>
            <p>Log your daily expenditure with automated categorization and instant validation</p>
        </div>
        <div>
            <span style="font-size: 2rem;">💳</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Session state initialization for form reset handling
    if "form_reset_counter" not in st.session_state:
        st.session_state.form_reset_counter = 0
    if "expense_submitted_id" not in st.session_state:
        st.session_state.expense_submitted_id = None
        
    cnt = st.session_state.form_reset_counter
    
    # Success banner if just submitted
    if st.session_state.expense_submitted_id:
        submitted_id = st.session_state.expense_submitted_id
        st.success(f"🎉 Expense record #{submitted_id} recorded successfully! Dashboard telemetry updated.")
        st.session_state.expense_submitted_id = None

    # Form card layout
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">📝 Expense Entry Details</div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        amount_input = st.number_input(
            "Expense Amount (INR ₹) *",
            min_value=0.0,
            value=0.0,
            step=50.0,
            format="%.2f",
            help="Enter amount greater than zero.",
            key=f"input_amount_{cnt}"
        )
        
        category_labels = [opt[1] for opt in CATEGORY_OPTIONS]
        selected_cat_label = st.selectbox(
            "Expense Category *",
            options=category_labels,
            index=0,
            help="Select the category that best classifies this transaction.",
            key=f"input_cat_{cnt}"
        )
        # Extract plain category name
        raw_category = [opt[0] for opt in CATEGORY_OPTIONS if opt[1] == selected_cat_label][0]
        
    with col_b:
        expense_date = st.date_input(
            "Expense Date *",
            value=date.today(),
            help="Date on which the expense occurred.",
            key=f"input_date_{cnt}"
        )
        
        payment_method = st.selectbox(
            "Payment Method",
            options=PAYMENT_METHODS,
            index=0,
            help="Select how this expense was settled.",
            key=f"input_pm_{cnt}"
        )
        
    description_input = st.text_input(
        "Expense Description",
        value="",
        placeholder="e.g., College semester textbooks, Cafeteria lunch, Metro card recharge",
        help="Optional brief description or vendor note.",
        key=f"input_desc_{cnt}"
    )
    
    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    
    # Form Action Buttons: Add Expense, Reset Form, Cancel
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1.2, 1, 1, 2])
    
    with btn_col1:
        submit_btn = st.button("➕ Add Expense", use_container_width=True, type="primary")
        
    with btn_col2:
        reset_btn = st.button("🔄 Reset Form", use_container_width=True, type="secondary")
        
    with btn_col3:
        cancel_btn = st.button("✖ Cancel", use_container_width=True, type="secondary")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Handle Form Submission Logic
    if submit_btn:
        # 1. Validation: Amount cannot be empty or <= 0
        if amount_input is None or amount_input <= 0.0:
            st.error("❌ Validation Failed: Expense amount must be strictly greater than zero (₹ 0.00).")
            return
            
        # 2. Validation: Category is required
        if not raw_category:
            st.error("❌ Validation Failed: Please select a valid expense category.")
            return
            
        # 3. Validation: Date must be valid
        if not expense_date:
            st.error("❌ Validation Failed: Expense date cannot be blank.")
            return
            
        date_str = expense_date.strftime("%Y-%m-%d")
        safe_desc = description_input.strip() if description_input else "Expense"
        
        try:
            new_id = database.add_expense(
                amount=amount_input,
                category=raw_category,
                date=date_str,
                description=safe_desc,
                payment_method=payment_method
            )
            # Increment counter to reset input widgets
            st.session_state.form_reset_counter += 1
            st.session_state.expense_submitted_id = new_id
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error saving expense: {str(e)}")

    # Handle Reset Form
    if reset_btn:
        st.session_state.form_reset_counter += 1
        st.toast("Form fields reset.", icon="🔄")
        st.rerun()

    # Handle Cancel (navigate back to Dashboard)
    if cancel_btn:
        st.session_state.current_page = "Dashboard"
        st.rerun()

    # Quick preview of today's logged expenses
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">📅 Today's Logged Transactions</div>
    """, unsafe_allow_html=True)
    
    today_str = date.today().strftime("%Y-%m-%d")
    today_records = database.get_filtered_expenses(start_date=today_str, end_date=today_str)
    
    if today_records:
        for rec in today_records:
            badge = styles.get_category_badge(rec["category"])
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid {'rgba(255,255,255,0.06)' if is_dark else '#F1F5F9'};">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div>{badge}</div>
                    <div style="font-weight: 600; font-size: 0.88rem; color: {'#F8FAFC' if is_dark else '#1E293B'};">{rec['description'] or 'Expense'}</div>
                </div>
                <div style="font-weight: 700; color: {'#F8FAFC' if is_dark else '#0B1220'};">₹{rec['amount']:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <p style="color: {'#94A3B8' if is_dark else '#64748B'}; font-size: 0.9rem; margin: 0;">
            No transactions logged today yet. Use the form above to record your first expense of the day.
        </p>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

