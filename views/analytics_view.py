"""
Analytics View for Intelligent Expense Management System
Author: Zaheer Ansari (GUI Developer, BTech 1st Year AI & Data Science)
Description: In-depth financial analytics, category distributions, monthly comparisons,
             outlier detection, payment method breakdowns, and AI-driven pattern insights.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import database
import backend
import styles
from datetime import datetime

def render_analytics(is_dark: bool = False):
    """Renders the comprehensive analytics view."""
    st.markdown(f"""
    <div class="fintech-header">
        <div>
            <h1>Financial Analytics & AI Insights</h1>
            <p>Data science metrics, spending trajectories, category concentration, and behavioral patterns</p>
        </div>
        <div>
            <span style="font-size: 2rem;">📈</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    summary = backend.get_dashboard_summary()
    total_spent = summary["total_expenses"]
    highest_cat = summary["highest_category"]
    highest_cat_amt = summary["highest_category_amount"]
    avg_tx = summary["avg_transaction"]
    tx_count = summary["total_transactions"]
    
    if tx_count == 0:
        st.markdown(f"""
        <div class="empty-state-box">
            <div class="empty-state-icon">📊</div>
            <div class="empty-state-title">No Analytics Data Available</div>
            <div class="empty-state-text">
                Analytics and AI telemetry will activate automatically once you record your first expenses.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("➕ Record New Expense", key="an_add_first", type="primary"):
            st.session_state.current_page = "Add Expense"
            st.rerun()
        return

    # KPI Top Bar
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(styles.render_metric_card(
            title="Total Spend",
            value=f"₹{total_spent:,.2f}",
            subtext="<span>Cumulative Outflow</span>",
            icon="💎",
            accent="primary"
        ), unsafe_allow_html=True)
    with kpi2:
        st.markdown(styles.render_metric_card(
            title="Highest Category",
            value=f"{highest_cat}",
            subtext=f"<span>₹{highest_cat_amt:,.0f} Total</span>",
            icon="🏆",
            accent="purple"
        ), unsafe_allow_html=True)
    with kpi3:
        st.markdown(styles.render_metric_card(
            title="Average Ticket",
            value=f"₹{avg_tx:,.2f}",
            subtext=f"<span>Across {tx_count} Transactions</span>",
            icon="📊",
            accent="success"
        ), unsafe_allow_html=True)
    with kpi4:
        st.markdown(styles.render_metric_card(
            title="Total Volume",
            value=f"{tx_count}",
            subtext="<span>Logged Records</span>",
            icon="🧾",
            accent="warning"
        ), unsafe_allow_html=True)
        
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # Visual Analytics Row 1: Category Bar & Donut
    c1, c2 = st.columns([1.1, 0.9])
    with c1:
        st.markdown(f"""
        <div class="fintech-card">
            <div class="fintech-card-title">📊 Category-Wise Spending Allocation</div>
        """, unsafe_allow_html=True)
        fig_bar = backend.create_category_bar_chart(is_dark=is_dark)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="fintech-card">
            <div class="fintech-card-title">🍩 Category Percentage Share</div>
        """, unsafe_allow_html=True)
        fig_pie = backend.create_category_pie_chart(is_dark=is_dark)
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Visual Analytics Row 2: Monthly Comparison & Payment Method
    c3, c4 = st.columns([1.1, 0.9])
    with c3:
        st.markdown(f"""
        <div class="fintech-card">
            <div class="fintech-card-title">📅 Monthly Spending Trend Comparison</div>
        """, unsafe_allow_html=True)
        fig_trend = backend.create_monthly_trend_chart(is_dark=is_dark)
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c4:
        st.markdown(f"""
        <div class="fintech-card">
            <div class="fintech-card-title">💳 Payment Channels Breakdown</div>
        """, unsafe_allow_html=True)
        fig_pm = backend.create_payment_methods_chart(is_dark=is_dark)
        st.plotly_chart(fig_pm, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Detailed Category Matrix Breakdown Table
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">📋 Comprehensive Category Performance Matrix</div>
    """, unsafe_allow_html=True)
    
    breakdown = database.get_category_breakdown()
    if breakdown:
        df_mat = pd.DataFrame(breakdown)
        df_mat["Avg per Tx"] = df_mat["total"] / df_mat["count"]
        df_mat["total_formatted"] = df_mat["total"].apply(lambda x: f"₹{x:,.2f}")
        df_mat["avg_formatted"] = df_mat["Avg per Tx"].apply(lambda x: f"₹{x:,.2f}")
        df_mat["pct_formatted"] = df_mat["percentage"].apply(lambda x: f"{x:.1f}%")
        
        display_df = df_mat[["category", "total_formatted", "pct_formatted", "count", "avg_formatted"]].copy()
        display_df.columns = ["Category", "Total Spent", "% Share", "Transaction Count", "Average Ticket"]
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Anomaly / Top 5 Largest Expenditures
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">🔍 Top 5 Largest Expenditures (Outlier Detection)</div>
    """, unsafe_allow_html=True)
    
    top_5 = database.get_filtered_expenses(sort_by="amount_desc")[:5]
    if top_5:
        for idx, item in enumerate(top_5, 1):
            badge = styles.get_category_badge(item["category"])
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid {'rgba(255,255,255,0.06)' if is_dark else '#F1F5F9'};">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="font-weight: 800; color: #2563EB; font-size: 1rem;">#{idx}</div>
                    <div>{badge}</div>
                    <div>
                        <div style="font-weight: 600; font-size: 0.9rem; color: {'#F8FAFC' if is_dark else '#1E293B'};">{item['description'] or 'Expense'}</div>
                        <div style="font-size: 0.75rem; color: #94A3B8;">{item['date']} • Settled via {item.get('payment_method', 'UPI')}</div>
                    </div>
                </div>
                <div style="font-weight: 800; font-size: 1.05rem; color: #2563EB;">
                    ₹{item['amount']:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

