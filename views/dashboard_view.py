"""
Dashboard View for Intelligent Expense Management System
Author: Zaheer Ansari (GUI Developer, BTech 1st Year AI & Data Science)
Description: Flagship executive dashboard presenting 4 core KPI summary cards,
             dynamic Plotly charts (Category Bar, Donut Distribution, Monthly Trend),
             budget utilization progress, AI insights, and recent transactions.
"""

import streamlit as st
from datetime import datetime, date
import database
import backend
import styles

def render_dashboard(is_dark: bool = False):
    """Renders the executive financial dashboard."""
    # Top Welcome Banner
    today_formatted = datetime.now().strftime("%A, %d %B %Y")
    st.markdown(f"""
    <div class="fintech-header">
        <div>
            <h1>Financial Dashboard</h1>
            <p>Welcome back, <b>Zaheer Ansari</b> • {today_formatted} • Live Financial Telemetry</p>
        </div>
        <div style="display: none; @media(min-width: 768px){{display: block;}}">
            <span style="background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 9999px; font-size: 0.82rem; font-weight: 600; border: 1px solid rgba(255,255,255,0.2);">
                🟢 System Synchronized
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch live summary statistics
    summary = backend.get_dashboard_summary()
    total_spent = summary["total_expenses"]
    today_spent = summary["today_expenses"]
    month_spent = summary["this_month_expenses"]
    tx_count = summary["total_transactions"]
    avg_tx = summary["avg_transaction"]
    budget = summary["monthly_budget"]
    pct_budget = summary["budget_percentage"]
    
    # 4 Summary Cards Grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        card1 = styles.render_metric_card(
            title="Total Expenses",
            value=f"₹{total_spent:,.2f}",
            subtext=f"<span>Lifetime All Records</span>",
            icon="💰",
            accent="primary"
        )
        st.markdown(card1, unsafe_allow_html=True)
        
    with col2:
        card2 = styles.render_metric_card(
            title="Today's Expenses",
            value=f"₹{today_spent:,.2f}",
            subtext=f"<span>Recorded Today</span>",
            icon="📅",
            accent="success" if today_spent == 0 else "warning"
        )
        st.markdown(card2, unsafe_allow_html=True)
        
    with col3:
        card3 = styles.render_metric_card(
            title="This Month's Expenses",
            value=f"₹{month_spent:,.2f}",
            subtext=f"<span>{pct_budget}% of ₹{budget:,.0f} Budget</span>",
            icon="🗓️",
            accent="purple"
        )
        st.markdown(card3, unsafe_allow_html=True)
        
    with col4:
        card4 = styles.render_metric_card(
            title="Total Transactions",
            value=f"{tx_count}",
            subtext=f"<span>Avg: ₹{avg_tx:,.0f} / tx</span>",
            icon="🧾",
            accent="primary"
        )
        st.markdown(card4, unsafe_allow_html=True)
        
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    # Budget Progress Bar Card
    fill_color = "#16A34A" if pct_budget < 70 else ("#EAB308" if pct_budget < 90 else "#DC2626")
    st.markdown(f"""
    <div class="fintech-card" style="padding: 16px 20px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-weight: 700; font-size: 0.95rem; color: {'#F8FAFC' if is_dark else '#0B1220'};">
                🎯 Monthly Spending Target: <b>₹{budget:,.0f}</b>
            </div>
            <div style="font-size: 0.85rem; font-weight: 600; color: {fill_color};">
                {pct_budget}% Utilized • ₹{max(0.0, budget - month_spent):,.0f} Remaining
            </div>
        </div>
        <div class="budget-bar-container" style="background: {'#1E293B' if is_dark else '#E2E8F0'}; height: 8px;">
            <div class="budget-bar-fill" style="width: {min(100.0, pct_budget)}%; background: {fill_color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Charts Section - Two columns
    chart_col1, chart_col2 = st.columns([1.1, 0.9])
    
    with chart_col1:
        st.markdown(f"""
        <div class="fintech-card">
            <div class="fintech-card-title">📊 Category Breakdown</div>
        """, unsafe_allow_html=True)
        fig_bar = backend.create_category_bar_chart(is_dark=is_dark)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with chart_col2:
        st.markdown(f"""
        <div class="fintech-card">
            <div class="fintech-card-title">🍩 Expense Distribution</div>
        """, unsafe_allow_html=True)
        fig_pie = backend.create_category_pie_chart(is_dark=is_dark)
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Full Width Monthly Spending Trend Chart
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">📈 Monthly Spending Trajectory & Historical Trends</div>
    """, unsafe_allow_html=True)
    fig_trend = backend.create_monthly_trend_chart(is_dark=is_dark)
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Bottom Section: AI Insights & Quick Recent Ledger
    bottom_col1, bottom_col2 = st.columns([1.2, 0.8])
    
    with bottom_col1:
        st.markdown(f"""
        <div class="fintech-card">
            <div class="fintech-card-title" style="display: flex; justify-content: space-between;">
                <span>⏱️ Recent Transactions</span>
                <span style="font-size: 0.8rem; font-weight: 500; color: #2563EB; cursor: pointer;">
                    Top 5 Latest
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        all_expenses = database.get_filtered_expenses(sort_by="date_desc")[:5]
        if all_expenses:
            for exp in all_expenses:
                badge_html = styles.get_category_badge(exp["category"])
                exp_date = exp["date"]
                desc = exp["description"] or "Uncategorized Item"
                amt = exp["amount"]
                pm = exp.get("payment_method", "UPI")
                
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid {'rgba(255,255,255,0.06)' if is_dark else '#F1F5F9'};">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div>{badge_html}</div>
                        <div>
                            <div style="font-weight: 600; font-size: 0.9rem; color: {'#F8FAFC' if is_dark else '#1E293B'};">{desc}</div>
                            <div style="font-size: 0.75rem; color: #94A3B8;">{exp_date} • via {pm}</div>
                        </div>
                    </div>
                    <div style="font-weight: 700; font-size: 0.95rem; color: {'#F8FAFC' if is_dark else '#0B1220'};">
                        ₹{amt:,.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("View Full Ledger in Expense History ➔", key="dash_view_history_btn"):
                st.session_state.current_page = "Expense History"
                st.rerun()
        else:
            st.markdown("""
            <div class="empty-state-box" style="padding: 24px 16px;">
                <div class="empty-state-icon" style="font-size: 2rem;">📭</div>
                <div class="empty-state-title" style="font-size: 1rem;">No Transactions Yet</div>
                <div class="empty-state-text" style="font-size: 0.8rem;">Add your first expense to begin tracking.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("➕ Add First Expense", key="dash_add_first_btn"):
                st.session_state.current_page = "Add Expense"
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)
        
    with bottom_col2:
        st.markdown(f"""
        <div class="fintech-card">
            <div class="fintech-card-title">🤖 AI & Analytics Insights</div>
        """, unsafe_allow_html=True)
        
        insights = backend.generate_ai_insights()
        for ins in insights:
            border_color = "#2563EB" if ins["type"] == "info" else ("#16A34A" if ins["type"] == "success" else ("#EAB308" if ins["type"] == "warning" else "#DC2626"))
            st.markdown(f"""
            <div style="background: {'rgba(37, 99, 235, 0.05)' if is_dark else '#F8FAFC'}; border-left: 3px solid {border_color}; border-radius: 8px; padding: 12px 14px; margin-bottom: 12px;">
                <div style="font-weight: 700; font-size: 0.85rem; color: {'#F8FAFC' if is_dark else '#0B1220'}; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;">
                    <span>{ins['icon']}</span> {ins['title']}
                </div>
                <div style="font-size: 0.8rem; color: {'#94A3B8' if is_dark else '#64748B'}; line-height: 1.4;">
                    {ins['text']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        if st.button("Explore Advanced Analytics ➔", key="dash_view_analytics_btn"):
            st.session_state.current_page = "Analytics"
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)

