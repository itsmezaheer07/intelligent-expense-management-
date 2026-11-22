"""
Main Application Entrypoint for Intelligent Expense Management System
Author: Zaheer Ansari (GUI Developer, BTech 1st Year AI & Data Science)
Description: Orchestrates state management, theme injection, sidebar navigation,
             and dynamic page routing across all financial dashboard views.
"""

import streamlit as st
import database
import styles
from components.sidebar import render_sidebar
from views.dashboard_view import render_dashboard
from views.add_expense_view import render_add_expense
from views.history_view import render_history
from views.analytics_view import render_analytics
from views.settings_view import render_settings
from views.about_view import render_about

# 1. Page Configuration
st.set_page_config(
    page_title="IntelliSpend - Intelligent Expense Management System",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Database Initialization
database.init_db(seed_if_empty=True)

# 3. Theme & Session State Setup
if "app_theme" not in st.session_state:
    st.session_state.app_theme = database.get_setting("theme", "light")
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

theme = st.session_state.app_theme
is_dark = (theme == "dark")

# 4. Inject Premium Fintech CSS Styling
st.markdown(styles.get_theme_css(theme), unsafe_allow_html=True)

# 5. Render Sidebar Navigation
render_sidebar()

# 6. Page Routing
current_view = st.session_state.current_page

if current_view == "Dashboard":
    render_dashboard(is_dark=is_dark)
elif current_view == "Add Expense":
    render_add_expense(is_dark=is_dark)
elif current_view == "Expense History":
    render_history(is_dark=is_dark)
elif current_view == "Analytics":
    render_analytics(is_dark=is_dark)
elif current_view == "Settings":
    render_settings(is_dark=is_dark)
elif current_view == "About Project":
    render_about(is_dark=is_dark)
else:
    render_dashboard(is_dark=is_dark)

