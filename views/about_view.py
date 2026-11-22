"""
About Project View for Intelligent Expense Management System
Author: Zaheer Ansari (GUI Developer, BTech 1st Year AI & Data Science)
Description: Complete documentation and viva presentation showcase highlighting
             problem statement, project architecture, AI capabilities, and GUI engineering.
"""

import streamlit as st

def render_about(is_dark: bool = False):
    """Renders the comprehensive project showcase and documentation page."""
    st.markdown(f"""
    <div class="fintech-header">
        <div>
            <h1>About Project & Engineering Architecture</h1>
            <p>Intelligent Expense Management System • BTech 1st Year AI & Data Science Project</p>
        </div>
        <div>
            <span style="font-size: 2rem;">🎓</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview Card
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">💡 Executive Project Overview</div>
        <p style="color: {'#CBD5E1' if is_dark else '#334155'}; line-height: 1.6; font-size: 0.95rem;">
            The <b>Intelligent Expense Management System (IntelliSpend)</b> is a modern, fintech-grade personal finance and automated telemetry platform designed specifically for students, young professionals, and micro-organizations. It replaces error-prone manual spreadsheets with an interactive, reactive user interface powered by real-time SQLite persistence, dynamic Plotly visual analytics, and rule-based AI spending insight generation.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 3-Pillar Architecture Grid
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">🏛️ System Architecture & Modularity</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px;">
            <div style="background: {'#111C30' if is_dark else '#F8FAFC'}; border: 1px solid {'rgba(255,255,255,0.08)' if is_dark else '#E2E8F0'}; border-radius: 12px; padding: 16px;">
                <div style="font-size: 1.25rem; margin-bottom: 6px;">🖥️</div>
                <div style="font-weight: 700; color: {'#F8FAFC' if is_dark else '#0B1220'}; margin-bottom: 4px;">1. GUI & Presentation Layer</div>
                <p style="font-size: 0.82rem; color: {'#94A3B8' if is_dark else '#64748B'}; line-height: 1.4; margin: 0;">
                    Engineered by <b>Zaheer Ansari</b>. Built with custom CSS injection, Plus Jakarta Sans typography, reactive session state, instant form validation, and Light/Dark themes.
                </p>
            </div>
            <div style="background: {'#111C30' if is_dark else '#F8FAFC'}; border: 1px solid {'rgba(255,255,255,0.08)' if is_dark else '#E2E8F0'}; border-radius: 12px; padding: 16px;">
                <div style="font-size: 1.25rem; margin-bottom: 6px;">⚙️</div>
                <div style="font-weight: 700; color: {'#F8FAFC' if is_dark else '#0B1220'}; margin-bottom: 4px;">2. Business & Analytics Logic</div>
                <p style="font-size: 0.82rem; color: {'#94A3B8' if is_dark else '#64748B'}; line-height: 1.4; margin: 0;">
                    Orchestrates dynamic aggregation pipelines, Plotly vector charts (spline trends, donut distributions, category bars), and automated financial health audits.
                </p>
            </div>
            <div style="background: {'#111C30' if is_dark else '#F8FAFC'}; border: 1px solid {'rgba(255,255,255,0.08)' if is_dark else '#E2E8F0'}; border-radius: 12px; padding: 16px;">
                <div style="font-size: 1.25rem; margin-bottom: 6px;">🗄️</div>
                <div style="font-weight: 700; color: {'#F8FAFC' if is_dark else '#0B1220'}; margin-bottom: 4px;">3. Data Persistence Layer</div>
                <p style="font-size: 0.82rem; color: {'#94A3B8' if is_dark else '#64748B'}; line-height: 1.4; margin: 0;">
                    Thread-safe SQLite engine with atomic transactions, constraint validations (amount > 0, required fields), and instant CSV/JSON serialization.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # AI & Data Science Alignment Card
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">🤖 AI & Data Science Highlights</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; font-size: 0.88rem;">
            <div>
                <b style="color: #2563EB;">• Category Concentration Analysis:</b><br>
                <span style="color: {'#94A3B8' if is_dark else '#64748B'};">Calculates category entropy and flags single-category spending anomalies exceeding 30% of total outflow.</span>
            </div>
            <div>
                <b style="color: #2563EB;">• Burn Rate & Velocity Tracking:</b><br>
                <span style="color: {'#94A3B8' if is_dark else '#64748B'};">Evaluates monthly budget consumption speed against elapsed calendar days to predict end-of-month budget breaches.</span>
            </div>
            <div>
                <b style="color: #2563EB;">• Statistical Outlier Isolation:</b><br>
                <span style="color: {'#94A3B8' if is_dark else '#64748B'};">Automatically identifies top 5 high-ticket transactions that deviate significantly from the mean ticket size.</span>
            </div>
            <div>
                <b style="color: #2563EB;">• Payment Channel Modeling:</b><br>
                <span style="color: {'#94A3B8' if is_dark else '#64748B'};">Classifies liquidity preference across UPI, Card, Cash, and Net Banking channels.</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Student Presentation Credits
    st.markdown(f"""
    <div class="fintech-card">
        <div class="fintech-card-title">👨‍💻 Academic Project Credentials</div>
        <div style="border-left: 4px solid #2563EB; padding-left: 14px;">
            <div style="font-size: 1.1rem; font-weight: 700; color: {'#F8FAFC' if is_dark else '#0B1220'};">Zaheer Ansari</div>
            <div style="color: #2563EB; font-weight: 600; font-size: 0.9rem;">Lead GUI Developer & UI/UX Architect</div>
            <div style="color: {'#94A3B8' if is_dark else '#64748B'}; font-size: 0.85rem; margin-top: 4px;">
                BTech 1st Year • Department of Artificial Intelligence & Data Science<br>
                Intelligent Expense Management System Group Project
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

