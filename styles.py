"""
Styles Module for Intelligent Expense Management System
Author: Zaheer Ansari (GUI Developer, BTech 1st Year AI & Data Science)
Description: Injects premium fintech SaaS CSS styling, typography, responsive card layouts,
             color systems (Light & Dark modes), status pills, and custom button themes.
"""

def get_theme_css(theme: str = "light") -> str:
    """
    Returns custom CSS tailored for the specified theme ('light' or 'dark').
    Adheres strictly to the fintech design palette:
      - Primary: Deep Navy Blue (#0B1220)
      - Secondary: Royal Blue (#2563EB)
      - Background: Light Gray (#F5F7FB) / Dark Slate (#0B1220)
      - Cards: White (#FFFFFF) / Slate (#1E293B)
      - Success: Green (#16A34A)
      - Danger: Red (#DC2626)
      - Text: Dark Slate (#1E293B) / Pure White (#F8FAFC)
    """
    is_dark = (theme.lower() == "dark")
    
    bg_color = "#0B1220" if is_dark else "#F5F7FB"
    card_bg = "#151F32" if is_dark else "#FFFFFF"
    card_border = "#26354D" if is_dark else "#E2E8F0"
    text_primary = "#F8FAFC" if is_dark else "#0B1220"
    text_secondary = "#94A3B8" if is_dark else "#64748B"
    sidebar_bg = "#070C16" if is_dark else "#0B1220"
    metric_border = "rgba(37, 99, 235, 0.2)" if is_dark else "#E2E8F0"
    hover_bg = "#1E2C44" if is_dark else "#F1F5F9"
    shadow_card = "0 4px 20px -2px rgba(0, 0, 0, 0.45)" if is_dark else "0 4px 20px -2px rgba(11, 18, 32, 0.06)"
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Base Styling */
    html, body, [class*="css"], .stApp {{
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: {bg_color} !important;
        color: {text_primary} !important;
    }}
    
    /* Hide Default Streamlit Clutter */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{background-color: transparent !important;}}
    
    /* Streamlit Main Container Spacing */
    .block-container {{
        padding-top: 1.8rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1250px !important;
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {{
        color: #F8FAFC !important;
    }}
    
    /* Premium Header / Banner */
    .fintech-header {{
        background: linear-gradient(135deg, #0B1220 0%, #172554 50%, #2563EB 100%);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        color: #FFFFFF !important;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.25);
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    .fintech-header h1 {{
        color: #FFFFFF !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: -0.02em;
    }}
    .fintech-header p {{
        color: #93C5FD !important;
        margin: 4px 0 0 0 !important;
        font-size: 0.95rem !important;
    }}
    
    /* Summary Metric Cards */
    .metric-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }}
    .metric-card {{
        background-color: {card_bg} !important;
        border: 1px solid {metric_border} !important;
        border-radius: 14px;
        padding: 20px;
        box-shadow: {shadow_card};
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        position: relative;
        overflow: hidden;
    }}
    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 28px -6px rgba(37, 99, 235, 0.18);
        border-color: #2563EB !important;
    }}
    .metric-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #2563EB, #60A5FA);
    }}
    .metric-card.success-accent::before {{
        background: linear-gradient(90deg, #16A34A, #4ADE80);
    }}
    .metric-card.warning-accent::before {{
        background: linear-gradient(90deg, #EAB308, #FDE047);
    }}
    .metric-card.purple-accent::before {{
        background: linear-gradient(90deg, #8B5CF6, #C084FC);
    }}
    .metric-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }}
    .metric-title {{
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {text_secondary};
    }}
    .metric-icon-wrap {{
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.15rem;
        background: rgba(37, 99, 235, 0.1);
        color: #2563EB;
    }}
    .metric-value {{
        font-size: 1.85rem;
        font-weight: 800;
        color: {text_primary};
        letter-spacing: -0.03em;
        margin-bottom: 6px;
    }}
    .metric-subtext {{
        font-size: 0.8rem;
        color: {text_secondary};
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    
    /* Standard Card Container */
    .fintech-card {{
        background-color: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: {shadow_card};
    }}
    .fintech-card-title {{
        font-size: 1.15rem;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    /* Category Badges */
    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }}
    .badge-food {{ background: rgba(249, 115, 22, 0.12); color: #EA580C; border: 1px solid rgba(249, 115, 22, 0.3); }}
    .badge-education {{ background: rgba(37, 99, 235, 0.12); color: #2563EB; border: 1px solid rgba(37, 99, 235, 0.3); }}
    .badge-transport {{ background: rgba(6, 182, 212, 0.12); color: #0891B2; border: 1px solid rgba(6, 182, 212, 0.3); }}
    .badge-shopping {{ background: rgba(236, 72, 153, 0.12); color: #DB2777; border: 1px solid rgba(236, 72, 153, 0.3); }}
    .badge-entertainment {{ background: rgba(139, 92, 246, 0.12); color: #7C3AED; border: 1px solid rgba(139, 92, 246, 0.3); }}
    .badge-healthcare {{ background: rgba(239, 68, 68, 0.12); color: #DC2626; border: 1px solid rgba(239, 68, 68, 0.3); }}
    .badge-bills {{ background: rgba(234, 179, 8, 0.12); color: #CA8A04; border: 1px solid rgba(234, 179, 8, 0.3); }}
    .badge-other {{ background: rgba(107, 114, 128, 0.12); color: #4B5563; border: 1px solid rgba(107, 114, 128, 0.3); }}
    
    /* Streamlit Buttons Customization */
    div.stButton > button {{
        background: linear-gradient(180deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.4rem !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.2s ease !important;
    }}
    div.stButton > button:hover {{
        background: linear-gradient(180deg, #1D4ED8 0%, #1E40AF 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
    }}
    div.stButton > button:active {{
        transform: translateY(0px) !important;
    }}
    
    /* Secondary and Danger buttons */
    button[kind="secondary"] {{
        background: {card_bg} !important;
        color: {text_primary} !important;
        border: 1px solid {card_border} !important;
        box-shadow: none !important;
    }}
    button[kind="secondary"]:hover {{
        background: {hover_bg} !important;
        border-color: #94A3B8 !important;
    }}
    
    /* Form Inputs */
    div[data-baseweb="input"] {{
        background-color: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
    }}
    div[data-baseweb="input"]:focus-within {{
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }}
    
    /* Budget Progress Indicator */
    .budget-bar-container {{
        background: {hover_bg};
        border-radius: 9999px;
        height: 10px;
        width: 100%;
        overflow: hidden;
        margin: 8px 0;
    }}
    .budget-bar-fill {{
        height: 100%;
        border-radius: 9999px;
        transition: width 0.4s ease;
    }}
    
    /* Empty State Container */
    .empty-state-box {{
        text-align: center;
        padding: 48px 24px;
        background: {card_bg};
        border: 2px dashed {card_border};
        border-radius: 16px;
        margin: 20px 0;
    }}
    .empty-state-icon {{
        font-size: 3rem;
        margin-bottom: 12px;
        opacity: 0.8;
    }}
    .empty-state-title {{
        font-size: 1.2rem;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 6px;
    }}
    .empty-state-text {{
        font-size: 0.9rem;
        color: {text_secondary};
        max-width: 400px;
        margin: 0 auto 16px auto;
    }}
    
    /* Navigation Sidebar Custom items */
    .nav-brand-title {{
        font-size: 1.25rem;
        font-weight: 800;
        color: #FFFFFF !important;
        display: flex;
        align-items: center;
        gap: 10px;
        letter-spacing: -0.02em;
        margin-bottom: 2px;
    }}
    .nav-brand-subtitle {{
        font-size: 0.75rem;
        color: #93C5FD !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 24px;
    }}
    .sidebar-user-card {{
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 14px;
        margin-top: 24px;
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .sidebar-user-avatar {{
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: linear-gradient(135deg, #2563EB, #8B5CF6);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
    }}
    
    /* Table Enhancements */
    div[data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid {card_border};
    }}
    </style>
    """
    return css

def render_metric_card(
    title: str,
    value: str,
    subtext: str,
    icon: str,
    accent: str = "primary"
) -> str:
    """
    Renders an HTML-based responsive SaaS fintech metric card with top border accent.
    """
    accent_class = ""
    if accent == "success":
        accent_class = "success-accent"
    elif accent == "warning":
        accent_class = "warning-accent"
    elif accent == "purple":
        accent_class = "purple-accent"
        
    html = f"""
    <div class="metric-card {accent_class}">
        <div class="metric-header">
            <span class="metric-title">{title}</span>
            <div class="metric-icon-wrap">{icon}</div>
        </div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtext">{subtext}</div>
    </div>
    """
    return html

def get_category_badge(category: str) -> str:
    """Returns an HTML badge for a category with appropriate color and icon."""
    cat_lower = category.lower().strip()
    badges = {
        "food": ('badge-food', '🍔'),
        "education": ('badge-education', '🎓'),
        "transport": ('badge-transport', '🚗'),
        "shopping": ('badge-shopping', '🛍️'),
        "entertainment": ('badge-entertainment', '🎬'),
        "healthcare": ('badge-healthcare', '🏥'),
        "bills": ('badge-bills', '💡'),
        "other": ('badge-other', '📦'),
    }
    badge_class, icon = badges.get(cat_lower, ('badge-other', '🏷️'))
    return f'<span class="badge {badge_class}">{icon} {category}</span>'

