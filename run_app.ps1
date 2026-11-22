# PowerShell launcher for Intelligent Expense Management System
# Developer: Zaheer Ansari (BTech 1st Year AI & Data Science)
# Role: Lead GUI Developer

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "   INTELLIGENT EXPENSE MANAGEMENT SYSTEM (INTELLISPEND)" -ForegroundColor Green
Write-Host "   Lead GUI Developer: Zaheer Ansari (BTech AI & DS)" -ForegroundColor Yellow
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Launching Streamlit application on http://localhost:8501..." -ForegroundColor White

$env:USERPROFILE = "$PWD"
python -m streamlit run app.py
