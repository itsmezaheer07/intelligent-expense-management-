# 💳 Intelligent Expense Management System (IntelliSpend)

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.15-blue.svg)](https://python.org)
[![Streamlit Framework](https://img.shields.io/badge/Streamlit-1.66-FF4B4B.svg)](https://streamlit.io)
[![Plotly Interactive](https://img.shields.io/badge/Plotly-Interactive%20Charts-brightgreen.svg)](https://plotly.com)
[![License](https://img.shields.io/badge/Academic-BTech%20Project-orange.svg)]()

> **Premium Fintech Desktop & Web Application** designed for the **Intelligent Expense Management System** group project. Built to enterprise SaaS standards by **Zaheer Ansari**, Lead GUI Developer & UI/UX Architect (BTech 1st Year, Artificial Intelligence & Data Science).

---

## 🌟 Executive Overview

**IntelliSpend** transforms mundane college expense tracking into a modern, fintech-grade personal finance dashboard. Engineered with **Streamlit**, **Plotly**, and **SQLite**, it provides real-time transaction telemetry, statistical categorization, interactive visual analytics, and reactive input validation.

### 🎨 Design Philosophy & Color Palette
Designed according to modern SaaS fintech principles (Stripe/Revolut aesthetics):
- **Primary Navy:** `#0B1220` (Deep authoritative foundation)
- **Secondary Royal Blue:** `#2563EB` (Interactive elements & primary actions)
- **Background:** `#F5F7FB` (Light Mode) / `#0B1220` (Dark Mode)
- **Cards & Surfaces:** `#FFFFFF` (Light) / `#151F32` (Dark)
- **Status Accents:** Success Green (`#16A34A`), Danger Red (`#DC2626`), Warning Yellow (`#EAB308`)
- **Typography:** Plus Jakarta Sans & Inter with strict visual hierarchy and elevation shadows.

---

## 🏛️ Project Architecture & File Structure

```
intelligent-expense-management/
├── .streamlit/
│   ├── config.toml           # Theme defaults, headless port, telemetry toggle
│   └── credentials.toml      # Local zero-friction activation
├── assets/                   # Static assets and icons
├── components/
│   ├── __init__.py
│   └── sidebar.py            # Persistent branded fintech sidebar & user badge
├── data/
│   └── expense_database.db   # SQLite relational database
├── views/
│   ├── __init__.py
│   ├── dashboard_view.py     # 4 KPI cards, 3 Plotly charts, budget progress, AI insights
│   ├── add_expense_view.py   # Strict form validation, 8 categories, 5 payment channels
│   ├── history_view.py       # Live search, filters, sorting, inline edit, delete confirmation
│   ├── analytics_view.py     # Deep statistical breakdown, payment donut, outlier analysis
│   ├── settings_view.py      # Light/Dark toggle, currency, budget limits, data studio
│   └── about_view.py         # Academic viva showcase, AI & DS project perspective
├── app.py                    # Application orchestration & reactive router
├── backend.py                # Business logic, aggregations, Plotly charts, AI engine
├── database.py               # Thread-safe SQLite database manager with context handling
├── styles.py                 # Custom CSS injection engine (Light & Dark modes)
├── test_app.py               # 12-test automated unit and integration suite
├── requirements.txt          # Python dependencies
├── run_app.bat               # Windows 1-click batch launcher
├── run_app.ps1               # PowerShell 1-click launcher
└── README.md                 # Complete documentation & viva presentation guide
```

---

## ✨ Features Breakdown

### 1. 📊 Executive Dashboard
- **4 Dynamic KPI Cards:**
  1. **Total Expenses** (Lifetime cumulative spending with transaction count)
  2. **Today's Expenses** (Day-to-day burn rate telemetry)
  3. **This Month's Expenses** (Pacing against monthly target)
  4. **Total Transactions** (Ticket volume & average transaction size)
- **Interactive Plotly Visualizations:**
  - **Category Breakdown:** Horizontal bar chart with royal blue gradient and ₹ tooltips.
  - **Expense Distribution:** 3D-styled donut chart with center total callout.
  - **Monthly Spending Trajectory:** Spline line area chart showing multi-month trends.
- **Budget Progress Indicator:** Live progress bar transitioning Green ➔ Yellow ➔ Red based on percentage utilized.
- **Recent Transactions Ledger:** 5 latest expenses with custom category pill badges.
- **AI & Analytics Insight Banners:** Dynamic alerts highlighting dominant categories and spending velocity.

### 2. ➕ Add Expense Form
- **Form Fields:** Amount (₹), Category, Date, Description, Payment Method.
- **Categories:** Food 🍔, Education 🎓, Transport 🚗, Shopping 🛍️, Entertainment 🎬, Healthcare 🏥, Bills 💡, Other 📦.
- **Payment Methods:** UPI, Credit Card, Debit Card, Cash, Net Banking.
- **Input Validation Rules:**
  - Amount cannot be empty or zero (`amount > 0`).
  - Negative amounts are rejected with descriptive alerts.
  - Category is mandatory.
  - Date is validated.
  - Safe sanitization of descriptions.
- **Actions:** Add Expense (Primary), Reset Form (Secondary), Cancel (Return to Dashboard).
- **Post-Submission:** Instant database persistence, success banner with ID, and reactive telemetry update.

### 3. 📜 Expense History & Audit Ledger
- **Live Search:** Instant filtering across descriptions, categories, payment methods, and amount.
- **Multi-Factor Filtering:** Filter by Category (`All Categories` or specific) and Date Range (`All Time`, `Today`, `Last 7 Days`, `This Month`, `Custom Range`).
- **Sorting Options:** Newest First, Oldest First, Highest Amount, Lowest Amount.
- **Inline Editing:** Edit amount, category, date, description, or payment method with one click.
- **Safe Deletion:** Pop-up confirmation dialog prevents accidental data loss.
- **Friendly Empty State:** Displays a modern illustration and prompt when zero records match.
- **One-Click Export:** Download filtered table as CSV.

### 4. 📈 Analytics & AI Insights
- **Key Financial Ratios:** Total Spend, Top Category, Average Ticket, Transaction Count.
- **Category Performance Matrix:** Full tabular breakdown showing Total, % Share, Count, and Average Ticket per category.
- **Payment Method Share:** Donut visualization identifying liquidity preference (UPI vs Cards vs Cash).
- **Outlier Detection:** Top 5 largest historical expenditures highlighted for budget audits.

### 5. ⚙️ Settings & Data Operations
- **Theme Switcher:** Seamlessly toggle between **Light Mode** and **Dark Mode**.
- **Currency Configuration:** Default INR (`₹`) with international currency options.
- **Monthly Budget Ceiling:** Dynamically adjust budget targets for alert thresholds.
- **Data Management Studio:**
  - Export Full Ledger as CSV
  - Export Database as JSON
  - Load Realistic Demo Dataset (seeds 18 varied student transactions in 1 click)
  - Wipe / Clear All Records (with double-confirmation safety guard)

### 6. ℹ️ Academic About & Viva Showcase
- Detailed architectural breakdown for college viva evaluations.
- Presentation of student developer credentials: **Zaheer Ansari (BTech 1st Year AI & DS)**.

---

## 🚀 How to Run the Project in VS Code

### Prerequisites
- Python 3.10+ (Python 3.15 supported)
- Visual Studio Code

### Step-by-Step Instructions

1. **Open the Project Folder in VS Code:**
   - Launch VS Code.
   - Click `File` ➔ `Open Folder...`.
   - Select: `c:\Users\SK\Desktop\intelligent expence management`.

2. **Open the Integrated Terminal:**
   - Press ``Ctrl + ` `` (Backtick) or click `Terminal` ➔ `New Terminal`.

3. **Install Dependencies (if not already installed):**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Application:**
   - **Method A (Direct Command):**
     ```powershell
     $env:USERPROFILE = "$PWD"
     python -m streamlit run app.py
     ```
   - **Method B (PowerShell Script):**
     ```powershell
     .\run_app.ps1
     ```
   - **Method C (Windows Batch File):**
     Double-click `run_app.bat` or run:
     ```cmd
     run_app.bat
     ```

5. **Access the Application:**
   Open your browser to:
   ```
   http://localhost:8501
   ```

---

## 🧪 Automated Testing & Verification

The project includes an automated test suite verifying database operations, constraints, validation, statistics, and charts.

To run the test suite:
```bash
python test_app.py
```

**Expected Output:**
```
Ran 12 tests in 0.35s
OK
```

---

## 🎓 Academic Viva Questions & Answers (For Project Presentation)

| Question | Answer |
| :--- | :--- |
| **Why choose Streamlit for this project?** | Streamlit enables a reactive, data-driven web GUI in pure Python with stateful reruns, native Plotly chart embedding, and responsive CSS injection—delivering a fintech SaaS aesthetic far superior to basic Tkinter. |
| **How does the GUI communicate with the backend?** | The GUI invokes modular functions in `backend.py` and `database.py`. The database layer uses SQLite with connection pooling context managers, ensuring thread safety and ACID transactions. |
| **How is form validation handled?** | Both client-level and database-level constraints are enforced: amounts must be strictly $> 0$, categories cannot be empty, dates must be valid ISO strings, and descriptions are sanitized. |
| **Where does the AI/Data Science aspect apply?** | Automated spending category distribution, budget burn velocity prediction, single-category concentration anomaly warnings ($>30\%$), and top outlier expense tracking. |

---

## 👨‍💻 Project Credits

- **Role:** Lead GUI Developer & UI/UX Architect
- **Student Name:** Zaheer Ansari
- **Program:** BTech 1st Year, Department of Artificial Intelligence & Data Science
- **Project:** Intelligent Expense Management System
- **Version:** 2.4.0 (Enterprise Fintech Edition)

