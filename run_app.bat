@echo off
title Intelligent Expense Management System - IntelliSpend
echo =====================================================================
echo    INTELLIGENT EXPENSE MANAGEMENT SYSTEM (INTELLISPEND)
echo    Developer: Zaheer Ansari (BTech 1st Year AI & Data Science)
echo    Role: Lead GUI Developer
echo =====================================================================
echo.
echo Launching Streamlit Premium Fintech Interface...
echo Application URL: http://localhost:8501
echo.
set USERPROFILE=%CD%
python -m streamlit run app.py
pause
