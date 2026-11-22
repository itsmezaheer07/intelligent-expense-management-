"""
Backend Logic & Analytics Module for Intelligent Expense Management System
Author: Zaheer Ansari (GUI Developer, BTech 1st Year AI & Data Science)
Description: Business logic layer connecting GUI views with database, handling
             validations, statistical aggregations, Plotly charts generation,
             AI financial insights, and export services.
"""

from datetime import datetime, date
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import database

# Fintech Color Palette
COLOR_PRIMARY = "#0B1220"
COLOR_SECONDARY = "#2563EB"
COLOR_SUCCESS = "#16A34A"
COLOR_DANGER = "#DC2626"
COLOR_ACCENT_PURPLE = "#8B5CF6"
COLOR_ACCENT_CYAN = "#06B6D4"
COLOR_ACCENT_ORANGE = "#F97316"
COLOR_ACCENT_PINK = "#EC4899"

FINTECH_PALETTE = [
    "#2563EB", "#06B6D4", "#F97316", "#8B5CF6",
    "#EC4899", "#10B981", "#F59E0B", "#6B7280"
]

def format_currency(amount: float, symbol: str = "₹") -> str:
    """Formats a float amount into Indian currency format with standard commas."""
    try:
        val = float(amount)
        # Format with Indian standard if practical or clean two decimal places
        return f"{symbol} {val:,.2f}"
    except (ValueError, TypeError):
        return f"{symbol} 0.00"

def get_dashboard_summary() -> Dict[str, Any]:
    """Retrieves all dashboard summary metrics from the database."""
    stats = database.get_statistics()
    budget_setting = database.get_setting("monthly_budget", "35000")
    try:
        monthly_budget = float(budget_setting)
    except ValueError:
        monthly_budget = 35000.0
        
    this_month_spent = stats["this_month_expenses"]
    budget_pct = (this_month_spent / monthly_budget * 100.0) if monthly_budget > 0 else 0.0
    budget_pct = round(budget_pct, 1)
    
    return {
        "total_expenses": stats["total_expenses"],
        "today_expenses": stats["today_expenses"],
        "this_month_expenses": this_month_spent,
        "total_transactions": stats["total_transactions"],
        "highest_category": stats["highest_category"],
        "highest_category_amount": stats["highest_category_amount"],
        "avg_transaction": stats["avg_transaction"],
        "monthly_budget": monthly_budget,
        "budget_percentage": budget_pct,
        "budget_remaining": max(0.0, monthly_budget - this_month_spent)
    }

def create_category_bar_chart(is_dark: bool = False) -> go.Figure:
    """
    Creates an interactive Category-wise Bar Chart using actual database records.
    """
    breakdown = database.get_category_breakdown()
    
    if not breakdown:
        fig = go.Figure()
        fig.add_annotation(
            text="No expense data recorded yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#94A3B8")
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=320,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        return fig
        
    df = pd.DataFrame(breakdown)
    df = df.sort_values(by="total", ascending=True)
    
    bg_paper = "rgba(0,0,0,0)"
    text_color = "#F8FAFC" if is_dark else "#0B1220"
    grid_color = "rgba(255,255,255,0.08)" if is_dark else "#E2E8F0"
    
    fig = go.Figure(go.Bar(
        x=df["total"],
        y=df["category"],
        orientation="h",
        marker=dict(
            color=df["total"],
            colorscale=[[0, "#93C5FD"], [1, "#2563EB"]],
            line=dict(color="#1D4ED8", width=1.5),
            cornerradius=6
        ),
        text=[f"₹{val:,.0f}" for val in df["total"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Spent: ₹%{x:,.2f}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>Spending by Category</b>",
            font=dict(size=15, color=text_color, family="Plus Jakarta Sans")
        ),
        paper_bgcolor=bg_paper,
        plot_bgcolor=bg_paper,
        height=320,
        margin=dict(l=10, r=40, t=40, b=20),
        xaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            zeroline=False,
            tickprefix="₹",
            tickfont=dict(color=text_color, size=11)
        ),
        yaxis=dict(
            tickfont=dict(color=text_color, size=12, family="Plus Jakarta Sans"),
            autorange="reversed"
        )
    )
    return fig

def create_category_pie_chart(is_dark: bool = False) -> go.Figure:
    """
    Creates an interactive Expense Distribution Donut Chart using actual database records.
    """
    breakdown = database.get_category_breakdown()
    
    if not breakdown:
        fig = go.Figure()
        fig.add_annotation(
            text="No expense data recorded yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#94A3B8")
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=320,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        return fig
        
    df = pd.DataFrame(breakdown)
    text_color = "#F8FAFC" if is_dark else "#0B1220"
    
    fig = go.Figure(go.Pie(
        labels=df["category"],
        values=df["total"],
        hole=0.6,
        marker=dict(colors=FINTECH_PALETTE, line=dict(color="#FFFFFF" if not is_dark else "#0B1220", width=2)),
        textinfo="percent+label",
        hoverinfo="label+value+percent",
        textposition="outside",
        hovertemplate="<b>%{label}</b><br>Total: ₹%{value:,.2f}<br>Share: %{percent}<extra></extra>"
    ))
    
    total_spent = df["total"].sum()
    
    fig.update_layout(
        title=dict(
            text="<b>Expense Distribution</b>",
            font=dict(size=15, color=text_color, family="Plus Jakarta Sans")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        annotations=[
            dict(
                text=f"<span style='font-size:11px;color:#94A3B8;'>TOTAL</span><br><b style='font-size:16px;color:{text_color}'>₹{total_spent:,.0f}</b>",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(family="Plus Jakarta Sans")
            )
        ]
    )
    return fig

def create_monthly_trend_chart(is_dark: bool = False) -> go.Figure:
    """
    Creates an interactive Monthly Spending Trend Chart using actual database records.
    """
    monthly_data = database.get_monthly_trend(limit_months=12)
    text_color = "#F8FAFC" if is_dark else "#0B1220"
    grid_color = "rgba(255,255,255,0.08)" if is_dark else "#E2E8F0"
    
    if not monthly_data:
        fig = go.Figure()
        fig.add_annotation(
            text="No trend data recorded yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#94A3B8")
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=300,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        return fig
        
    df = pd.DataFrame(monthly_data)
    
    # Format month names for friendly display (e.g. 2026-11 -> Nov 2026)
    def format_month(val):
        try:
            dt = datetime.strptime(val, "%Y-%m")
            return dt.strftime("%b %Y")
        except Exception:
            return val
            
    df["month_label"] = df["month"].apply(format_month)
    
    fig = go.Figure()
    
    # Spline Area fill
    fig.add_trace(go.Scatter(
        x=df["month_label"],
        y=df["total"],
        mode="lines+markers",
        line=dict(color="#2563EB", width=3, shape="spline"),
        marker=dict(size=8, color="#2563EB", line=dict(color="#FFFFFF", width=2)),
        fill="tozeroy",
        fillcolor="rgba(37, 99, 235, 0.12)",
        name="Spending",
        hovertemplate="<b>%{x}</b><br>Spent: ₹%{y:,.2f}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>Monthly Spending Trend</b>",
            font=dict(size=15, color=text_color, family="Plus Jakarta Sans")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color=text_color, size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            tickprefix="₹",
            tickfont=dict(color=text_color, size=11)
        )
    )
    return fig

def create_payment_methods_chart(is_dark: bool = False) -> go.Figure:
    """Creates a chart showing breakdown by payment method."""
    all_expenses = database.get_all_expenses()
    text_color = "#F8FAFC" if is_dark else "#0B1220"
    
    if not all_expenses:
        fig = go.Figure()
        fig.add_annotation(text="No transactions", showarrow=False)
        return fig
        
    df = pd.DataFrame(all_expenses)
    if "payment_method" not in df.columns or df["payment_method"].isnull().all():
        df["payment_method"] = "UPI"
    else:
        df["payment_method"] = df["payment_method"].fillna("UPI")
        
    pm_summary = df.groupby("payment_method")["amount"].agg(["sum", "count"]).reset_index()
    pm_summary.columns = ["Method", "Total", "Count"]
    
    fig = go.Figure(go.Pie(
        labels=pm_summary["Method"],
        values=pm_summary["Total"],
        hole=0.45,
        marker=dict(colors=["#06B6D4", "#2563EB", "#8B5CF6", "#10B981", "#F59E0B"]),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.2f} (%{percent})<extra></extra>"
    ))
    fig.update_layout(
        title=dict(text="<b>Payment Method Distribution</b>", font=dict(size=15, color=text_color)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(font=dict(color=text_color))
    )
    return fig

def generate_ai_insights() -> List[Dict[str, str]]:
    """
    Generates intelligent financial insights and recommendations based on
    actual spending patterns, category concentration, and budget adherence.
    """
    stats = database.get_statistics()
    breakdown = database.get_category_breakdown()
    budget_setting = float(database.get_setting("monthly_budget", "35000"))
    
    insights = []
    
    if stats["total_transactions"] == 0:
        insights.append({
            "type": "info",
            "icon": "💡",
            "title": "Welcome to Intelligent Expense Management",
            "text": "Start by adding your daily transactions to unlock automated categorization and AI spending trends."
        })
        return insights
        
    # Budget Insight
    month_spent = stats["this_month_expenses"]
    pct_used = (month_spent / budget_setting * 100.0) if budget_setting > 0 else 0
    if pct_used > 85.0:
        insights.append({
            "type": "danger",
            "icon": "⚠️",
            "title": f"Budget Warning: {pct_used:.1f}% Exhausted",
            "text": f"You have spent ₹{month_spent:,.0f} out of your ₹{budget_setting:,.0f} monthly budget. Consider curtailing discretionary spending."
        })
    elif pct_used > 60.0:
        insights.append({
            "type": "warning",
            "icon": "📊",
            "title": f"Moderate Spending: {pct_used:.1f}% of Budget Used",
            "text": f"You are pacing well within your ₹{budget_setting:,.0f} monthly limit with ₹{budget_setting - month_spent:,.0f} remaining."
        })
    else:
        insights.append({
            "type": "success",
            "icon": "✅",
            "title": "Healthy Financial Trajectory",
            "text": f"Your current monthly expenditure is well under control ({pct_used:.1f}% utilized)."
        })
        
    # Highest Category Insight
    if breakdown:
        top_cat = breakdown[0]
        if top_cat["percentage"] >= 30.0:
            insights.append({
                "type": "info",
                "icon": "🎯",
                "title": f"Dominant Category: {top_cat['category']} ({top_cat['percentage']}%)",
                "text": f"A significant portion (₹{top_cat['total']:,.0f}) of your total expenses is concentrated in {top_cat['category']} across {top_cat['count']} transactions."
            })
            
    # Transaction size insight
    if stats["avg_transaction"] > 0:
        insights.append({
            "type": "info",
            "icon": "💳",
            "title": f"Average Ticket Size: ₹{stats['avg_transaction']:,.0f}",
            "text": f"Across {stats['total_transactions']} recorded transactions, your average spend is ₹{stats['avg_transaction']:,.2f} per transaction."
        })
        
    return insights

def export_expenses_to_dataframe() -> pd.DataFrame:
    """Exports all expenses into a clean, presentation-ready Pandas DataFrame."""
    expenses = database.get_all_expenses()
    if not expenses:
        return pd.DataFrame(columns=["ID", "Date", "Category", "Description", "Payment Method", "Amount"])
        
    df = pd.DataFrame(expenses)
    df = df.rename(columns={
        "id": "ID",
        "date": "Date",
        "category": "Category",
        "description": "Description",
        "payment_method": "Payment Method",
        "amount": "Amount (₹)"
    })
    cols = ["ID", "Date", "Category", "Description", "Payment Method", "Amount (₹)"]
    existing_cols = [c for c in cols if c in df.columns]
    return df[existing_cols]

