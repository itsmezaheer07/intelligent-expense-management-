"""
Settings View for Intelligent Expense Management System
Author: Zaheer Ansari (GUI Developer, BTech 1st Year AI & Data Science)
Description: Manages theme toggling (Light / Dark mode), currency preference,
             monthly budget thresholds, database backups, reset operations,
             and sample dataset seeding.
"""

import streamlit as st
import json
from datetime import date
import database
import backend

def render_settings(is_dark: bool = False):
    """Renders the settings and configuration page."""
    st.markdown(f"""
    <div class="fintech-header">
        <div>
            <h1>System Settings & Preferences</h1>
            <p>Configure interface themes, budget targets, currency conventions, and database state</p>
        </div>
        <div>
            <span style="font-size: 2rem;">⚙️</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. Interface & Theme Configuration
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">🎨 Appearance & Interface Mode</div>
    """, unsafe_allow_html=True)
    
    current_theme = database.get_setting("theme", "light")
    theme_options = ["Light Mode", "Dark Mode"]
    theme_idx = 0 if current_theme == "light" else 1
    
    tcol1, tcol2 = st.columns([1.5, 2])
    with tcol1:
        selected_theme_label = st.radio(
            "Select Application Theme",
            options=theme_options,
            index=theme_idx,
            help="Toggle between clean fintech Light Mode and high-contrast Dark Mode."
        )
        new_theme = "light" if selected_theme_label == "Light Mode" else "dark"
        if new_theme != current_theme:
            database.set_setting("theme", new_theme)
            st.session_state.app_theme = new_theme
            st.toast(f"Theme switched to {selected_theme_label}!", icon="🎨")
            st.rerun()
            
    with tcol2:
        st.markdown(f"""
        <div style="background: {'rgba(255,255,255,0.05)' if is_dark else '#F8FAFC'}; border: 1px solid {'rgba(255,255,255,0.1)' if is_dark else '#E2E8F0'}; border-radius: 10px; padding: 14px;">
            <div style="font-weight: 700; font-size: 0.9rem; margin-bottom: 6px; color: {'#F8FAFC' if is_dark else '#0B1220'};">Current Palette Specs:</div>
            <div style="font-size: 0.82rem; color: {'#94A3B8' if is_dark else '#64748B'}; line-height: 1.5;">
                • Primary Navy: <code>#0B1220</code><br>
                • Royal Blue Accent: <code>#2563EB</code><br>
                • Background: <code>{'#0B1220 (Dark)' if is_dark else '#F5F7FB (Light)'}</code><br>
                • Status Accents: Success <code>#16A34A</code>, Danger <code>#DC2626</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 2. Currency & Budget Thresholds
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">💵 Currency & Budget Allocation</div>
    """, unsafe_allow_html=True)
    
    cur_budget = float(database.get_setting("monthly_budget", "35000"))
    cur_currency = database.get_setting("currency", "₹")
    
    bcol1, bcol2 = st.columns(2)
    with bcol1:
        new_currency = st.selectbox(
            "Active Currency Standard",
            options=["₹ - Indian Rupee (INR)", "$ - US Dollar (USD)", "€ - Euro (EUR)", "£ - British Pound (GBP)"],
            index=0,
            help="Default currency formatting used throughout the system."
        )
        symbol = new_currency.split(" ")[0]
        if symbol != cur_currency:
            database.set_setting("currency", symbol)
            st.toast(f"Currency updated to {symbol}", icon="💵")
            st.rerun()
            
    with bcol2:
        new_budget = st.number_input(
            "Monthly Spending Target / Budget (₹)",
            min_value=1000.0,
            max_value=1000000.0,
            value=cur_budget,
            step=5000.0,
            help="Set your monthly spending ceiling for dashboard alert calculations."
        )
        if new_budget != cur_budget:
            if st.button("Update Monthly Budget", key="update_budget_btn", type="primary"):
                database.set_setting("monthly_budget", str(new_budget))
                st.toast(f"Monthly budget updated to ₹{new_budget:,.0f}!", icon="🎯")
                st.rerun()
                
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 3. Data Management Studio (Backup, Export, Seed & Reset)
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">💾 Data Operations & Backup Studio</div>
    """, unsafe_allow_html=True)
    
    dcol1, dcol2 = st.columns(2)
    with dcol1:
        st.markdown(f"<p style='font-weight: 600; font-size: 0.9rem; color: {'#F8FAFC' if is_dark else '#0B1220'};'>Export Data</p>", unsafe_allow_html=True)
        # CSV Export
        df_export = backend.export_expenses_to_dataframe()
        csv_bytes = df_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Full Ledger to CSV",
            data=csv_bytes,
            file_name=f"IntelliSpend_FullBackup_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # JSON Export
        all_raw = database.get_all_expenses()
        json_str = json.dumps(all_raw, indent=2)
        st.download_button(
            label="📥 Export Database as JSON",
            data=json_str.encode("utf-8"),
            file_name=f"IntelliSpend_Backup_{date.today()}.json",
            mime="application/json",
            use_container_width=True
        )
        
    with dcol2:
        st.markdown(f"<p style='font-weight: 600; font-size: 0.9rem; color: {'#F8FAFC' if is_dark else '#0B1220'};'>Sample Data & Reset</p>", unsafe_allow_html=True)
        if st.button("🌱 Load Realistic Demo Dataset (18 Transactions)", use_container_width=True, type="secondary"):
            database.reset_and_seed_data()
            st.toast("Realistic demo dataset seeded successfully!", icon="🌱")
            st.rerun()
            
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        
        # Danger zone with confirmation
        if "confirm_wipe" not in st.session_state:
            st.session_state.confirm_wipe = False
            
        if not st.session_state.confirm_wipe:
            if st.button("⚠️ Wipe / Reset All Expense Records", use_container_width=True, type="secondary"):
                st.session_state.confirm_wipe = True
                st.rerun()
        else:
            st.error("🚨 Are you sure you want to delete all expenses? This will clear all transactions.")
            wcol1, wcol2 = st.columns(2)
            with wcol1:
                if st.button("Yes, Wipe All", key="wipe_confirm", type="primary"):
                    database.clear_all_expenses()
                    st.session_state.confirm_wipe = False
                    st.toast("All expense records cleared.", icon="🗑️")
                    st.rerun()
            with wcol2:
                if st.button("Cancel", key="wipe_cancel", type="secondary"):
                    st.session_state.confirm_wipe = False
                    st.rerun()
                    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 4. System & Developer Credits
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">ℹ️ System Specifications & Credits</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; font-size: 0.88rem;">
            <div>
                <span style="color: #94A3B8;">Project Title:</span><br>
                <b style="color: {'#F8FAFC' if is_dark else '#0B1220'};">Intelligent Expense Management System</b>
            </div>
            <div>
                <span style="color: #94A3B8;">Lead GUI Developer:</span><br>
                <b style="color: #2563EB;">Zaheer Ansari</b>
            </div>
            <div>
                <span style="color: #94A3B8;">Academic Department:</span><br>
                <b style="color: {'#F8FAFC' if is_dark else '#0B1220'};">BTech 1st Year (AI & Data Science)</b>
            </div>
            <div>
                <span style="color: #94A3B8;">Architecture Stack:</span><br>
                <b style="color: {'#F8FAFC' if is_dark else '#0B1220'};">Python 3.15 • Streamlit • Plotly • SQLite</b>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

