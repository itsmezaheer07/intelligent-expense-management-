"""
Sidebar Component for Intelligent Expense Management System
Author: Zaheer Ansari (GUI Developer, BTech 1st Year AI & Data Science)
Description: Renders the branded fintech sidebar, active navigation buttons,
             system status indicators, and student developer credits.
"""

import streamlit as st
import database
import backend

NAV_ITEMS = [
    {"id": "Dashboard", "label": "Dashboard", "icon": "📊"},
    {"id": "Add Expense", "label": "Add Expense", "icon": "➕"},
    {"id": "Expense History", "label": "Expense History", "icon": "📜"},
    {"id": "Analytics", "label": "Analytics", "icon": "📈"},
    {"id": "Settings", "label": "Settings", "icon": "⚙️"},
    {"id": "About Project", "label": "About Project", "icon": "ℹ️"},
]

def render_sidebar():
    """Renders the complete professional fintech sidebar."""
    with st.sidebar:
        # Brand Logo and Title
        st.markdown("""
        <div style="padding: 10px 0 16px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 18px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 42px; height: 42px; border-radius: 12px; background: linear-gradient(135deg, #2563EB, #60A5FA); display: flex; align-items: center; justify-content: center; font-size: 1.4rem; box-shadow: 0 4px 14px rgba(37,99,235,0.4);">
                    💳
                </div>
                <div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; line-height: 1.2;">
                        IntelliSpend
                    </div>
                    <div style="font-size: 0.72rem; color: #93C5FD; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600;">
                        Expense Management
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Current active page in session state
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Dashboard"
            
        current = st.session_state.current_page
        
        st.markdown("<p style='font-size: 0.75rem; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.08em; margin-bottom: 8px;'>Main Menu</p>", unsafe_allow_html=True)
        
        # Navigation Buttons
        for item in NAV_ITEMS:
            page_id = item["id"]
            label = f"{item['icon']}  {item['label']}"
            is_active = (current == page_id)
            
            # Use Streamlit button with active styling indicator
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"nav_{page_id}", use_container_width=True, type=btn_type):
                if st.session_state.current_page != page_id:
                    st.session_state.current_page = page_id
                    st.rerun()

        st.markdown("<div style='margin-top: 24px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 16px;'></div>", unsafe_allow_html=True)

        # Quick monthly summary card in sidebar
        summary = backend.get_dashboard_summary()
        budget = summary["monthly_budget"]
        spent = summary["this_month_expenses"]
        pct = summary["budget_percentage"]
        fill_color = "#16A34A" if pct < 70 else ("#EAB308" if pct < 90 else "#DC2626")
        
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; margin-bottom: 16px;">
            <div style="font-size: 0.78rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;">Monthly Budget</div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF; margin: 4px 0;">₹{spent:,.0f} <span style="font-size:0.8rem; font-weight:400; color:#94A3B8;">/ ₹{budget:,.0f}</span></div>
            <div class="budget-bar-container" style="background: rgba(255,255,255,0.1); height: 6px; margin-top: 6px;">
                <div class="budget-bar-fill" style="width: {min(100.0, pct)}%; background: {fill_color};"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #94A3B8; margin-top: 4px;">
                <span>{pct}% Used</span>
                <span>₹{max(0.0, budget - spent):,.0f} Left</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Student Developer Profile Card
        st.markdown("""
        <div style="background: rgba(37, 99, 235, 0.08); border: 1px solid rgba(37, 99, 235, 0.2); border-radius: 12px; padding: 12px; display: flex; align-items: center; gap: 10px;">
            <div style="width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #2563EB, #1D4ED8); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; color: white;">
                ZA
            </div>
            <div style="overflow: hidden;">
                <div style="font-size: 0.85rem; font-weight: 700; color: #FFFFFF; white-space: nowrap; text-overflow: ellipsis;">Zaheer Ansari</div>
                <div style="font-size: 0.72rem; color: #93C5FD;">GUI Developer • AI & DS</div>
            </div>
        </div>
        <div style="text-align: center; margin-top: 10px; font-size: 0.7rem; color: #64748B;">
            v2.4.0 • Enterprise Edition
        </div>
        """, unsafe_allow_html=True)

