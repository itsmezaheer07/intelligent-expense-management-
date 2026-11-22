@echo off
title Push IntelliSpend to GitHub
echo =====================================================================
echo    PUSHING INTELLIGENT EXPENSE MANAGEMENT TO GITHUB
echo    Repository: https://github.com/itsmezaheer07/intelligent-expense-management-.git
echo =====================================================================
echo.
set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%PATH%"
git config http.schannelCheckRevoke false
echo Running: git push -u origin main
echo (If prompted, sign in via your browser)
echo.
git push -u origin main
echo.
pause
