"""
Expense History / Ledger View for Intelligent Expense Management System
Author: Zaheer Ansari (GUI Developer, BTech 1st Year AI & Data Science)
Description: Financial ledger featuring real-time search, multi-factor filtering,
             sorting, inline editing, delete confirmation modals, and friendly empty states.
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import database
import backend
import styles

SORT_OPTIONS = {
    "Date (Newest First)": "date_desc",
    "Date (Oldest First)": "date_asc",
    "Amount (Highest First)": "amount_desc",
    "Amount (Lowest First)": "amount_asc",
}

CATEGORIES_FILTER = [
    "All Categories",
    "Food",
    "Education",
    "Transport",
    "Shopping",
    "Entertainment",
    "Healthcare",
    "Bills",
    "Other",
]

def render_history(is_dark: bool = False):
    """Renders the comprehensive transaction history ledger."""
    st.markdown(f"""
    <div class="fintech-header">
        <div>
            <h1>Expense History & Audit Ledger</h1>
            <p>Search, filter, edit and audit all logged transactions across accounts</p>
        </div>
        <div>
            <span style="font-size: 2rem;">📜</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Session state for managing Edit and Delete operations
    if "editing_expense_id" not in st.session_state:
        st.session_state.editing_expense_id = None
    if "deleting_expense_id" not in st.session_state:
        st.session_state.deleting_expense_id = None

    # Filter Toolbar Card
    st.markdown(f"""
    <div class="fintech-card" style="padding: 18px 22px; margin-bottom: 20px;">
    """, unsafe_allow_html=True)
    
    fcol1, fcol2, fcol3, fcol4 = st.columns([1.5, 1.1, 1.2, 1.2])
    
    with fcol1:
        search_query = st.text_input(
            "🔍 Search Transactions",
            value="",
            placeholder="Search description, category, payment mode...",
            key="hist_search_box"
        )
        
    with fcol2:
        selected_cat = st.selectbox(
            "Category Filter",
            options=CATEGORIES_FILTER,
            index=0,
            key="hist_cat_filter"
        )
        
    with fcol3:
        date_filter_option = st.selectbox(
            "Date Range",
            options=["All Time", "Today", "Last 7 Days", "This Month", "Custom Range"],
            index=0,
            key="hist_date_preset"
        )
        
    with fcol4:
        sort_label = st.selectbox(
            "Sort Order",
            options=list(SORT_OPTIONS.keys()),
            index=0,
            key="hist_sort_select"
        )
        
    start_date_val = None
    end_date_val = None
    today = date.today()
    
    if date_filter_option == "Today":
        start_date_val = today.strftime("%Y-%m-%d")
        end_date_val = today.strftime("%Y-%m-%d")
    elif date_filter_option == "Last 7 Days":
        start_date_val = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date_val = today.strftime("%Y-%m-%d")
    elif date_filter_option == "This Month":
        start_date_val = today.replace(day=1).strftime("%Y-%m-%d")
        end_date_val = today.strftime("%Y-%m-%d")
    elif date_filter_option == "Custom Range":
        ccol1, ccol2 = st.columns(2)
        with ccol1:
            d_start = st.date_input("Start Date", value=today - timedelta(days=30), key="hist_custom_start")
            start_date_val = d_start.strftime("%Y-%m-%d")
        with ccol2:
            d_end = st.date_input("End Date", value=today, key="hist_custom_end")
            end_date_val = d_end.strftime("%Y-%m-%d")
            
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Fetch filtered expenses from database
    sort_code = SORT_OPTIONS[sort_label]
    cat_param = selected_cat if selected_cat != "All Categories" else None
    
    records = database.get_filtered_expenses(
        search_query=search_query,
        category=cat_param,
        start_date=start_date_val,
        end_date=end_date_val,
        sort_by=sort_code
    )
    
    # Delete Confirmation Dialog handling
    if st.session_state.deleting_expense_id is not None:
        del_id = st.session_state.deleting_expense_id
        exp_to_del = database.get_expense_by_id(del_id)
        if exp_to_del:
            st.warning(f"⚠️ **Confirm Deletion**: Are you sure you want to delete expense record **#{del_id}** ('{exp_to_del['description']}', ₹{exp_to_del['amount']:,.2f})? This action cannot be undone.")
            dcol1, dcol2, dcol3 = st.columns([1, 1, 3])
            with dcol1:
                if st.button("🗑️ Yes, Delete", key="confirm_del_btn", type="primary"):
                    database.delete_expense(del_id)
                    st.session_state.deleting_expense_id = None
                    st.toast(f"Expense #{del_id} deleted successfully.", icon="🗑️")
                    st.rerun()
            with dcol2:
                if st.button("Cancel", key="cancel_del_btn", type="secondary"):
                    st.session_state.deleting_expense_id = None
                    st.rerun()
        else:
            st.session_state.deleting_expense_id = None

    # Edit Expense Form handling
    if st.session_state.editing_expense_id is not None:
        edit_id = st.session_state.editing_expense_id
        edit_item = database.get_expense_by_id(edit_id)
        if edit_item:
            st.markdown(f"""
            <div class="fintech-card" style="border: 2px solid #2563EB;">
                <div class="fintech-card-title">✏️ Editing Expense Record #{edit_id}</div>
            """, unsafe_allow_html=True)
            
            ecol1, ecol2, ecol3 = st.columns(3)
            with ecol1:
                e_amt = st.number_input("Amount (₹) *", min_value=1.0, value=float(edit_item["amount"]), step=50.0, key="edit_amt")
            with ecol2:
                all_cats = [c for c in CATEGORIES_FILTER if c != "All Categories"]
                cat_idx = all_cats.index(edit_item["category"]) if edit_item["category"] in all_cats else 0
                e_cat = st.selectbox("Category *", options=all_cats, index=cat_idx, key="edit_cat")
            with ecol3:
                try:
                    cur_date = datetime.strptime(edit_item["date"], "%Y-%m-%d").date()
                except Exception:
                    cur_date = date.today()
                e_date = st.date_input("Date *", value=cur_date, key="edit_date")
                
            ecol4, ecol5 = st.columns([2, 1])
            with ecol4:
                e_desc = st.text_input("Description", value=edit_item["description"] or "", key="edit_desc")
            with ecol5:
                pms = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]
                cur_pm = edit_item.get("payment_method", "UPI")
                pm_idx = pms.index(cur_pm) if cur_pm in pms else 0
                e_pm = st.selectbox("Payment Method", options=pms, index=pm_idx, key="edit_pm")
                
            ebtn1, ebtn2, ebtn3 = st.columns([1.2, 1, 3])
            with ebtn1:
                if st.button("💾 Save Changes", key="save_edit_btn", type="primary"):
                    if e_amt <= 0:
                        st.error("Amount must be greater than zero.")
                    else:
                        database.update_expense(
                            expense_id=edit_id,
                            amount=e_amt,
                            category=e_cat,
                            date=e_date.strftime("%Y-%m-%d"),
                            description=e_desc,
                            payment_method=e_pm
                        )
                        st.session_state.editing_expense_id = None
                        st.toast(f"Expense #{edit_id} updated successfully!", icon="✅")
                        st.rerun()
            with ebtn2:
                if st.button("Cancel", key="cancel_edit_btn", type="secondary"):
                    st.session_state.editing_expense_id = None
                    st.rerun()
                    
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
        else:
            st.session_state.editing_expense_id = None

    # Ledger Summary Statistics Bar
    total_filtered_amt = sum(r["amount"] for r in records)
    record_count = len(records)
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding: 0 4px;">
        <div style="font-size: 0.95rem; font-weight: 700; color: {'#F8FAFC' if is_dark else '#0B1220'};">
            Showing <span style="color: #2563EB;">{record_count}</span> transactions
        </div>
        <div style="font-size: 0.95rem; font-weight: 700; color: {'#F8FAFC' if is_dark else '#0B1220'};">
            Filtered Total: <span style="color: #16A34A;">₹{total_filtered_amt:,.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Ledger Table or Empty State
    if not records:
        st.markdown(f"""
        <div class="empty-state-box">
            <div class="empty-state-icon">📭</div>
            <div class="empty-state-title">No Transactions Found</div>
            <div class="empty-state-text">
                No expense entries match your current search and filter criteria. Adjust your filters or log a new transaction.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_center = st.columns([2, 1, 2])
        with btn_center[1]:
            if st.button("➕ Add New Expense", key="empty_add_btn", use_container_width=True, type="primary"):
                st.session_state.current_page = "Add Expense"
                st.rerun()
        return

    # Render Table Header
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 60px 110px 140px 1fr 110px 110px 140px; gap: 8px; padding: 10px 16px; background: {'#111C30' if is_dark else '#E2E8F0'}; border-radius: 8px; font-weight: 700; font-size: 0.8rem; color: {'#94A3B8' if is_dark else '#475569'}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">
        <div>ID</div>
        <div>Date</div>
        <div>Category</div>
        <div>Description</div>
        <div>Method</div>
        <div style="text-align: right;">Amount</div>
        <div style="text-align: center;">Actions</div>
    </div>
    """, unsafe_allow_html=True)

    # Render Table Rows
    for r in records:
        exp_id = r["id"]
        exp_date = r["date"]
        exp_cat = r["category"]
        exp_desc = r["description"] or "—"
        exp_pm = r.get("payment_method", "UPI")
        exp_amt = r["amount"]
        badge_html = styles.get_category_badge(exp_cat)
        
        # Grid layout with Streamlit columns for action buttons
        col_id, col_date, col_cat, col_desc, col_pm, col_amt, col_acts = st.columns([0.6, 1.1, 1.4, 3.0, 1.1, 1.2, 1.4])
        
        with col_id:
            st.markdown(f"<span style='font-weight: 700; color: #94A3B8; font-size: 0.85rem;'>#{exp_id}</span>", unsafe_allow_html=True)
        with col_date:
            st.markdown(f"<span style='font-size: 0.85rem; color: {'#F8FAFC' if is_dark else '#1E293B'};'>{exp_date}</span>", unsafe_allow_html=True)
        with col_cat:
            st.markdown(badge_html, unsafe_allow_html=True)
        with col_desc:
            st.markdown(f"<span style='font-size: 0.88rem; font-weight: 500; color: {'#F8FAFC' if is_dark else '#1E293B'};'>{exp_desc}</span>", unsafe_allow_html=True)
        with col_pm:
            st.markdown(f"<span style='font-size: 0.8rem; color: #64748B;'>{exp_pm}</span>", unsafe_allow_html=True)
        with col_amt:
            st.markdown(f"<span style='font-weight: 700; font-size: 0.92rem; color: {'#F8FAFC' if is_dark else '#0B1220'};'>₹{exp_amt:,.2f}</span>", unsafe_allow_html=True)
        with col_acts:
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("✏️", key=f"edit_{exp_id}", help="Edit this expense"):
                    st.session_state.editing_expense_id = exp_id
                    st.rerun()
            with act_col2:
                if st.button("🗑️", key=f"del_{exp_id}", help="Delete this expense"):
                    st.session_state.deleting_expense_id = exp_id
                    st.rerun()
                    
        st.markdown(f"<div style='border-bottom: 1px solid {'rgba(255,255,255,0.05)' if is_dark else '#F1F5F9'}; margin: 4px 0 8px 0;'></div>", unsafe_allow_html=True)
        
    # Quick Export options
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    exp_col1, exp_col2, exp_col3 = st.columns([1.5, 1.5, 2])
    with exp_col1:
        df_export = backend.export_expenses_to_dataframe()
        csv_data = df_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Ledger as CSV",
            data=csv_data,
            file_name=f"IntelliSpend_Ledger_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )

