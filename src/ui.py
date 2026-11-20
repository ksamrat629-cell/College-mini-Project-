import textwrap
import streamlit as st
import streamlit.components.v1 as components

def apply_custom_css():
    """
    Injects executive-grade modern CSS into the Streamlit DOM.
    Features:
    - Google Fonts (Plus Jakarta Sans, Inter, JetBrains Mono)
    - Dark Navy Executive Sidebar with Glowing Status Indicators
    - Modern Glassmorphism Cards, Hover Transitions, and Micro-interactions
    - Polished Tab Navigation, Buttons, Metric Badges, and Alert Banners
    """
    custom_css = textwrap.dedent("""
    <style>
    /* 1. Global Typography & Canvas */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #0F172A;
    }

    /* Main Container Padding & Clean Canvas */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 96% !important;
    }

    /* 2. Executive Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #09122C 0%, #111A35 40%, #0F172A 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    /* Sidebar Divider & Badges */
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
        margin: 1.25rem 0 !important;
    }

    /* Sidebar Multiselect & Selectboxes */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #1E3A8A !important;
        color: #93C5FD !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 11px !important;
    }

    /* 3. Modern Metric Cards & Hover Effects */
    .metro-kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 16px 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .metro-kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 24px -6px rgba(15, 23, 42, 0.12), 0 6px 10px -4px rgba(15, 23, 42, 0.08);
        border-color: #CBD5E1;
    }

    .metro-kpi-accent {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }

    /* Accent color variants */
    .accent-blue { background: linear-gradient(90deg, #2563EB, #60A5FA); }
    .accent-emerald { background: linear-gradient(90deg, #059669, #34D399); }
    .accent-amber { background: linear-gradient(90deg, #D97706, #FBBF24); }
    .accent-rose { background: linear-gradient(90deg, #DC2626, #F87171); }
    .accent-purple { background: linear-gradient(90deg, #7C3AED, #A78BFA); }

    /* 4. Styled Navigation Cards */
    .nav-module-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 2px 5px rgba(0,0,0,0.04);
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }

    .nav-module-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 20px -4px rgba(37, 99, 235, 0.12);
        border-color: #93C5FD;
    }

    /* 5. Custom Styled Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F1F5F9;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px !important;
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 0 18px !important;
        border: none !important;
        background-color: transparent !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.6) !important;
        color: #1E293B !important;
    }

    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #1E40AF !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    }

    /* 6. Styled Buttons & Micro-Interactions */
    .stButton > button {
        background: linear-gradient(135deg, #1E40AF 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.25rem !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: 0.01em !important;
        box-shadow: 0 4px 10px -2px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px -2px rgba(37, 99, 235, 0.45) !important;
        color: #FFFFFF !important;
    }

    /* 7. Live System Status Bar Ticker */
    .system-status-ticker {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 10px 18px;
        margin: 12px 0 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        display: inline-block;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse-ring 2s infinite;
    }

    @keyframes pulse-ring {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* 8. Dataframe Tables Modernization */
    [data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    </style>
    """).strip()
    st.markdown(custom_css, unsafe_allow_html=True)


def render_tailwind_header(title: str, subtitle: str, badge_text: str = "Active Production", badge_color: str = "bg-emerald-100 text-emerald-800"):
    """
    Renders an executive, responsive header banner using an elegant gradient mesh,
    animated heartbeat pulse glow, and live system metadata tags.
    Also automatically injects custom global CSS into the Streamlit session.
    """
    # 1. Apply global custom CSS automatically
    apply_custom_css()

    # 2. Render modern responsive header container with zero-indent dedent
    header_html = textwrap.dedent(f"""
    <div style="
        background: linear-gradient(135deg, #09122C 0%, #171E36 45%, #0F172A 100%);
        border-radius: 18px;
        padding: 24px 28px;
        color: #FFFFFF;
        box-shadow: 0 12px 30px -8px rgba(9, 18, 44, 0.35), 0 4px 12px -2px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    ">
        <!-- Background Ambient Glow -->
        <div style="
            position: absolute;
            top: -60px;
            right: -60px;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(37, 99, 235, 0.25) 0%, rgba(37, 99, 235, 0) 70%);
            border-radius: 50%;
            pointer-events: none;
        "></div>

        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px; position: relative; z-index: 2;">
            <div>
                <!-- Institutional Breadcrumbs -->
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #60A5FA;">
                        MetroCare Health Systems
                    </span>
                    <span style="color: rgba(255, 255, 255, 0.3);">•</span>
                    <span style="font-size: 11px; font-weight: 600; color: #94A3B8;">
                        Delhi NCR Tertiary Care (450 Beds)
                    </span>
                    <span style="color: rgba(255, 255, 255, 0.3);">•</span>
                    <span style="font-size: 11px; font-weight: 600; color: #A7F3D0;">
                        ABES MCA Capstone 2026
                    </span>
                </div>

                <!-- Title & Badge -->
                <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
                    <div style="
                        width: 42px;
                        height: 42px;
                        border-radius: 12px;
                        background: linear-gradient(135deg, #1E40AF, #3B82F6);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
                        font-size: 20px;
                    ">
                        🏥
                    </div>
                    <h1 style="margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.02em; color: #FFFFFF; font-family: 'Plus Jakarta Sans', sans-serif;">
                        {title}
                    </h1>
                    <span style="
                        font-size: 11px;
                        font-weight: 700;
                        padding: 4px 12px;
                        border-radius: 20px;
                        background: rgba(16, 185, 129, 0.18);
                        color: #34D399;
                        border: 1px solid rgba(52, 211, 153, 0.3);
                        display: inline-flex;
                        align-items: center;
                        gap: 6px;
                    ">
                        <span class="pulse-dot"></span>
                        {badge_text}
                    </span>
                </div>

                <!-- Subtitle -->
                <p style="margin: 8px 0 0 0; color: #CBD5E1; font-size: 13.5px; font-weight: 400; max-width: 820px; line-height: 1.5;">
                    {subtitle}
                </p>
            </div>

            <!-- Header System Metadata Ticker -->
            <div style="
                display: flex;
                flex-direction: column;
                gap: 6px;
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 11.5px;
                min-width: 200px;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; color: #94A3B8;">
                    <span>Analytics Engine:</span>
                    <strong style="color: #60A5FA;">SQLite3 ACID</strong>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; color: #94A3B8;">
                    <span>Rule-01 Quarantine:</span>
                    <strong style="color: #34D399;">Active & Audited</strong>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; color: #94A3B8;">
                    <span>Query Latency:</span>
                    <strong style="color: #FBBF24;">&lt; 15 ms</strong>
                </div>
            </div>
        </div>
    </div>
    """).strip()
    st.markdown(header_html, unsafe_allow_html=True)


def render_kpi_card(title: str, value: str, subtext: str, badge_text: str = "+0.0%", badge_color: str = "bg-slate-100 text-slate-700"):
    """
    Renders a single responsive modern executive metric card with top accent styling.
    """
    # Pick accent color based on badge text or title
    accent_class = "accent-blue"
    if "breach" in title.lower() or "breach" in badge_text.lower() or "risk" in badge_text.lower() or "danger" in badge_color.lower() or "red" in badge_color.lower():
        accent_class = "accent-rose"
    elif "compliant" in badge_text.lower() or "normal" in badge_text.lower() or "emerald" in badge_color.lower():
        accent_class = "accent-emerald"
    elif "warning" in badge_color.lower() or "amber" in badge_color.lower():
        accent_class = "accent-amber"
    elif "revenue" in title.lower() or "csat" in title.lower() or "purple" in badge_color.lower():
        accent_class = "accent-purple"

    card_html = textwrap.dedent(f"""
    <div class="metro-kpi-card">
        <div class="metro-kpi-accent {accent_class}"></div>
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px;">
            <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #64748B;">
                {title}
            </span>
            <span style="
                font-size: 10.5px;
                font-weight: 700;
                padding: 2px 8px;
                border-radius: 12px;
                background: #F1F5F9;
                color: #334155;
                white-space: nowrap;
            ">
                {badge_text}
            </span>
        </div>
        <div style="font-size: 26px; font-weight: 800; color: #0F172A; margin-top: 8px; letter-spacing: -0.03em; font-family: 'Plus Jakarta Sans', sans-serif;">
            {value}
        </div>
        <div style="font-size: 12px; font-weight: 500; color: #64748B; margin-top: 4px;">
            {subtext}
        </div>
    </div>
    """).strip()
    st.markdown(card_html, unsafe_allow_html=True)


def render_kpi_grid(kpis: list):
    """
    Renders 4 KPI cards in a unified responsive grid using Streamlit native columns
    and custom styled HTML cards for zero layout jitter.
    kpis: list of dicts with keys: ['title', 'value', 'subtext', 'badge_text', 'badge_color']
    """
    cols = st.columns(len(kpis))
    for idx, (col, k) in enumerate(zip(cols, kpis)):
        with col:
            # Determine color theme
            b_text = k.get("badge_text", "")
            title = k.get("title", "")
            val = k.get("value", "")
            sub = k.get("subtext", "")

            # Choose accent strip
            if idx == 0:
                accent = "accent-blue"
                pill_bg = "#EFF6FF"
                pill_fg = "#1D4ED8"
                pill_border = "#BFDBFE"
                icon = "📊"
            elif idx == 1:
                if "breach" in b_text.lower() or "high" in b_text.lower():
                    accent = "accent-rose"
                    pill_bg = "#FEF2F2"
                    pill_fg = "#B91C1C"
                    pill_border = "#FECACA"
                else:
                    accent = "accent-emerald"
                    pill_bg = "#ECFDF5"
                    pill_fg = "#047857"
                    pill_border = "#A7F3D0"
                icon = "⏱️"
            elif idx == 2:
                if "high" in b_text.lower() or "risk" in b_text.lower():
                    accent = "accent-amber"
                    pill_bg = "#FFFBEB"
                    pill_fg = "#B45309"
                    pill_border = "#FDE68A"
                else:
                    accent = "accent-emerald"
                    pill_bg = "#ECFDF5"
                    pill_fg = "#047857"
                    pill_border = "#A7F3D0"
                icon = "📅"
            else:
                accent = "accent-purple"
                pill_bg = "#F5F3FF"
                pill_fg = "#6D28D9"
                pill_border = "#DDD6FE"
                icon = "⭐"

            card_html = textwrap.dedent(f"""
            <div class="metro-kpi-card" style="margin-bottom: 16px;">
                <div class="metro-kpi-accent {accent}"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; gap: 8px;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="font-size: 14px;">{icon}</span>
                        <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B;">
                            {title}
                        </span>
                    </div>
                    <span style="
                        font-size: 10px;
                        font-weight: 700;
                        padding: 3px 8px;
                        border-radius: 12px;
                        background: {pill_bg};
                        color: {pill_fg};
                        border: 1px solid {pill_border};
                        white-space: nowrap;
                    ">
                        {b_text}
                    </span>
                </div>
                <div style="font-size: 26px; font-weight: 800; color: #0F172A; margin-top: 10px; letter-spacing: -0.03em;">
                    {val}
                </div>
                <div style="font-size: 11.5px; font-weight: 500; color: #64748B; margin-top: 4px; line-height: 1.3;">
                    {sub}
                </div>
            </div>
            """).strip()
            st.markdown(card_html, unsafe_allow_html=True)


def render_insight_box(title: str, text: str, category: str = "Info"):
    """
    Renders a high-contrast analytical insight callout box with modern left border accent.
    category: 'Success', 'Warning', 'Danger', 'Info'
    """
    styles = {
        "Success": {
            "bg": "#F0FDF4",
            "border": "#22C55E",
            "title_color": "#15803D",
            "tag_bg": "#DCFCE7",
            "tag_color": "#166534",
            "icon": "✅"
        },
        "Warning": {
            "bg": "#FFFBEB",
            "border": "#F59E0B",
            "title_color": "#B45309",
            "tag_bg": "#FEF3C7",
            "tag_color": "#92400E",
            "icon": "⚠️"
        },
        "Danger": {
            "bg": "#FEF2F2",
            "border": "#EF4444",
            "title_color": "#B91C1C",
            "tag_bg": "#FEE2E2",
            "tag_color": "#991B1B",
            "icon": "🚨"
        },
        "Info": {
            "bg": "#EFF6FF",
            "border": "#3B82F6",
            "title_color": "#1D4ED8",
            "tag_bg": "#DBEAFE",
            "tag_color": "#1E40AF",
            "icon": "💡"
        }
    }
    cfg = styles.get(category, styles["Info"])

    html_code = textwrap.dedent(f"""
    <div style="
        background-color: {cfg['bg']};
        border: 1px solid {cfg['border']}40;
        border-left: 5px solid {cfg['border']};
        border-radius: 12px;
        padding: 14px 18px;
        margin: 12px 0 18px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 16px;">{cfg['icon']}</span>
                <span style="font-weight: 700; font-size: 13.5px; color: {cfg['title_color']}; font-family: 'Plus Jakarta Sans', sans-serif;">
                    {title}
                </span>
            </div>
            <span style="
                font-size: 10px;
                font-weight: 700;
                padding: 2px 8px;
                border-radius: 6px;
                background-color: {cfg['tag_bg']};
                color: {cfg['tag_color']};
                text-transform: uppercase;
                letter-spacing: 0.05em;
            ">
                ANALYTICAL INSIGHT • {category}
            </span>
        </div>
        <div style="font-size: 12.5px; color: #334155; margin-top: 6px; line-height: 1.5; font-weight: 500;">
            {text}
        </div>
    </div>
    """).strip()
    st.markdown(html_code, unsafe_allow_html=True)


def apply_plotly_theme(fig, title: str = None, height: int = 380):
    """
    Applies the MetroCare executive design language to any Plotly chart:
    - Transparent plot and canvas background
    - Elegant typography (Plus Jakarta Sans)
    - Soft slate gridlines (#E2E8F0)
    - Rounded bar corners and enhanced tooltips
    """
    if fig is None:
        return fig

    layout_updates = {
        "font": {"family": "Plus Jakarta Sans, Inter, sans-serif", "color": "#1E293B"},
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "margin": dict(l=30, r=20, t=50 if title else 20, b=30),
        "height": height,
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "bgcolor": "rgba(255,255,255,0.8)",
            "bordercolor": "#E2E8F0",
            "borderwidth": 1
        },
        "hoverlabel": {
            "bgcolor": "#0F172A",
            "font_size": 12,
            "font_family": "Plus Jakarta Sans, sans-serif",
            "font_color": "#FFFFFF",
            "bordercolor": "#334155"
        }
    }

    if title:
        layout_updates["title"] = {
            "text": title,
            "font": {"size": 15, "weight": 700, "color": "#0F172A"},
            "x": 0.02,
            "y": 0.96
        }

    fig.update_layout(**layout_updates)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#F1F5F9", zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#F1F5F9", zeroline=False)

    return fig
