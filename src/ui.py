import streamlit as st
import streamlit.components.v1 as components

def render_tailwind_header(title: str, subtitle: str, badge_text: str = "Active Production", badge_color: str = "bg-emerald-100 text-emerald-800"):
    """
    Renders an executive, responsive header banner using Tailwind CSS CDN inside an isolated iframe.
    """
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; background: transparent; }}
        </style>
    </head>
    <body class="p-1">
        <div class="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 rounded-2xl p-6 text-white shadow-xl border border-slate-800">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <div class="flex items-center gap-3">
                        <span class="p-2 bg-blue-600/30 rounded-lg border border-blue-500/30 text-blue-400">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                            </svg>
                        </span>
                        <h1 class="text-2xl font-bold tracking-tight text-white">{title}</h1>
                        <span class="text-xs font-semibold px-2.5 py-1 rounded-full {badge_color} border border-emerald-300/20">{badge_text}</span>
                    </div>
                    <p class="text-slate-300 text-sm mt-2 max-w-3xl leading-relaxed">{subtitle}</p>
                </div>
                <div class="hidden lg:flex items-center gap-2 text-xs text-slate-400 bg-slate-800/60 px-3 py-2 rounded-xl border border-slate-700/50">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>Live SQLite Analytics Data Mart</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=130)

def render_kpi_card(title: str, value: str, subtext: str, badge_text: str = "+0.0%", badge_color: str = "bg-slate-100 text-slate-700"):
    """
    Renders a single responsive Tailwind executive metric card.
    """
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; background: transparent; }}</style>
    </head>
    <body class="p-1">
        <div class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow p-5 border border-slate-200">
            <div class="flex justify-between items-start">
                <span class="text-xs font-semibold uppercase tracking-wider text-slate-500">{title}</span>
                <span class="text-xs font-bold px-2 py-0.5 rounded-full {badge_color}">{badge_text}</span>
            </div>
            <div class="text-2xl font-extrabold text-slate-900 mt-2 tracking-tight">{value}</div>
            <div class="text-xs font-medium text-slate-500 mt-1">{subtext}</div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=115)

def render_kpi_grid(kpis: list):
    """
    Renders 4 KPI cards in a unified responsive grid using Tailwind CSS.
    kpis: list of dicts with keys: ['title', 'value', 'subtext', 'badge_text', 'badge_color']
    """
    cards_html = ""
    for k in kpis:
        badge_cls = k.get("badge_color", "bg-slate-100 text-slate-700")
        b_text = k.get("badge_text", "")
        cards_html += f"""
        <div class="bg-white rounded-xl shadow-sm hover:shadow p-4 border border-slate-200">
            <div class="flex justify-between items-start">
                <span class="text-[11px] font-bold uppercase tracking-wider text-slate-500">{k['title']}</span>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded-full {badge_cls}">{b_text}</span>
            </div>
            <div class="text-2xl font-black text-slate-800 mt-2 tracking-tight">{k['value']}</div>
            <div class="text-xs text-slate-500 mt-1">{k['subtext']}</div>
        </div>
        """

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; background: transparent; }}</style>
    </head>
    <body class="p-1">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {cards_html}
        </div>
    </body>
    </html>
    """
    components.html(full_html, height=125)

def render_insight_box(title: str, text: str, category: str = "Info"):
    """
    Renders an analytical insight callout box with Tailwind styling.
    category: 'Success', 'Warning', 'Danger', 'Info'
    """
    styles = {
        "Success": ("bg-emerald-50 border-emerald-300 text-emerald-900", "text-emerald-700"),
        "Warning": ("bg-amber-50 border-amber-300 text-amber-900", "text-amber-700"),
        "Danger": ("bg-red-50 border-red-300 text-red-900", "text-red-700"),
        "Info": ("bg-blue-50 border-blue-300 text-blue-900", "text-blue-700")
    }
    box_cls, title_cls = styles.get(category, styles["Info"])

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; background: transparent; }}</style>
    </head>
    <body class="p-1">
        <div class="rounded-xl border p-4 {box_cls}">
            <div class="flex items-center gap-2 font-bold text-sm {title_cls}">
                <span>[Analytical Insight • {category.upper()}]</span>
                <span>{title}</span>
            </div>
            <div class="text-xs leading-relaxed mt-1 text-slate-700 font-medium">
                {text}
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=90)
