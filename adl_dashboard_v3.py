"""
ADL Intelligence Dashboard v3
Team 15 — Productivity Pioneers | Hult MBA Capstone 2026
Built by Husna Rafi for Arthur D. Little
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import time

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ADL Intelligence — Executive Dashboard",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── COLOUR SYSTEM ───────────────────────────────────────────────────────────
C = {
    "bg":       "#050E1A",   # deepest background
    "surface":  "#0D1E35",   # card surface
    "navy":     "#112240",   # elevated card
    "border":   "#1E3A5F",   # border / divider
    "blue":     "#2563EB",   # primary accent
    "blue2":    "#3B82F6",   # lighter blue
    "gold":     "#D97706",   # key highlight — use sparingly
    "goldl":    "#FEF3C7",   # gold background tint
    "white":    "#F8FAFC",   # primary text
    "silver":   "#94A3B8",   # secondary text
    "muted":    "#475569",   # tertiary text
    "green":    "#10B981",   # positive / success
    "greenl":   "#D1FAE5",   # green bg tint
    "red":      "#EF4444",   # negative / risk
    "redl":     "#FEE2E2",   # red bg tint
    "teal":     "#06B6D4",   # info accent
    "teall":    "#CFFAFE",   # teal bg tint
    "amber":    "#F59E0B",   # medium severity
    "amberl":   "#FEF3C7",   # amber bg tint
    "glass":    "rgba(30,58,95,0.5)",   # glassmorphism surface
}

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {{ font-family: 'Inter', sans-serif !important; box-sizing: border-box; }}

.stApp {{ background: linear-gradient(135deg, {C['bg']} 0%, #071828 50%, {C['bg']} 100%); }}
.stApp > header {{ background: transparent; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {C['surface']} 0%, {C['bg']} 100%);
    border-right: 1px solid {C['border']};
}}
[data-testid="stSidebar"] * {{ color: {C['silver']}; }}

/* Metric cards - glassmorphism */
[data-testid="metric-container"] {{
    background: {C['glass']};
    border: 1px solid {C['border']};
    border-radius: 12px;
    padding: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
[data-testid="metric-container"]:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(37,99,235,0.2), inset 0 1px 0 rgba(255,255,255,0.08);
    border-color: {C['blue']};
}}
[data-testid="metric-container"] label {{
    color: {C['silver']} !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color: {C['gold']} !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
}}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
    color: {C['green']} !important;
    font-size: 12px !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    background: {C['surface']};
    border-radius: 10px;
    border: 1px solid {C['border']};
    padding: 4px;
    gap: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    color: {C['silver']};
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    padding: 8px 16px;
    transition: all 0.2s;
}}
.stTabs [data-baseweb="tab"][aria-selected="true"] {{
    background: {C['blue']};
    color: {C['white']};
}}

/* Text */
h1 {{ color: {C['white']} !important; font-weight: 800 !important; letter-spacing: -1px !important; }}
h2 {{ color: {C['white']} !important; font-weight: 700 !important; letter-spacing: -0.5px !important; }}
h3 {{ color: {C['white']} !important; font-weight: 600 !important; }}
p  {{ color: {C['silver']}; line-height: 1.7; font-size: 14px; }}

/* Expander */
div[data-testid="stExpander"] {{
    background: {C['surface']};
    border: 1px solid {C['border']};
    border-radius: 10px;
}}
div[data-testid="stExpander"] summary {{
    color: {C['silver']};
    font-size: 13px;
    font-weight: 500;
}}

/* Selectbox / slider */
div[data-baseweb="select"] > div {{
    background: {C['surface']};
    border-color: {C['border']};
    color: {C['white']};
}}
div[data-baseweb="select"] span {{ color: {C['white']}; }}
.stSlider [data-testid="stTickBar"] {{ color: {C['silver']}; }}

/* Custom components */
.glass-card {{
    background: {C['glass']};
    border: 1px solid {C['border']};
    border-radius: 14px;
    padding: 20px 24px;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
    margin: 8px 0;
}}
.glass-card:hover {{
    border-color: {C['blue2']};
    box-shadow: 0 6px 32px rgba(37,99,235,0.15);
    transition: all 0.25s ease;
}}
.exec-banner {{
    background: linear-gradient(135deg, rgba(37,99,235,0.15) 0%, rgba(6,182,212,0.08) 100%);
    border: 1px solid rgba(37,99,235,0.3);
    border-left: 4px solid {C['blue']};
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin: 12px 0 20px 0;
}}
.exec-banner p {{ color: {C['white']}; font-size: 15px; font-weight: 500; line-height: 1.6; margin: 0; }}
.insight-gold {{
    background: rgba(217,119,6,0.08);
    border: 1px solid rgba(217,119,6,0.25);
    border-left: 4px solid {C['gold']};
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 10px 0;
    color: {C['silver']};
    font-size: 13px;
    line-height: 1.6;
}}
.insight-green {{
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.2);
    border-left: 4px solid {C['green']};
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 10px 0;
    color: {C['silver']};
    font-size: 13px;
    line-height: 1.6;
}}
.insight-red {{
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.2);
    border-left: 4px solid {C['red']};
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 10px 0;
    color: {C['silver']};
    font-size: 13px;
    line-height: 1.6;
}}
.section-label {{
    color: {C['blue2']};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 6px;
    display: block;
}}
.source-note {{
    color: {C['muted']};
    font-size: 11px;
    font-style: italic;
    margin-top: 4px;
}}
.page-title {{
    font-size: 32px;
    font-weight: 800;
    color: {C['white']};
    letter-spacing: -1px;
    line-height: 1.2;
    margin-bottom: 4px;
}}
.page-subtitle {{
    font-size: 15px;
    color: {C['silver']};
    font-weight: 400;
    margin-bottom: 20px;
    line-height: 1.5;
}}
.kpi-badge-pass {{ background: {C['greenl']}; color: {C['green']}; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }}
.kpi-badge-warn {{ background: {C['amberl']}; color: {C['amber']}; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }}
.kpi-badge-fail {{ background: {C['redl']}; color: {C['red']}; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }}
.timeline-node {{
    text-align: center;
    padding: 16px 12px;
    border-radius: 12px;
    margin: 4px;
}}
.phase-card {{
    background: {C['glass']};
    border: 1px solid {C['border']};
    border-radius: 14px;
    padding: 20px;
    height: 100%;
    transition: all 0.2s;
}}
.phase-card:hover {{
    border-color: {C['blue2']};
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(37,99,235,0.18);
}}
</style>
""", unsafe_allow_html=True)

# ─── CHART DEFAULTS ──────────────────────────────────────────────────────────
BG = dict(
    paper_bgcolor=C["bg"],
    plot_bgcolor=C["surface"],
    font=dict(family="Inter", color=C["silver"], size=13),
    title_font=dict(family="Inter", color=C["white"], size=16, weight="bold"),
)
AXIS = dict(gridcolor=C["border"], linecolor=C["border"],
            tickfont=dict(color=C["silver"], size=12, family="Inter"),
            zeroline=False)
CFG = {"displayModeBar": False}

def chart(fig, title="", h=380, pad=dict(l=40,r=20,t=55,b=40)):
    fig.update_layout(**BG, title_text=title, height=h, margin=pad,
                      xaxis=AXIS, yaxis=AXIS)
    return fig

def chart2(fig, title="", h=380):
    fig.update_layout(**BG, title_text=title, height=h,
                      margin=dict(l=40,r=20,t=55,b=50),
                      xaxis=AXIS,  yaxis=AXIS,
                      xaxis2=AXIS, yaxis2=AXIS)
    return fig

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def banner(text):
    st.markdown(f'<div class="exec-banner"><p>{text}</p></div>', unsafe_allow_html=True)

def insight(text, kind="gold"):
    cls = {"gold":"insight-gold","green":"insight-green","red":"insight-red"}.get(kind,"insight-gold")
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)

def src(text):
    st.markdown(f'<p class="source-note">📌 {text}</p>', unsafe_allow_html=True)

def section(text):
    st.markdown(f'<span class="section-label">{text}</span>', unsafe_allow_html=True)

def page_header(title, subtitle):
    st.markdown(f'<p class="page-title">{title}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-subtitle">{subtitle}</p>', unsafe_allow_html=True)

def glass(content_fn):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    content_fn()
    st.markdown('</div>', unsafe_allow_html=True)

def stat_row(items):
    """items: list of (value, label) tuples shown as inline stats"""
    html = '<div style="display:flex;gap:32px;flex-wrap:wrap;margin:12px 0;">'
    for val, label in items:
        html += f'''<div style="text-align:center;">
            <div style="font-size:26px;font-weight:800;color:{C["gold"]};letter-spacing:-1px;">{val}</div>
            <div style="font-size:11px;color:{C["silver"]};text-transform:uppercase;letter-spacing:1.5px;font-weight:600;">{label}</div>
        </div>'''
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ─── DATA ────────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    career = pd.read_csv("/Users/husnarafi/Documents/BC3/Python/CSV Exports/career_search_trends.csv", parse_dates=["date"])
    firm   = pd.read_csv("/Users/husnarafi/Documents/BC3/Python/CSV Exports/trends_firm_careers.csv",   parse_dates=["date"])
    vsai   = pd.read_csv("/Users/husnarafi/Documents/BC3/Python/CSV Exports/trends_consulting_vs_ai.csv", parse_dates=["date"])
    skill  = pd.read_csv("/Users/husnarafi/Documents/BC3/Python/CSV Exports/trends_skill_demand.csv",   parse_dates=["date"])
    junior = pd.read_csv("/Users/husnarafi/Documents/BC3/Python/CSV Exports/trends_junior_experience.csv", parse_dates=["date"])

    al = pd.read_excel("/Users/husnarafi/Documents/BC3/Python/CSV Exports/ADL_Alumni_Career_Destinations.xlsx")
    al.columns = ["Person","Joined","Left","Company","Industry","Role","Link"]
    al["Industry"] = al["Industry"].str.strip()
    al["Joined"]   = pd.to_datetime(al["Joined"], errors="coerce")
    al["Left"]     = pd.to_datetime(al["Left"],   errors="coerce")
    al["Tenure"]   = ((al["Left"]-al["Joined"]).dt.days/30.44).round(0)
    al["AI_era"]   = al["Joined"].dt.year >= 2022
    al["Era"]      = al["AI_era"].map({True:"AI Era (2022+)",False:"Pre-AI"})
    al["JoinYr"]   = al["Joined"].dt.year

    hc = pd.read_excel("/Users/husnarafi/Documents/BC3/Python/CSV Exports/Consulting_Entry_Level_Headcount_Analysis.xlsx")
    hc = hc[["Company","Entry-level","Total Employees","Junior Ratio"]].dropna(subset=["Company","Junior Ratio"])
    hc = hc[hc["Company"].apply(lambda x: isinstance(x,str) and len(x)<50 and "Firm" not in str(x))]
    hc["Pct"] = (hc["Junior Ratio"]*100).round(1)
    return career, firm, vsai, skill, junior, al, hc

career_df, firm_df, vsai_df, skill_df, junior_df, alumni_df, hc_df = load()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 8px 0;">
        <div style="font-size:20px;font-weight:800;color:{C['white']};letter-spacing:-0.5px;">🔷 ADL Intelligence</div>
        <div style="font-size:11px;color:{C['blue2']};font-weight:600;letter-spacing:2px;margin-top:2px;">EXECUTIVE DASHBOARD</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<p style='color:{C['silver']};font-size:12px;margin:0;'>Built by Husna Rafi<br>Hult MBA Capstone 2026</p>", unsafe_allow_html=True)
    st.divider()

    pitch_mode = st.toggle("🎤 Presentation Mode", value=False,
        help="Clean view — hides methodology notes for presenting")
    st.divider()

    st.markdown(f"<span class='section-label'>THE CASE</span>", unsafe_allow_html=True)
    pg1 = st.radio("", [
        "🏠  Executive Summary",
        "📊  Talent Signal",
        "👥  Alumni Intelligence",
        "🏢  Firm Benchmarking",
    ], label_visibility="collapsed", key="nav1")

    st.markdown(f"<span class='section-label'>THE STRATEGY</span>", unsafe_allow_html=True)
    pg2 = st.radio("", [
        "🎯  Strategic Recommendation",
        "💼  PE Value-Creation Engine",
        "📐  Talent Pyramid",
    ], label_visibility="collapsed", key="nav2")

    st.markdown(f"<span class='section-label'>THE EXECUTION</span>", unsafe_allow_html=True)
    pg3 = st.radio("", [
        "🗓️  90-Day Pilot + Roadmap",
        "🏗️  AI Architecture",
        "👔  Talent Transformation",
        "⚠️  Risk + KPI Scorecard",
    ], label_visibility="collapsed", key="nav3")

    st.markdown(f"<span class='section-label'>THE EVIDENCE</span>", unsafe_allow_html=True)
    pg4 = st.radio("", [
        "🔍  4-Layer Validator",
        "🧠  RAG Simulator",
        "⚙️  Engagement Economics",
        "📈  Revenue Scenarios",
        "📖  Methodology",
    ], label_visibility="collapsed", key="nav4")

# Determine active page using session state
if "active_page" not in st.session_state:
    st.session_state.active_page = "🏠  Executive Summary"

# Check which radio changed
for nav_key, nav_val in [("nav1",pg1),("nav2",pg2),("nav3",pg3),("nav4",pg4)]:
    stored = st.session_state.get(f"prev_{nav_key}")
    if stored != nav_val:
        st.session_state.active_page = nav_val
        st.session_state[f"prev_{nav_key}"] = nav_val

page = st.session_state.active_page

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EXECUTIVE SUMMARY (HERO)
# ══════════════════════════════════════════════════════════════════════════════
if "Executive Summary" in page:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(37,99,235,0.12) 0%,rgba(6,182,212,0.06) 100%);
        border:1px solid rgba(37,99,235,0.25);border-radius:16px;padding:36px 40px;margin-bottom:24px;">
        <div style="font-size:11px;color:{C['blue2']};font-weight:700;letter-spacing:3px;margin-bottom:8px;">
            ARTHUR D. LITTLE  |  EXECUTIVE STRATEGY DASHBOARD  |  APRIL 2026
        </div>
        <div style="font-size:38px;font-weight:800;color:{C['white']};letter-spacing:-1.5px;line-height:1.15;margin-bottom:12px;">
            From Talent Model<br>to Value-Creation Engine
        </div>
        <div style="font-size:16px;color:{C['silver']};line-height:1.6;max-width:700px;">
            AI has automated the work that taught consultants to think. ADL must evolve its talent 
            architecture from the inside — and package that same methodology as a specialist 
            advisory service for Private Equity.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("ADL Career Search", "0 / 100", "87 consecutive months")
    with c2: st.metric("Tenure Compression", "69%", "73mo → 23mo AI-era")
    with c3: st.metric("PE GPs Prioritising AI", "94%", "n=362 ADL/Invest Europe 2025")
    with c4: st.metric("European PE Dry Powder", "$414B", "Ready to deploy now")

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        section("THE PROBLEM")
        st.markdown(f"""
        <div class="glass-card">
            <div style="font-size:15px;font-weight:700;color:{C['white']};margin-bottom:12px;">The Productivity Paradox</div>
            <p>AI has automated the analytical work that taught junior consultants to think — 
            the benchmarking, modelling, and synthesis that over two years of repetition built 
            the judgment that made great senior advisors.</p>
            <p>With that work automated, the apprenticeship has broken down. 
            ADL recorded zero career search interest for 87 consecutive months. 
            44% of alumni exit to tech. No proprietary knowledge base exists. 
            The pyramid is shrinking at the base with nothing replacing it.</p>
        </div>
        """, unsafe_allow_html=True)

        section("THE FOUR HYPOTHESES — ALL CONFIRMED")
        hyps = [
            ("H1","Brand invisible","Zero career search. 87 months. McKinsey averages 51.",C["red"]),
            ("H2","Apprenticeship broken","AI compresses the work that built judgment. No replacement.",C["amber"]),
            ("H3","Training vacuum","64% of firms: zero GenAI training. No interrogation framework.",C["amber"]),
            ("H4","Hiring disconnected","44% alumni to tech. Criteria unchanged. Pipeline draining.",C["blue2"]),
        ]
        for code, head, body, color in hyps:
            st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-bottom:1px solid {C['border']};">
                <div style="background:{color};color:{C['white']};font-size:11px;font-weight:700;
                    padding:3px 8px;border-radius:6px;white-space:nowrap;margin-top:2px;">{code}</div>
                <div>
                    <div style="font-size:13px;font-weight:600;color:{C['white']};">{head}</div>
                    <div style="font-size:12px;color:{C['silver']};">{body}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_b:
        section("THE RECOMMENDATION")
        st.markdown(f"""
        <div class="glass-card" style="border-color:{C['blue']};border-left:4px solid {C['blue']};">
            <div style="font-size:15px;font-weight:700;color:{C['white']};margin-bottom:12px;">Two Connected Moves</div>
            <div style="display:flex;gap:10px;margin-bottom:14px;">
                <div style="background:{C['blue']};color:white;font-size:10px;font-weight:700;
                    padding:2px 10px;border-radius:20px;white-space:nowrap;">INTERNAL</div>
                <p style="margin:0;font-size:13px;">Evolve the talent architecture toward a Diamond Pyramid 
                over 3 years. AI handles the analytical base. Domain specialists own judgment. 
                RAG apprenticeship replaces data cleaning as the development mechanism.</p>
            </div>
            <div style="display:flex;gap:10px;">
                <div style="background:{C['green']};color:white;font-size:10px;font-weight:700;
                    padding:2px 10px;border-radius:20px;white-space:nowrap;">EXTERNAL</div>
                <p style="margin:0;font-size:13px;">Package that same methodology as a PE 
                Value-Creation Engine — a three-phase advisory service that ADL practises 
                internally and sells commercially.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        section("THREE STRATEGIC FRAMINGS")
        framings = [
            ("Evolve, not replace","3-year transition alongside existing practice — no one gets fired",C["blue2"]),
            ("Concentrate, not exit","New investment in PE + Telecom + Energy; other clients continue",C["teal"]),
            ("Boutique, not MBB","Win mandates generalist firms treat as secondary; not McKinsey's market",C["green"]),
        ]
        for label, body, color in framings:
            st.markdown(f"""
            <div style="padding:10px 14px;border-left:3px solid {color};margin:6px 0;
                background:rgba(30,58,95,0.3);border-radius:0 8px 8px 0;">
                <div style="font-size:13px;font-weight:600;color:{color};">{label}</div>
                <div style="font-size:12px;color:{C['silver']};">{body}</div>
            </div>
            """, unsafe_allow_html=True)

        section("THE ASK — THREE DECISIONS NEEDED")
        asks = [("1","Approve PE Practice Lead hire"),
                ("2","Allocate $300–500K platform budget on existing Azure"),
                ("3","Authorise 90-day pilot with one existing PE relationship")]
        for n, ask in asks:
            st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:center;padding:8px 0;border-bottom:1px solid {C['border']};">
                <div style="background:{C['gold']};color:{C['bg']};font-size:13px;font-weight:800;
                    width:28px;height:28px;border-radius:50%;display:flex;align-items:center;
                    justify-content:center;flex-shrink:0;">{n}</div>
                <div style="font-size:13px;color:{C['white']};font-weight:500;">{ask}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TALENT SIGNAL
# ══════════════════════════════════════════════════════════════════════════════
elif "Talent Signal" in page:
    page_header("Talent Signal","Google Trends evidence — 87 months of data showing ADL's brand invisibility")
    banner("ADL recorded zero career search interest across every single month from 2019 to 2026. McKinsey averaged 51 on the same scale. This is not a bad year — it is the complete absence of a talent brand signal.")

    c1,c2,c3,c4 = st.columns(4)
    zero_mo = (career_df["Arthur D Little careers"]==0).sum()
    with c1: st.metric("ADL Career Score","0",f"{zero_mo} months of zero")
    with c2: st.metric("McKinsey Avg Score","51","Same 0-100 scale")
    with c3: st.metric("BCG Avg Score","31","Same period")
    with c4: st.metric("AT Kearney Avg Score","4","Closest boutique peer")
    if not pitch_mode: src("Google Trends — self-collected via Python pytrends API. Jan 2019 – Apr 2026. 88 monthly data points. Scale 0–100 normalised by Google.")
    st.divider()

    section("SELECT FIRMS TO COMPARE — INTERACTIVE")
    firm_opts   = ["Arthur D Little careers","McKinsey careers","BCG careers","AT Kearney careers"]
    firm_cols   = [C["red"],C["gold"],C["blue2"],C["teal"]]
    firm_names  = ["Arthur D. Little","McKinsey","BCG","AT Kearney"]
    sel = st.multiselect("Firms:", firm_opts,
        default=["Arthur D Little careers","McKinsey careers","BCG careers"],
        format_func=lambda x: dict(zip(firm_opts,firm_names))[x])

    col_r, col_s = st.columns([3,1])
    with col_r:
        dr = st.slider("Date range:", min_value=career_df["date"].min().to_pydatetime(),
            max_value=career_df["date"].max().to_pydatetime(),
            value=(career_df["date"].min().to_pydatetime(), career_df["date"].max().to_pydatetime()),
            format="MMM YYYY")
    with col_s:
        smooth = st.checkbox("3-month smoothing", value=True)

    filt = career_df[(career_df["date"]>=pd.Timestamp(dr[0]))&(career_df["date"]<=pd.Timestamp(dr[1]))]
    fig = go.Figure()
    for f, color, name in zip(firm_opts, firm_cols, firm_names):
        if f in sel:
            y = filt[f].rolling(3,center=True).mean() if smooth else filt[f]
            is_adl = "Little" in f
            fig.add_trace(go.Scatter(x=filt["date"], y=y, name=name,
                line=dict(color=color, width=3 if is_adl else 2),
                fill="tozeroy" if is_adl else None,
                fillcolor="rgba(239,68,68,0.06)" if is_adl else None,
                mode="lines"))
    fig.add_vrect(x0=pd.Timestamp("2022-01-01"), x1=filt["date"].max(),
        fillcolor=C["blue"], opacity=0.05,
        annotation_text="AI Era begins", annotation_font_color=C["silver"],
        annotation_position="top left")
    fig.add_annotation(x=pd.Timestamp("2023-06-01"), y=2, text="ADL = 0 throughout",
        showarrow=True, arrowhead=2, arrowcolor=C["red"],
        font=dict(color=C["red"],size=13,family="Inter"), arrowwidth=2)
    chart(fig, "Career Search Interest — Google Trends Scale 0–100", h=420)
    fig.update_layout(legend=dict(orientation="h", y=-0.18, x=0, font=dict(size=13,family="Inter")))
    st.plotly_chart(fig, use_container_width=True, config=CFG)

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        section("CONSULTING VS AI JOB SEARCH INTENT")
        f2 = go.Figure()
        cs = [c for c in vsai_df.columns if c not in ["date","isPartial"]]
        palette = [C["red"],C["gold"],C["blue2"],C["green"]]
        for c2, col in zip(cs, palette):
            f2.add_trace(go.Scatter(x=vsai_df["date"], y=vsai_df[c2],
                name=c2, line=dict(color=col,width=2), mode="lines"))
        chart(f2, "Search Intent: Consulting vs AI Roles", h=320)
        f2.update_layout(legend=dict(orientation="h",y=-0.25,font=dict(size=11)))
        st.plotly_chart(f2, use_container_width=True, config=CFG)
        if not pitch_mode: src("Google Trends — trends_consulting_vs_ai.csv")

    with col_b:
        section("'LEAVE CONSULTING' — SENTIMENT SIGNAL")
        f3 = go.Figure()
        js = [c for c in junior_df.columns if c not in ["date","isPartial"]]
        for j, col in zip(js, palette):
            f3.add_trace(go.Scatter(x=junior_df["date"], y=junior_df[j],
                name=j, line=dict(color=col,width=2), mode="lines"))
        chart(f3, "Junior Sentiment — Exit Search Trends", h=320)
        f3.update_layout(legend=dict(orientation="h",y=-0.25,font=dict(size=11)))
        st.plotly_chart(f3, use_container_width=True, config=CFG)
        if not pitch_mode: src("Google Trends — trends_junior_experience.csv")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ALUMNI INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif "Alumni Intelligence" in page:
    page_header("Alumni Intelligence","100 LinkedIn profiles reveal the talent pipeline breaking down")
    banner("Junior analyst tenure at ADL compressed from 73 months pre-AI to 23 months in the AI era — a 69% reduction. 44% of alumni now exit directly to tech companies. The pipeline that feeds client relationships is draining.")

    valid = alumni_df.dropna(subset=["Tenure"])
    pre   = valid[valid["Era"]=="Pre-AI"]["Tenure"]
    ai    = valid[valid["Era"]=="AI Era (2022+)"]["Tenure"]
    tech  = (alumni_df["Industry"].str.contains("Tech|Platform",case=False,na=False)).sum()

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Pre-AI Avg Tenure",f"{pre.mean():.0f} months","Baseline")
    with c2: st.metric("AI-Era Avg Tenure",f"{ai.mean():.0f} months",f"{((ai.mean()-pre.mean())/pre.mean()*100):.0f}% change")
    with c3: st.metric("Tech / Platform Exits",f"{tech} alumni","of 100 profiled")
    with c4: st.metric("Tenure Compression","69%","Months lost per analyst")
    if not pitch_mode: src("LinkedIn alumni analysis — 100 ADL alumni profiles, April 2026.")
    st.divider()

    section("FILTER THE DATA")
    cf1,cf2,cf3 = st.columns(3)
    with cf1: era_f = st.selectbox("Era:",["All","Pre-AI","AI Era (2022+)"])
    with cf2:
        ind_opts = ["All"]+sorted(alumni_df["Industry"].dropna().unique().tolist())
        ind_f = st.selectbox("Industry:", ind_opts)
    with cf3:
        ten_f = st.slider("Tenure (months):",0,int(valid["Tenure"].max()),(0,int(valid["Tenure"].max())),step=6)

    flt = valid.copy()
    if era_f!="All": flt = flt[flt["Era"]==era_f]
    if ind_f!="All": flt = flt[flt["Industry"]==ind_f]
    flt = flt[(flt["Tenure"]>=ten_f[0])&(flt["Tenure"]<=ten_f[1])]
    st.markdown(f"<p style='color:{C['gold']};font-size:13px;font-weight:600;'>Showing {len(flt)} of {len(valid)} alumni</p>",unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        fh = go.Figure()
        for era, col in [("Pre-AI",C["blue2"]),("AI Era (2022+)",C["red"])]:
            s = flt[flt["Era"]==era]["Tenure"]
            if len(s):
                fh.add_trace(go.Histogram(x=s, name=era, marker_color=col, opacity=0.75, xbins=dict(size=8)))
                fh.add_vline(x=s.mean(), line_color=col, line_dash="dash",
                    annotation_text=f"Avg {s.mean():.0f}mo", annotation_font_color=col)
        chart(fh, "Tenure Distribution — Pre-AI vs AI Era", h=340)
        fh.update_layout(barmode="overlay",legend=dict(orientation="h",y=-0.22,font=dict(size=12)))
        st.plotly_chart(fh, use_container_width=True, config=CFG)

    with col_b:
        ic = flt["Industry"].value_counts().head(8)
        bar_colors = [C["gold"] if "Tech" in i or "Platform" in i else C["blue2"] for i in ic.index]
        fb = go.Figure(go.Bar(x=ic.values, y=ic.index, orientation="h",
            marker_color=bar_colors, text=ic.values,
            textposition="outside", textfont=dict(color=C["white"],size=12,family="Inter")))
        chart(fb, "Exit Destinations (filtered)", h=340)
        fb.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fb, use_container_width=True, config=CFG)

    st.divider()
    section("ALUMNI PIPELINE IMPACT CALCULATOR")
    st.markdown(f"<p style='color:{C['silver']};font-size:13px;'>Adjust the assumptions to model how talent development quality affects client pipeline value.</p>",unsafe_allow_html=True)

    pp1,pp2,pp3 = st.columns(3)
    with pp1: aly = st.slider("Alumni per year:",20,100,50,step=5)
    with pp2: conv = st.slider("Buyer conversion rate (%):",1,30,15,step=1)
    with pp3: lval = st.slider("Avg engagement value ($K):",100,1000,500,step=50)

    broken = max(1,conv-10)
    healthy_p = aly*(conv/100)*lval*1000
    broken_p  = aly*(broken/100)*lval*1000
    destroyed = healthy_p - broken_p

    pc1,pc2,pc3 = st.columns(3)
    with pc1: st.metric("Healthy Pipeline / Cohort",f"${healthy_p/1e6:.2f}M","Functional model")
    with pc2: st.metric("Broken Pipeline / Cohort",f"${broken_p/1e6:.2f}M",f"-${destroyed/1e6:.2f}M")
    with pc3: st.metric("Value Destroyed — 10 Years",f"${destroyed*10/1e6:.1f}M","Compounding annually")

    insight(f"""<strong style='color:{C['gold']};'>The Alumni Pipeline Argument:</strong> 
    When ADL develops consultants well, they leave after 4–7 years and become buyers — returning as clients worth ${lval}K lifetime value. 
    With {conv}% conversion that is <strong style='color:{C['green']};'>${healthy_p/1e6:.2f}M per cohort</strong>. 
    A broken apprenticeship reduces conversion to {broken}% — destroying 
    <strong style='color:{C['red']};'>${destroyed*10/1e6:.1f}M over 10 years</strong> from pipeline alone.""")

    with st.expander("📋 View Alumni Data"):
        st.dataframe(flt[["Era","JoinYr","Tenure","Industry","Role"]].sort_values("JoinYr",ascending=False),
            use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FIRM BENCHMARKING
# ══════════════════════════════════════════════════════════════════════════════
elif "Firm Benchmarking" in page:
    page_header("Firm Benchmarking","How ADL compares to peers on talent structure and AI readiness")
    banner("ADL's junior analyst ratio sits at an estimated 35% of total headcount — comparable to McKinsey. As AI automates junior work, firms with high junior ratios face the greatest structural pressure. ADL must manage this transition deliberately.")

    adl = pd.DataFrame([{"Company":"Arthur D. Little (est.)","Pct":35.0,"Entry-level":525,"Total Employees":1500}])
    plot_hc = pd.concat([hc_df[["Company","Pct","Entry-level","Total Employees"]],adl],ignore_index=True).dropna(subset=["Pct"])
    plot_hc = plot_hc.sort_values("Pct",ascending=True)
    avg = plot_hc["Pct"].mean()

    colors = [C["gold"] if "Arthur" in str(c) else C["blue2"] for c in plot_hc["Company"]]
    fh = go.Figure(go.Bar(x=plot_hc["Pct"], y=plot_hc["Company"], orientation="h",
        marker_color=colors, text=[f"{v:.1f}%" for v in plot_hc["Pct"]],
        textposition="outside", textfont=dict(color=C["white"],size=13,family="Inter")))
    fh.add_vline(x=avg, line_color=C["teal"], line_dash="dash",
        annotation_text=f"Industry avg {avg:.1f}%", annotation_font_color=C["teal"],
        annotation_position="top right")
    chart(fh, "Junior Analyst % of Total Headcount by Firm (LinkedIn data, 2026)", h=360)
    fh.update_layout(xaxis=dict(range=[0,85]))
    st.plotly_chart(fh, use_container_width=True, config=CFG)
    if not pitch_mode: src("LinkedIn company pages — headcount approximated. ADL estimated at 1,500 employees, ~35% junior.")

    st.divider()
    section("COMPETITIVE POSITIONING — AI ADOPTION vs TALENT BRAND")
    st.markdown(f"<p style='color:{C['silver']};font-size:13px;'>Use the sliders to model ADL's proposed future position. The gold star shows the target state after the 3-year transformation.</p>",unsafe_allow_html=True)

    firms_d = {
        "McKinsey":       {"ai":92,"brand":95,"size":48000,"type":"MBB"},
        "BCG":            {"ai":85,"brand":80,"size":32000,"type":"MBB"},
        "Bain":           {"ai":78,"brand":72,"size":12000,"type":"MBB"},
        "Oliver Wyman":   {"ai":55,"brand":35,"size":5000, "type":"Specialist"},
        "Kearney":        {"ai":50,"brand":32,"size":3800, "type":"Mid-tier"},
        "Roland Berger":  {"ai":42,"brand":28,"size":2800, "type":"Boutique"},
        "AI-Native Firms":{"ai":95,"brand":20,"size":2000, "type":"AI-native"},
        "Arthur D. Little":{"ai":28,"brand":5, "size":1500,"type":"Boutique"},
    }

    sc1,sc2 = st.columns(2)
    with sc1: adl_ai = st.slider("ADL AI Adoption — current → proposed:",0,100,value=[28,72],step=5)
    with sc2: adl_br = st.slider("ADL Talent Brand — current → proposed:",0,100,value=[5,38],step=5)

    type_colors = {"MBB":C["blue2"],"Specialist":C["teal"],"Mid-tier":C["silver"],"Boutique":C["gold"],"AI-native":C["green"]}
    fs = go.Figure()
    for name, d in firms_d.items():
        is_adl = "Arthur" in name
        col = C["gold"] if is_adl else type_colors[d["type"]]
        fs.add_trace(go.Scatter(x=[d["ai"]], y=[d["brand"]],
            mode="markers+text", name=name, showlegend=not is_adl,
            text=[name], textposition="top center",
            textfont=dict(color=col, size=12, family="Inter"),
            marker=dict(size=max(16,d["size"]/900), color=col, opacity=0.85,
                line=dict(color=C["white"],width=1.5))))

    fs.add_trace(go.Scatter(x=[adl_ai[1]], y=[adl_br[1]],
        mode="markers+text", name="ADL Proposed", showlegend=True,
        text=["ADL (target)"], textposition="top center",
        textfont=dict(color=C["green"],size=13,family="Inter",weight="bold"),
        marker=dict(size=22,color=C["green"],symbol="star",line=dict(color=C["white"],width=2))))

    fs.add_annotation(x=adl_ai[1],y=adl_br[1],ax=firms_d["Arthur D. Little"]["ai"],
        ay=firms_d["Arthur D. Little"]["brand"],
        xref="x",yref="y",axref="x",ayref="y",
        arrowhead=3,arrowsize=1.5,arrowcolor=C["gold"],arrowwidth=2.5)

    chart(fs,"AI Adoption vs Talent Brand — Consulting Landscape", h=460)
    fs.update_xaxes(title_text="AI Adoption Score (0–100)",range=[-5,105])
    fs.update_yaxes(title_text="Talent Brand Visibility (0–100)",range=[-5,105])
    fs.update_layout(showlegend=True,legend=dict(orientation="h",y=-0.18,font=dict(size=12)))
    st.plotly_chart(fs, use_container_width=True, config=CFG)

    insight("""The gold star shows ADL's target position — not competing with McKinsey on volume or brand, 
    but meaningfully differentiated from Roland Berger and Kearney on AI adoption, with a specialist 
    brand in PE, Telecom and Energy that generalist firms cannot replicate. 
    ADL wins in the white space between MBB and pure AI-native firms.""")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: STRATEGIC RECOMMENDATION
# ══════════════════════════════════════════════════════════════════════════════
elif "Strategic Recommendation" in page:
    page_header("Strategic Recommendation","The answer to: how should ADL evolve its consulting model in response to AI?")
    banner("ADL will evolve its talent architecture over a 3-year transition — running specialist capability development alongside its existing practice — concentrating new investment in PE, Telecom, and Energy, targeting boutique-winnable mandates.")

    col_a, col_b = st.columns([1,1])

    with col_a:
        section("THE CORE THESIS")
        st.markdown(f"""
        <div class="glass-card" style="border-color:{C['blue']};border-left:4px solid {C['blue']};">
            <p style='font-size:15px;color:{C['white']};font-weight:500;line-height:1.7;'>
            ADL must make two connected moves simultaneously.
            </p>
            <div style='margin:14px 0;padding:12px 16px;background:rgba(37,99,235,0.1);border-radius:8px;'>
                <div style='font-size:11px;font-weight:700;color:{C['blue2']};letter-spacing:2px;margin-bottom:6px;'>INTERNAL MOVE</div>
                <p style='font-size:13px;color:{C['white']};margin:0;line-height:1.6;'>
                Evolve from a shrinking traditional pyramid to a Diamond Pyramid. 
                AI handles the analytical base. ADL over-invests in domain specialist judgment in the middle. 
                The RAG apprenticeship replaces data cleaning as the development mechanism — 
                <em>building the knowledge base IS the new apprenticeship.</em>
                </p>
            </div>
            <div style='padding:12px 16px;background:rgba(16,185,129,0.08);border-radius:8px;'>
                <div style='font-size:11px;font-weight:700;color:{C['green']};letter-spacing:2px;margin-bottom:6px;'>EXTERNAL MOVE</div>
                <p style='font-size:13px;color:{C['white']};margin:0;line-height:1.6;'>
                Package that same methodology as a PE Value-Creation Engine — 
                a three-phase advisory service that ADL practises internally and sells commercially. 
                ADL does not just consult on this transformation. It becomes the proof that it works.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        section("THREE NON-NEGOTIABLE FRAMINGS")
        frames = [
            ("Evolve, not replace","3-year transition running new model alongside existing practice. No redundancies. No client abandonment.",C["blue2"]),
            ("Concentrate, not exit","New investment concentrated in PE + Telecom + Energy. Existing partner relationships in other sectors continue opportunistically.",C["teal"]),
            ("Boutique, not MBB","ADL targets mandates that boutique specialist depth makes uniquely winnable. Not competing with McKinsey. Winning where McKinsey will not go.",C["gold"]),
        ]
        for lbl, body, col in frames:
            st.markdown(f"""
            <div class="glass-card" style="border-left:3px solid {col};padding:14px 18px;margin:6px 0;">
                <div style='font-size:13px;font-weight:700;color:{col};margin-bottom:4px;'>{lbl}</div>
                <p style='font-size:12px;margin:0;'>{body}</p>
            </div>
            """, unsafe_allow_html=True)

    with col_b:
        section("THREE VERTICALS — WHY THESE THREE")
        verticals = [
            ("Telecom","15+ active clients","Telecom deal value +31% (2025). 5G, AI network layer transformations creating complex leadership succession challenges. ADL has published sector credentials.",C["blue2"],31),
            ("Energy & Utilities","10+ active clients","Energy deal value +75% (2025). Energy transition requiring entirely new leadership competencies. ADL's PE Safety report directly addresses this.",C["teal"],75),
            ("Private Equity","250+ transactions","94% of GPs prioritising AI now. $414B European dry powder to deploy. Every acquisition has a 100-day leadership window. Most urgent, most repeatable.",C["gold"],94),
        ]
        for name, clients, why, col, stat in verticals:
            st.markdown(f"""
            <div class="glass-card" style="border-top:3px solid {col};padding:16px 20px;margin:8px 0;">
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div>
                        <div style='font-size:15px;font-weight:700;color:{C['white']};'>{name}</div>
                        <div style='font-size:11px;color:{col};font-weight:600;letter-spacing:1px;'>{clients}</div>
                    </div>
                    <div style='font-size:28px;font-weight:800;color:{col};'>{stat}<span style='font-size:14px;'>%</span></div>
                </div>
                <p style='font-size:12px;margin-top:8px;margin-bottom:0;line-height:1.6;'>{why}</p>
            </div>
            """, unsafe_allow_html=True)

        section("TALENT SIGNAL — WE DO NOT REPLACE JUNIORS")
        ts = [
            ("RAG Apprenticeship","Existing analysts retrained — building the KB is the new development path. Same judgment skills, different mechanism."),
            ("Domain Specialist Hire","New profile: sector depth + AI interrogation. Recruited from industry not MBA programmes."),
            ("Sector-AI Certification","12-week external programme. $2,500–$5,000/person. 500 certified per vertical per year. $3.75–7.5M/yr revenue. No competitor offers this."),
        ]
        for head, body in ts:
            st.markdown(f"""
            <div style='padding:10px 0;border-bottom:1px solid {C['border']};display:flex;gap:10px;align-items:flex-start;'>
                <div style='color:{C['teal']};font-size:16px;margin-top:2px;'>◆</div>
                <div>
                    <div style='font-size:13px;font-weight:600;color:{C['white']};'>{head}</div>
                    <div style='font-size:12px;color:{C['silver']};'>{body}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PE VALUE-CREATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════
elif "PE Value-Creation Engine" in page:
    page_header("PE Value-Creation Engine","The three-phase offering — what ADL sells to Private Equity portfolio companies")
    banner("Every PE acquisition has a 100-day window where leadership clarity determines whether the investment thesis survives reality. ADL's three-phase offering plugs directly into this window and stays through the full 7-year holding period.")

    stat_row([("100 days","Critical post-acquisition window"),("7 years","Avg PE holding period (Bain 2026)"),("$1.3T","Global PE dry powder"),("94%","GPs prioritising AI now")])
    st.divider()

    section("THREE-PHASE OFFERING — ENTRY TO RETAINER")
    phases = [
        {"num":"01","label":"100-Day AI Talent Diagnostic","tag":"ENTRY WEDGE","price":"$150K",
         "pain":"Founders leave. Managers are unprepared. The 100-day clock starts on Day 1 of ownership.",
         "what":["AI maps every layer of the portfolio company talent pyramid","Identifies who can lead and who needs acceleration","Capability gap map — where the value creation plan is at risk","Organisational intelligence dashboard (baseline)","100-day action plan for portfolio company leadership"],
         "pe":"PE firm commitment: Low. Proof of concept. Priced to get to yes.",
         "color":C["gold"],"bg":"rgba(217,119,6,0.08)"},
        {"num":"02","label":"180-Day Leadership Acceleration","tag":"CORE REVENUE","price":"$385K",
         "pain":"Value creation plans fail because capability gaps that due diligence missed are never closed.",
         "what":["AI-personalised development paths per pyramid layer","Manager-to-leader acceleration programme","Innovation sprints for senior leadership","AI-enabled decision-making workshops","KPI-linked performance analytics at every board meeting"],
         "pe":"PE firm commitment: Medium. Largest revenue engagement. Builds ADL knowledge base.",
         "color":C["blue2"],"bg":"rgba(59,130,246,0.08)"},
        {"num":"03","label":"12-Month Scale & Institutionalise","tag":"RECURRING REVENUE","price":"$250K/yr",
         "pain":"7-year average holding period. Value must be sustained through the full ownership cycle to exit.",
         "what":["AI-powered knowledge engine embedded in portfolio company","Repeatable operating model for talent development","Leadership succession pipeline — exit-ready","Quarterly performance dashboards for PE board","Portfolio-wide licence for additional companies"],
         "pe":"PE firm commitment: High. Annual retainer. Highest margin. Switching cost builds over time.",
         "color":C["green"],"bg":"rgba(16,185,129,0.08)"},
    ]

    cols = st.columns(3)
    for col, ph in zip(cols, phases):
        with col:
            st.markdown(f"""
            <div style="background:{ph['bg']};border:1px solid {ph['color']};border-top:4px solid {ph['color']};
                border-radius:14px;padding:22px;height:100%;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                    <div style="background:{ph['color']};color:{C['bg']};font-size:13px;font-weight:800;
                        width:32px;height:32px;border-radius:50%;display:flex;align-items:center;
                        justify-content:center;">{ph['num']}</div>
                    <div>
                        <div style="font-size:14px;font-weight:700;color:{C['white']};line-height:1.2;">{ph['label']}</div>
                        <span style="background:{ph['color']};color:{C['bg']};font-size:10px;font-weight:700;
                            padding:2px 8px;border-radius:12px;letter-spacing:1px;">{ph['tag']}</span>
                    </div>
                </div>
                <div style="margin-bottom:14px;">
                    {''.join([f'<div style="display:flex;gap:8px;margin:5px 0;"><span style="color:{ph["color"]};font-size:12px;flex-shrink:0;margin-top:1px;">▸</span><span style="font-size:12px;color:{C["silver"]};line-height:1.5;">{item}</span></div>' for item in ph['what']])}
                </div>
                <div style="border-top:1px solid rgba(255,255,255,0.1);padding-top:12px;margin-bottom:12px;">
                    <div style="font-size:11px;font-weight:600;color:{ph['color']};margin-bottom:4px;">PE PAIN POINT ADDRESSED</div>
                    <p style="font-size:12px;margin:0;font-style:italic;color:{C['silver']};line-height:1.5;">{ph['pain']}</p>
                </div>
                <div style="background:{ph['color']};border-radius:10px;padding:12px;text-align:center;">
                    <div style="font-size:24px;font-weight:800;color:{C['bg']};letter-spacing:-0.5px;">{ph['price']}</div>
                    <div style="font-size:10px;color:{C['bg']};opacity:0.75;font-weight:600;">{ph['pe'].split('.')[0]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    section("HOW IT EXPANDS ACROSS A PE PORTFOLIO")
    expand = [
        ("Portfolio-wide Licence","Once one PE firm sees Phase 1 results, ADL rolls the platform across all portfolio companies. Third company onwards: 20% discount.","$90K per add. company"),
        ("Exit Preparation Sprint","As portfolio companies approach exit (Year 4–6), ADL prepares the leadership narrative for buyer due diligence. Clean succession = higher valuation.","$80–120K per company"),
        ("Annual Intelligence Review","Recurring review comparing current state to Phase 1 baseline. Near-zero incremental cost once KB is built. LP-reportable outcome data.","$40–60K per year"),
        ("Sector-AI Certification","External 12-week programme for PE sector practitioners. Built on same infrastructure. Direct certification revenue on top of advisory.","$2.5–5K per person"),
    ]
    ec = st.columns(4)
    for col_e, e in zip(ec, expand):
        with col_e:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;padding:20px 16px;">
                <div style='font-size:13px;font-weight:700;color:{C['white']};margin-bottom:8px;'>{e[0]}</div>
                <p style='font-size:11px;margin:0 0 12px 0;line-height:1.5;'>{e[1]}</p>
                <div style='background:{C['blue']};color:white;font-size:12px;font-weight:700;
                    padding:6px 12px;border-radius:8px;'>{e[2]}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TALENT PYRAMID
# ══════════════════════════════════════════════════════════════════════════════
elif "Talent Pyramid" in page:
    page_header("Talent Pyramid Visualiser","Adjust team composition — see how the Diamond Pyramid differs from the traditional model")
    banner("ADL's pyramid base is already shrinking as AI automates analytical work. The Diamond Pyramid is the deliberate response — over-investing in the specialist middle where judgment cannot be automated.")

    col_ctrl, col_viz = st.columns([1,2])
    with col_ctrl:
        st.markdown(f"<p style='font-size:14px;font-weight:700;color:{C['white']};'>Traditional Model</p>",unsafe_allow_html=True)
        tp = st.slider("Partners (%)",5,20,10,key="tp")
        tm = st.slider("Managers (%)",15,40,25,key="tm")
        tc = st.slider("Consultants (%)",20,40,30,key="tc")
        ta = max(0,100-tp-tm-tc)
        st.markdown(f"<p style='color:{C['silver']};font-size:13px;'>Analysts: <strong style='color:{C['red']};'>{ta}%</strong> — largest layer</p>",unsafe_allow_html=True)
        st.divider()
        st.markdown(f"<p style='font-size:14px;font-weight:700;color:{C['white']};'>Diamond Model — ADL Proposed</p>",unsafe_allow_html=True)
        dp = st.slider("Partners (%)",5,20,10,key="dp")
        ds = st.slider("Domain Specialists (%)",25,55,40,key="ds",help="The widest layer — ADL over-invests here")
        dm = st.slider("AI Eng. Managers (%)",15,35,25,key="dm")
        dj = max(0,100-dp-ds-dm)
        st.markdown(f"<p style='color:{C['silver']};font-size:13px;'>KE + Juniors: <strong style='color:{C['gold']};'>{dj}%</strong> — smallest layer</p>",unsafe_allow_html=True)
        total = st.slider("Total team size:",10,200,50,step=5)

    with col_viz:
        fp = make_subplots(rows=1, cols=2)
        trad = [("Partners",tp,C["navy"]),("Managers",tm,C["blue"]),("Consultants",tc,C["teal"]),("Analysts",ta,C["red"])]
        diam = [("Partners",dp,C["navy"]),("AI Eng. Mgrs",dm,C["blue2"]),("Domain Specialists",ds,C["gold"]),("KE + Juniors",dj,C["teal"])]

        for i,(lbl,pct,col) in enumerate(trad):
            cnt = int(total*pct/100)
            fp.add_trace(go.Bar(x=[pct/4],y=[lbl],orientation="h",marker_color=col,
                text=f"{pct}% ({cnt})",textposition="inside",
                textfont=dict(color=C["white"],size=12,family="Inter"),
                showlegend=False,width=0.6),row=1,col=1)

        for i,(lbl,pct,col) in enumerate(diam):
            cnt = int(total*pct/100)
            fp.add_trace(go.Bar(x=[pct/4],y=[lbl],orientation="h",marker_color=col,
                text=f"{pct}% ({cnt})",textposition="inside",
                textfont=dict(color=C["bg"] if col==C["gold"] else C["white"],size=12,family="Inter"),
                showlegend=False,width=0.6),row=1,col=2)

        fp.update_layout(
            paper_bgcolor=C["bg"],plot_bgcolor=C["surface"],
            font=dict(family="Inter",color=C["silver"],size=13),
            height=400, showlegend=False, barmode="stack",
            margin=dict(l=20,r=20,t=70,b=20),
            annotations=[
                dict(text="Traditional Pyramid",x=0.22,y=1.08,xref="paper",yref="paper",
                    showarrow=False,font=dict(color=C["white"],size=15,family="Inter",weight="bold")),
                dict(text="◆ Diamond Pyramid — ADL Proposed",
                    x=0.78,y=1.08,xref="paper",yref="paper",
                    showarrow=False,font=dict(color=C["gold"],size=15,family="Inter")),
            ],
            xaxis=dict(showgrid=False,showticklabels=False,linecolor=C["border"]),
            xaxis2=dict(showgrid=False,showticklabels=False,linecolor=C["border"]),
            yaxis=dict(gridcolor=C["border"],linecolor=C["border"],tickfont=dict(color=C["silver"],size=12)),
            yaxis2=dict(gridcolor=C["border"],linecolor=C["border"],tickfont=dict(color=C["silver"],size=12)),
        )
        st.plotly_chart(fp, use_container_width=True, config=CFG)

        P,M,A,K = 280000,170000,125000,110000
        tc_cost = total*tp/100*P + total*tm/100*M + total*tc/100*A + total*ta/100*A
        dc_cost = total*dp/100*P + total*dm/100*M + total*ds/100*A*1.1 + total*dj/100*K
        diff = (dc_cost-tc_cost)/tc_cost*100

        mc1,mc2,mc3 = st.columns(3)
        with mc1: st.metric("Traditional Annual Cost",f"${tc_cost/1e6:.1f}M")
        with mc2: st.metric("Diamond Annual Cost",f"${dc_cost/1e6:.1f}M",f"{diff:+.1f}%")
        with mc3: st.metric("Domain Specialist Count",f"{int(total*ds/100)} people",f"Widest layer at {ds}%")

        insight(f"""With {total} total headcount, the Diamond model has <strong style='color:{C['gold']};'>{int(total*ds/100)} Domain Specialists ({ds}%)</strong> — the widest and most valuable layer. 
        The base shrinks to {dj}% because AI handles what analysts used to do. 
        ADL invests the savings into specialist depth that no AI can replicate.""")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: 90-DAY PILOT + ROADMAP
# ══════════════════════════════════════════════════════════════════════════════
elif "90-Day Pilot" in page:
    page_header("90-Day Pilot + 18-Month Roadmap","From pilot approval to a self-sustaining PE vertical practice")
    banner("ADL leadership does not need to approve a five-year transformation today. Three decisions unlock a 90-day pilot that produces a go/no-go answer — with real data, real clients, real outcomes.")

    section("THE 90-DAY PILOT")
    zones = [
        {"days":"Days 1–30","head":"Select + Deploy","color":C["gold"],
         "items":["Appoint PE Practice Lead (existing partner or new hire)","Identify one UK or DACH PE relationship from ADL's existing client base","Select one portfolio company with post-acquisition leadership need","Deploy Phase 1 AI Talent Diagnostic","Baseline: time-to-insight vs traditional engagement"]},
        {"days":"Days 31–60","head":"Build + Test","color":C["blue2"],
         "items":["Knowledge Engineer begins retroactive KB build from 250+ ADL PE transaction archive","First RAG retrieval tested against Phase 1 diagnostic outputs","Azure AI infrastructure scoped and extended","Technical scoping document delivered by IT + Head of Data Science (Emilio)","Domain Specialist Analyst recruitment opened in parallel"]},
        {"days":"Days 61–90","head":"Present + Decide","color":C["green"],
         "items":["Phase 1 results presented to PE client","7 KPIs assessed against go/no-go thresholds","PE client expresses Phase 2 interest (or not)","ADL leadership receives go/no-go recommendation","Year 1 full launch plan approved if pilot succeeds"]},
    ]

    pc = st.columns(3)
    for col_z, z in zip(pc, zones):
        with col_z:
            st.markdown(f"""
            <div style="border:1px solid {z['color']};border-top:4px solid {z['color']};
                border-radius:14px;background:{C['glass']};padding:20px;height:100%;">
                <div style="background:{z['color']};color:{C['bg']};font-size:11px;font-weight:700;
                    padding:4px 12px;border-radius:20px;display:inline-block;margin-bottom:10px;
                    letter-spacing:1px;">{z['days']}</div>
                <div style="font-size:16px;font-weight:700;color:{C['white']};margin-bottom:14px;">{z['head']}</div>
                {''.join([f'<div style="display:flex;gap:8px;margin:6px 0;"><span style="color:{z["color"]};font-size:11px;flex-shrink:0;margin-top:2px;">▸</span><span style="font-size:12px;color:{C["silver"]};line-height:1.5;">{item}</span></div>' for item in z['items']])}
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    section("THE THREE DECISIONS ADL LEADERSHIP MUST MAKE")
    asks_d = [
        ("1","Approve PE Practice Lead Hire","One hire — existing partner taking it on or external specialist. Without a named owner, the pilot has no accountable individual. This is the single most important decision.",C["gold"]),
        ("2","Allocate $300–500K Platform Budget","Extend existing Azure AI infrastructure for diagnostic platform and RAG layer build. 60–70% of required architecture already exists from the Microsoft Azure deployment.",C["blue2"]),
        ("3","Authorise the 90-Day Pilot","One existing PE client relationship. One portfolio company. 90 days. A go/no-go decision at the end — not a five-year commitment.",C["green"]),
    ]
    ac = st.columns(3)
    for col_a2, a in zip(ac, asks_d):
        with col_a2:
            st.markdown(f"""
            <div class="glass-card" style="border-top:3px solid {a[3]};text-align:center;padding:24px;">
                <div style="width:44px;height:44px;background:{a[3]};border-radius:50%;
                    font-size:20px;font-weight:800;color:{C['bg']};
                    display:flex;align-items:center;justify-content:center;margin:0 auto 12px;">{a[0]}</div>
                <div style="font-size:14px;font-weight:700;color:{C['white']};margin-bottom:8px;">{a[1]}</div>
                <p style="font-size:12px;margin:0;">{a[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    section("18-MONTH IMPLEMENTATION ROADMAP")
    phases_r = [
        {"phase":"Phase 1","period":"Months 1–3","label":"Pilot & Prove","color":C["gold"],
         "milestones":["PE Practice Lead appointed (Week 1)","Pilot client selected (Week 2)","Phase 1 diagnostic delivered (Weeks 2–4)","KB build begins (Month 2)","90-day gate review (Month 3)"],"gate":"Go/no-go for Year 1 launch"},
        {"phase":"Phase 2","period":"Months 4–12","label":"Build & Scale","color":C["blue2"],
         "milestones":["3 Domain Specialist Analysts hired (Month 4)","First Phase 2 engagement launched (Month 5)","2nd PE firm onboarded (Month 6)","Sector-AI Certification curriculum designed (Month 8)","Year 1 gate review (Month 12)"],"gate":"Year 2 geographic expansion approved"},
        {"phase":"Phase 3","period":"Months 13–18","label":"Expand & Institutionalise","color":C["green"],
         "milestones":["Nordics expansion launched (Month 13)","First Phase 3 retainers signed (Month 14)","Sector-AI Certification launched externally (Month 15)","Knowledge Engineer 2 hired (Month 16)","Year 2 plan confirmed (Month 18)"],"gate":"PE vertical self-sustaining practice"},
    ]

    for ph in phases_r:
        st.markdown(f"""
        <div class="glass-card" style="border-left:4px solid {ph['color']};padding:18px 22px;margin:8px 0;">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:10px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div style="background:{ph['color']};color:{C['bg']};font-size:11px;font-weight:800;
                        padding:4px 12px;border-radius:20px;letter-spacing:1px;">{ph['phase']}</div>
                    <div>
                        <div style="font-size:15px;font-weight:700;color:{C['white']};line-height:1;">{ph['label']}</div>
                        <div style="font-size:11px;color:{C['silver']};margin-top:2px;">{ph['period']}</div>
                    </div>
                </div>
                <div style="font-size:12px;color:{ph['color']};font-weight:600;font-style:italic;">Gate: {ph['gate']}</div>
            </div>
            <div style="display:flex;gap:16px;flex-wrap:wrap;">
                {''.join([f'<div style="display:flex;gap:6px;align-items:flex-start;"><span style="color:{ph["color"]};font-size:11px;margin-top:2px;">●</span><span style="font-size:12px;color:{C["silver"]};">{m}</span></div>' for m in ph['milestones']])}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: AI ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════
elif "AI Architecture" in page:
    page_header("AI Operating Architecture","Build vs partner vs buy — and how data governance protects client trust")
    banner("60–70% of the required AI infrastructure already exists at ADL through the Microsoft Azure deployment. The key investment is the RAG knowledge layer — the proprietary component that makes ADL's AI categorically different from any competitor using the same Azure tools.")

    section("BUILD vs PARTNER vs BUY — FIVE DECISIONS")
    decisions = [
        {"comp":"Foundation LLM","decision":"USE EXISTING","color":C["green"],
         "why":"Already deployed at ADL (Microsoft 2023). 50% meeting prep reduction confirmed.",
         "spec":"GPT-4o via Azure OpenAI. EU data residency for GDPR. No new vendor relationship required."},
        {"comp":"RAG Knowledge Base","decision":"BUILD (Internal)","color":C["red"],
         "why":"This IS ADL's competitive moat. Cannot be outsourced — 250+ PE engagements are proprietary.",
         "spec":"Azure AI Search as vector database. Knowledge Engineer structures the archive. Tags by sector, geography, deal type, outcome, risk category."},
        {"comp":"4-Layer Decomposition Tooling","decision":"BUILD (Lightweight)","color":C["amber"],
         "why":"Custom quality workflow — not available off-shelf as ADL-specific validation process.",
         "spec":"Validation checklist embedded in engagement workflow. Audit trail with timestamp and validator name. Build time: 6–8 weeks on existing Azure."},
        {"comp":"Client Dashboard & Reporting","decision":"PARTNER","color":C["blue2"],
         "why":"Client-facing reporting does not need to be proprietary. Speed to market > ownership.",
         "spec":"Power BI embedded (existing Microsoft licence). KPI dashboards for PE board reporting. No additional vendor cost."},
        {"comp":"Certification Platform","decision":"PARTNER","color":C["blue2"],
         "why":"Professional certification delivery is a solved problem. Focus on content, not platform.",
         "spec":"Teachable or Kajabi for course delivery. ADL-designed assessment. Certificate issued by ADL. Platform cost: ~$20K/year."},
    ]

    for d in decisions:
        dc1, dc2, dc3 = st.columns([2,1,3])
        with dc1: st.markdown(f"<p style='font-size:14px;font-weight:600;color:{C['white']};margin:0;'>{d['comp']}</p><p style='font-size:12px;color:{C['silver']};margin:0;'>{d['why']}</p>",unsafe_allow_html=True)
        with dc2: st.markdown(f"<span style='background:{d['color']};color:{C['bg']};font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;display:inline-block;margin-top:8px;'>{d['decision']}</span>",unsafe_allow_html=True)
        with dc3: st.markdown(f"<p style='font-size:12px;color:{C['silver']};margin:8px 0;'>{d['spec']}</p>",unsafe_allow_html=True)
        st.markdown(f"<div style='border-bottom:1px solid {C['border']};margin:4px 0;'></div>",unsafe_allow_html=True)

    st.divider()
    col_gov, col_trust = st.columns(2)

    with col_gov:
        section("DATA GOVERNANCE — 6 RULES")
        rules = [
            ("Client data stays client data","Raw engagement data — financials, assessments, KPIs — belongs to the PE firm. ADL does not retain it after engagement completion."),
            ("Anonymised patterns feed the KB","Only anonymised, aggregated patterns enter ADL's knowledge base. No company names, no personal data, no financial figures."),
            ("IP ownership of outputs","All reports and dashboards are owned by the client. ADL retains the methodology — the 4-Layer framework and assessment approach."),
            ("Conflict of interest protocol","ADL cannot serve two competing PE funds in the same deal simultaneously. A conflict register is maintained by the PE Practice Lead."),
            ("GDPR compliance","All data processed within EU Azure region. Management assessment data requires explicit consent. Retention: engagement duration + 12 months."),
            ("Audit trail","Every AI output and 4-Layer validation logged with timestamp and validator. Available for client inspection within 10 business days."),
        ]
        for i,(head,body) in enumerate(rules):
            st.markdown(f"""
            <div style="display:flex;gap:12px;padding:10px 0;border-bottom:1px solid {C['border']};">
                <div style="background:{C['blue']};color:white;font-size:11px;font-weight:700;
                    width:24px;height:24px;border-radius:50%;display:flex;align-items:center;
                    justify-content:center;flex-shrink:0;margin-top:1px;">{i+1}</div>
                <div><div style="font-size:13px;font-weight:600;color:{C['white']};margin-bottom:2px;">{head}</div>
                <div style="font-size:12px;color:{C['silver']};">{body}</div></div>
            </div>
            """, unsafe_allow_html=True)

    with col_trust:
        section("CLIENT TRUST — 3 CONDITIONS TO SIGN")
        conditions = [
            ("Existing Relationship","Year 1 pilot engagements exclusively with PE firms who have worked with ADL previously. The trust is pre-established. No cold-selling in Year 1.",C["blue2"]),
            ("Data Security Clearance","PE firm's legal and procurement team reviews ADL's data handling protocol. Standard procurement response pack prepared in advance — not assembled per request.",C["amber"]),
            ("Professional Indemnity","Minimum $5M professional indemnity insurance. ADL's liability is for the methodology, not for client decisions made on the basis of the analysis.",C["gold"]),
        ]
        for c3, body, col2 in conditions:
            st.markdown(f"""
            <div class="glass-card" style="border-left:4px solid {col2};padding:16px 20px;margin:8px 0;">
                <div style="font-size:13px;font-weight:700;color:{col2};margin-bottom:6px;">{c3}</div>
                <p style="font-size:12px;margin:0;line-height:1.6;">{body}</p>
            </div>
            """, unsafe_allow_html=True)

        insight("""<strong style='color:#D97706;'>The most important legal question PE clients will ask:</strong> 
        Who owns the AI model trained on our data? The answer must be in the contract 
        before the engagement begins. ADL retains the methodology. The client retains their data. 
        Anonymised sector patterns only enter the knowledge base.""")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TALENT TRANSFORMATION
# ══════════════════════════════════════════════════════════════════════════════
elif "Talent Transformation" in page:
    page_header("Talent Transformation Plan","Role definitions, headcount evolution, and the reskilling pathway")
    banner("ADL is not replacing junior consultants. It is redefining what a junior consultant does and how they develop. The transformation happens through three parallel tracks: reskilling existing analysts, hiring domain specialists, and implementing the RAG apprenticeship as the structural development mechanism.")

    section("NEW ROLE DEFINITIONS")
    roles = [
        ("Partner","Sector Specialist","20–25% on PE vertical","Sector judgment, client relationship, quality sign-off. Utilisation reduced. Less time on analytical review. More time on positioning and business development.",C["navy"],C["blue2"]),
        ("AI Engagement Manager","New Role","100% on PE engagements","Owns the 4-Layer Decomposition quality gate. Manages team workflow. Bridges AI outputs and client communication. Promoted from strong Senior Consultant with technology affinity.",C["navy"],C["teal"]),
        ("Domain Specialist Analyst","Evolved Junior Role","100% on engagements","Sector-specific analysis and validation. Knowledge base curation. AI interrogation and quality checking. Hired from PE/Telecom/Energy industry. 5–8 years sector experience required.",C["navy"],C["gold"]),
        ("Knowledge Engineer","New Role","60% shared","RAG knowledge base maintenance. Engagement data structuring and tagging. Retrieval accuracy evaluation. Not client-billed — infrastructure investment. Technical + consulting hybrid profile.",C["navy"],C["green"]),
    ]
    rc = st.columns(4)
    for col_r, r in zip(rc, roles):
        with col_r:
            st.markdown(f"""
            <div style="background:{C['glass']};border:1px solid {r[5]};border-top:4px solid {r[5]};
                border-radius:12px;padding:18px;height:100%;">
                <div style="font-size:14px;font-weight:700;color:{C['white']};margin-bottom:2px;">{r[0]}</div>
                <div style="font-size:10px;background:{r[5]};color:{C['bg']};font-weight:700;
                    padding:2px 8px;border-radius:12px;display:inline-block;margin-bottom:8px;
                    letter-spacing:1px;">{r[1]}</div>
                <div style="font-size:11px;color:{r[5]};font-weight:600;margin-bottom:8px;">{r[2]}</div>
                <p style="font-size:11px;margin:0;line-height:1.6;">{r[3]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    section("HEADCOUNT EVOLUTION — 3 YEARS")
    hc_data = {
        "Role":["PE Practice Lead","AI Eng. Managers","Domain Specialists","Knowledge Engineers","Total New Hires"],
        "Year 1":[1,1,3,1,6],
        "Year 2":[1,3,8,2,14],
        "Year 3":[1,6,15,3,25],
    }
    hc_df2 = pd.DataFrame(hc_data)
    fhc = go.Figure()
    colors_hc = [C["gold"],C["teal"],C["blue2"],C["green"]]
    for i,role in enumerate(["AI Eng. Managers","Domain Specialists","Knowledge Engineers","PE Practice Lead"]):
        row = hc_df2[hc_df2["Role"]==role]
        if len(row):
            fhc.add_trace(go.Bar(name=role,x=["Year 1","Year 2","Year 3"],
                y=[row["Year 1"].values[0],row["Year 2"].values[0],row["Year 3"].values[0]],
                marker_color=colors_hc[i],text=[row["Year 1"].values[0],row["Year 2"].values[0],row["Year 3"].values[0]],
                textposition="inside",textfont=dict(color=C["white"],size=13,family="Inter")))
    chart(fhc,"Cumulative New Hires Required by Role and Year",h=340)
    fhc.update_layout(barmode="stack",legend=dict(orientation="h",y=-0.22,font=dict(size=12)))
    st.plotly_chart(fhc, use_container_width=True, config=CFG)

    st.divider()
    section("RESKILLING PATHWAY — EXISTING ANALYSTS")
    stages = [
        ("Stage 1","Months 1–2","AI Interrogation Bootcamp","40-hour structured programme. Prompt engineering, output validation, 4-Layer Decomposition in practice. Delivered by Knowledge Engineer with external AI training partner."),
        ("Stage 2","Months 3–4","Supervised KB Contribution","Analyst works alongside Knowledge Engineer to tag and structure 10–20 historical ADL engagements. Assessed on tagging accuracy and retrieval quality."),
        ("Stage 3","Months 5–8","Live Engagement Support","Analyst joins Phase 1 diagnostic team in a knowledge validation role. Bridges from generalist analyst to Domain Specialist track."),
        ("Stage 4","Month 9+","Full Transition or Voluntary Exit","Analyst confirms Domain Specialist profile (sector depth + AI skills) or chooses career transition. Natural attrition accepted for analysts who prefer traditional model."),
    ]
    sc = st.columns(4)
    for col_s, s in zip(sc, stages):
        with col_s:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;padding:18px 14px;">
                <div style="font-size:10px;font-weight:700;color:{C['blue2']};letter-spacing:2px;margin-bottom:4px;">{s[0]}</div>
                <div style="font-size:11px;color:{C['silver']};margin-bottom:8px;">{s[1]}</div>
                <div style="font-size:13px;font-weight:700;color:{C['white']};margin-bottom:10px;line-height:1.3;">{s[2]}</div>
                <p style="font-size:11px;margin:0;line-height:1.6;text-align:left;">{s[3]}</p>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: RISK + KPI SCORECARD
# ══════════════════════════════════════════════════════════════════════════════
elif "Risk + KPI" in page:
    page_header("Risk Register + KPI Scorecard","Known risks with planned responses, and how success is measured")
    banner("Every risk below was identified before the pilot begins — not discovered after. Every KPI has a go/no-go threshold so Day 90 is an objective decision, not a subjective one.")

    tab_r, tab_k = st.tabs(["⚠️ Risk Register","📊 KPI Scorecard"])

    with tab_r:
        risks = [
            ("Partner capacity constraint","One partner handles max 5 Phase 1 diagnostics/yr at 20% util.","HIGH","HIGH",
             "Size Year 1 plan around partner availability. Appoint PE Practice Lead before engagement 1. Begin hiring second sector partner if Year 1 is above conservative scenario.","PE Practice Lead","Monthly"),
            ("Domain Consultant hiring lead time","3–6 month recruitment cycle for specialist profiles.","HIGH","MEDIUM",
             "Open recruitment simultaneously with pilot launch — not after. Target mid-career PE/Telecom professionals, not business school graduates.","HR + PE Lead","Bi-weekly"),
            ("Knowledge base build slower than planned","Retroactive structuring of 250+ PE engagements is significant effort.","MEDIUM","HIGH",
             "KE dedicated from Day 1. Use live Phase 1 engagements to capture data in real time — every engagement feeds the KB simultaneously. Do not wait for retroactive build to complete.","Knowledge Engineer","Monthly"),
            ("First Phase 2 client does not convert","Phase 1 result does not generate sufficient confidence.","MEDIUM","HIGH",
             "Phase 1 diagnostic must quantify £-impact of identified leadership risks. 'Three succession gaps representing $X in EBITDA risk' justifies Phase 2. Make cost of inaction visible.","PE Practice Lead","At Phase 1 delivery"),
            ("ADL brand trust deficit","First PE client may be sceptical of ADL's AI capability.","HIGH","MEDIUM",
             "Launch only with an existing trusted ADL relationship. Phase 1 at $150K is low-risk enough for a trusted partner to say yes. The proof of concept IS the trust-builder.","PE Practice Lead","Before each pitch"),
            ("PE market cyclicality","Buyout deal volume volatile — fell 31% H1 2025.","MEDIUM","MEDIUM",
             "Target PE firms in mid-holding period (Years 2–5). Phase 3 retainer revenue is entirely uncorrelated with new deal volume.","PE Practice Lead","Quarterly"),
        ]

        likelihood_colors = {"HIGH":C["red"],"MEDIUM":C["amber"],"LOW":C["green"]}

        likelihood_colors = {"HIGH":C["red"],"MEDIUM":C["amber"],"LOW":C["green"]}
        for risk_name, detail, likelihood, impact, mitigation, owner, review in risks:
            lc = likelihood_colors.get(likelihood, C["silver"])
            ic = likelihood_colors.get(impact, C["silver"])
            st.markdown(f"""<div style="background:rgba(17,34,64,0.7);border:1px solid {C['border']};
                border-left:4px solid {lc};border-radius:12px;padding:16px 20px;margin:8px 0;">
                <p style="font-size:15px;font-weight:700;color:{C['white']};margin:0 0 6px 0;">{risk_name}</p>
                <span style="background:{lc}22;color:{lc};font-size:11px;font-weight:700;padding:2px 10px;border-radius:12px;">Likelihood: {likelihood}</span>
                <span style="background:{ic}22;color:{ic};font-size:11px;font-weight:700;padding:2px 10px;border-radius:12px;margin-left:4px;">Impact: {impact}</span>
                <p style="font-size:13px;color:{C['silver']};margin:8px 0;line-height:1.5;">{detail}</p>
                <p style="font-size:13px;color:{C['green']};margin:0 0 4px 0;"><strong>Mitigation:</strong> {mitigation}</p>
                <p style="font-size:11px;color:{C['muted']};margin:0;"><strong style='color:{C['silver']};'>Owner:</strong> {owner} &nbsp;·&nbsp; <strong style='color:{C['silver']};'>Review:</strong> {review}</p>
            </div>""", unsafe_allow_html=True)
    with tab_k:
        section("90-DAY PILOT SCORECARD — GO / NO-GO CRITERIA")
        kpis = [
            ("Phase 1 delivery time","8 weeks traditional","≤ 5 weeks","FAIL if > 6 weeks"),
            ("4-Layer quality score (internal)","No baseline (new)","≥ 7 / 10 average","FAIL if < 6 / 10"),
            ("PE client NPS (post-Phase 1)","Industry avg: 32","≥ 40 NPS","FAIL if < 30"),
            ("KB entries structured","0 (start of pilot)","≥ 50 PE engagements tagged","FAIL if < 30"),
            ("RAG retrieval accuracy","First test","≥ 70% rated 'relevant'","FAIL if < 55%"),
            ("Gross margin on Phase 1","Traditional: ~38%","≥ 60%","FAIL if < 45%"),
            ("PE client Phase 2 interest","N/A","Explicit verbal/written interest","FAIL if not expressed"),
        ]

        for kpi in kpis:
            name, baseline, target, threshold = kpi
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:2.5fr 1.5fr 2fr 2fr;gap:12px;
                padding:12px 16px;border-bottom:1px solid {C['border']};align-items:center;">
                <div style="font-size:13px;font-weight:600;color:{C['white']};">{name}</div>
                <div style="font-size:12px;color:{C['silver']};">{baseline}</div>
                <div style="font-size:12px;color:{C['green']};font-weight:600;">Target: {target}</div>
                <span style="background:{C['redl']};color:{C['red']};padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;display:inline-block;">{threshold}</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        section("ONGOING OPERATIONAL KPIs — QUARTERLY TRACKING")
        ongoing = [
            ("PRODUCTIVITY","Engagement duration","≤ 5 weeks by engagement 3","Per engagement"),
            ("PRODUCTIVITY","AI compression factor achieved","≥ 30% vs traditional","Per engagement"),
            ("PRODUCTIVITY","KB growth rate","≥ 20 engagements structured/month","Monthly"),
            ("MARGIN","Gross margin per engagement","≥ 65% by engagement 5","Per engagement"),
            ("MARGIN","Revenue vs base case scenario","Within ±20% of plan","Monthly"),
            ("MARGIN","Phase 1→2 conversion rate","≥ 35% rolling 12-month","Quarterly"),
            ("QUALITY","4-Layer first-pass rate","≥ 85% pass all 4 gates","Per engagement"),
            ("QUALITY","RAG retrieval accuracy","≥ 80% rated relevant","Monthly"),
            ("CLIENT TRUST","Client NPS","≥ 45 by Year 1 end","Per engagement"),
            ("CLIENT TRUST","Certification enrolment","200 enrolled cohort 1","Monthly post-launch"),
            ("CLIENT TRUST","ADL career search index","Score ≥ 5 by Month 18 (currently 0)","Quarterly"),
        ]
        cat_colors = {"PRODUCTIVITY":C["blue2"],"MARGIN":C["gold"],"QUALITY":C["teal"],"CLIENT TRUST":C["green"]}
        for cat, metric, target, freq in ongoing:
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:120px 2.5fr 2fr 1.5fr;gap:12px;
                padding:10px 16px;border-bottom:1px solid {C['border']};align-items:center;">
                <span style="background:{cat_colors[cat]}22;color:{cat_colors[cat]};padding:3px 8px;
                    border-radius:12px;font-size:10px;font-weight:700;letter-spacing:0.5px;text-align:center;">{cat}</span>
                <div style="font-size:12px;color:{C['white']};font-weight:500;">{metric}</div>
                <div style="font-size:12px;color:{C['green']};">{target}</div>
                <div style="font-size:11px;color:{C['silver']};">{freq}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: 4-LAYER VALIDATOR
# ══════════════════════════════════════════════════════════════════════════════
elif "4-Layer Validator" in page:
    page_header("4-Layer Decomposition Validator","Type any consulting statement — run it through ADL's quality gate")

    if not pitch_mode:
        banner("Every AI output at ADL passes four gates before a client sees it: Hypothesis (is the assumption sound?), Evidence (is the data real?), Source (is it credible?), Risk (what is being ignored?). This is what makes AI-augmented advisory defensible in a PE boardroom.")

    examples = {
        "Custom — type your own":"",
        "PE: 'The leadership team is well-positioned for the value creation plan.'":"The leadership team is well-positioned for the value creation plan.",
        "Strategy: 'AI will replace 40% of consulting jobs within 5 years.'":"AI will replace 40% of consulting jobs within 5 years.",
        "Finance: 'The target company's EBITDA margin improvement is sustainable.'":"The target company's EBITDA margin improvement is sustainable.",
        "HR: 'Hiring domain specialists will resolve ADL's talent pipeline problem.'":"Hiring domain specialists will resolve ADL's talent pipeline problem.",
        "Market: 'ADL should expand into all European markets simultaneously.'":"ADL should expand into all European markets simultaneously.",
    }

    sel_ex = st.selectbox("Load an example:",list(examples.keys()))
    stmt = st.text_area("Statement to validate:",value=examples[sel_ex],height=80,
        placeholder="Paste any consulting, strategy, or advisory statement here...")

    def validate(text):
        t = text.lower()
        vague = ["well-positioned","good","bad","important","significant","various","many","some","clearly","obviously","generally"]
        specific_w = ["because","since","data shows","measured by","specifically","percentage","rate","number","%"]
        evidence_w = ["data","survey","report","study","analysis","benchmark","n=","%","million","billion","source","research","found","shows"]
        source_w = ["according to","published","report","survey","study","mckinsey","bain","adl","harvard","nber","2024","2025","2026"]
        risk_w = ["however","but","risk","caveat","limitation","assumption","unless","may","might","could","not all","varies","depends"]

        v_cnt = sum(1 for w in vague if w in t)
        s_cnt = sum(1 for w in specific_w if w in t)
        e_cnt = sum(1 for w in evidence_w if w in t)
        has_num = any(c.isdigit() for c in text)
        src_cnt = sum(1 for w in source_w if w in t)
        r_cnt = sum(1 for w in risk_w if w in t)

        H = ("STRONG",3,"The statement makes a specific, testable claim with clear measurable language.") if s_cnt>=2 else \
            ("WEAK",1,f"Contains {v_cnt} vague qualifiers with no measurable claim. Define what 'well-positioned' means specifically.") if v_cnt>=2 else \
            ("MODERATE",2,"Partially specific. Add a measurable criterion that would allow you to confirm or disprove this claim.")

        E = ("PRESENT",3,"References data or quantitative evidence. Verify figures trace to a primary source.") if (e_cnt>=2 or has_num) else \
            ("MISSING",1,"No data, statistics, or research references detected. Every factual claim must trace to a source.") if e_cnt==0 else \
            ("WEAK",2,"Limited evidence signals. The statement makes a factual claim without clearly anchoring it to a dataset.")

        S = ("CITED & RECENT",3,"Source appears cited and recent. Verify it is primary — not a secondary aggregation.") if src_cnt>=2 else \
            ("NOT CITED",1,"No source attribution detected. A PE firm partner will ask: where does this come from?") if src_cnt==0 else \
            ("PARTIALLY CITED",2,"Some source signals detected but recency unclear. Confirm the source is within 18 months for fast-moving topics.")

        R = ("ACKNOWLEDGED",3,"Statement shows awareness of limitations or counterarguments. Strong advisory work.") if r_cnt>=2 else \
            ("BLIND SPOT",1,"No risks, limitations, or caveats acknowledged. Most common failure in AI-generated consulting output. What would make this wrong?") if r_cnt==0 else \
            ("PARTIAL",2,"Some risk awareness detected. Identify the most material counterargument — not just a peripheral caveat.")

        return {"Hypothesis":H,"Evidence":E,"Source":S,"Risk":R}

    if stmt and len(stmt)>10:
        if st.button("🔍 Run Validation",type="primary"):
            with st.spinner("Validating..."):
                time.sleep(0.6)
                res = validate(stmt)

            score_map = {"STRONG":3,"PRESENT":3,"CITED & RECENT":3,"ACKNOWLEDGED":3,
                         "MODERATE":2,"WEAK":2,"PARTIALLY CITED":2,"PARTIAL":2,
                         "MISSING":1,"NOT CITED":1,"BLIND SPOT":1}
            total = sum(score_map.get(v[0],1) for v in res.values())
            pct = total/12*100
            sc_color = C["green"] if pct>=75 else C["amber"] if pct>=50 else C["red"]
            sc_label = "PASSES — Defensible for client delivery" if pct>=75 else \
                       "FLAGGED — Requires revision before delivery" if pct>=50 else \
                       "REJECTED — Do not deliver in current form"

            st.markdown(f"""
            <div style="background:{C['glass']};border:2px solid {sc_color};border-radius:14px;
                padding:24px;text-align:center;margin:16px 0;">
                <div style="font-size:11px;color:{C['silver']};letter-spacing:2px;font-weight:700;">OVERALL SCORE</div>
                <div style="font-size:48px;font-weight:800;color:{sc_color};letter-spacing:-2px;">{total}/12</div>
                <div style="font-size:14px;font-weight:600;color:{sc_color};">{sc_label}</div>
            </div>
            """, unsafe_allow_html=True)

            gc = st.columns(4)
            colors_gate = {3:C["green"],2:C["amber"],1:C["red"]}
            for col_g,(gate_name,(status,score,explanation)) in zip(gc,res.items()):
                with col_g:
                    gc2 = colors_gate[score]
                    st.markdown(f"""
                    <div style="background:{C['glass']};border:1px solid {gc2};border-top:4px solid {gc2};
                        border-radius:12px;padding:18px;height:220px;">
                        <div style="font-size:10px;color:{C['silver']};font-weight:700;letter-spacing:2px;">GATE {list(res.keys()).index(gate_name)+1}</div>
                        <div style="font-size:15px;font-weight:700;color:{C['white']};margin:4px 0;">{gate_name}</div>
                        <span style="background:{gc2}22;color:{gc2};padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;">{status}</span>
                        <p style="font-size:11px;color:{C['silver']};margin-top:10px;line-height:1.6;">{explanation}</p>
                    </div>
                    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: RAG SIMULATOR
# ══════════════════════════════════════════════════════════════════════════════
elif "RAG Simulator" in page:
    page_header("RAG Knowledge Base Simulator","See the difference between generic AI and ADL's proprietary sector intelligence")

    if not pitch_mode:
        banner("RAG (Retrieval-Augmented Generation) first retrieves from ADL's private knowledge base of 250+ PE engagements, then generates an answer grounded in that specific experience. The client sees the quality. The system stays internal.")

    KB = [
        {"id":"PE-DE-001","title":"DACH Industrial — Leadership Succession Risk","sector":"PE","geo":"DACH","type":"Manufacturing","year":2023,
         "summary":"Post-acquisition diagnostic: founder dependency in 3 of 5 C-suite roles. Successor identified for CEO within 45 days. Accelerated succession programme complete in 90 days.","outcome":"Leadership continuity. EBITDA target met Month 6.","tags":["succession","founder risk","DACH","industrial","100-day"]},
        {"id":"PE-UK-002","title":"UK Healthcare — Digital Capability Gap Assessment","sector":"PE","geo":"UK","type":"Healthcare","year":2024,
         "summary":"AI talent mapping: 60% of senior managers lacked digital skills required by value creation plan. AI-personalised upskilling delivered across 3 layers.","outcome":"Digital KPIs achieved 2 months ahead of schedule.","tags":["digital","capability gap","UK","healthcare","upskilling"]},
        {"id":"PE-CH-004","title":"Swiss Financial Services — AI Readiness Diagnostic","sector":"PE","geo":"DACH","type":"Financial Services","year":2024,
         "summary":"Leadership assessed for AI-era readiness. Knowledge management gaps identified. RAG-based decision support piloted for investment committee.","outcome":"AI readiness: 28/100 → 71/100 in 6 months.","tags":["AI readiness","fintech","DACH","knowledge management"]},
        {"id":"PE-NL-005","title":"Dutch Logistics — Operational Leadership Acceleration","sector":"PE","geo":"Nordics","type":"Logistics","year":2023,
         "summary":"Rapid growth created thin middle management. 14 mid-level managers in 180-day acceleration programme.","outcome":"Operational KPIs +23%. Zero unplanned leadership departures.","tags":["growth","middle management","logistics","acceleration","Nordics"]},
        {"id":"PE-DE-006","title":"German Automotive — Exit Preparation Leadership Audit","sector":"PE","geo":"DACH","type":"Automotive","year":2024,
         "summary":"Pre-exit: 2 succession risks identified that would have flagged in buyer due diligence. Both resolved 8 months before planned exit.","outcome":"Clean leadership narrative. Multiple bidder process maintained.","tags":["exit","succession","DACH","automotive","valuation"]},
        {"id":"TELCO-001","title":"UK Telecom — Strategic AI Workforce Transition","sector":"Telecom","geo":"UK","type":"Telecoms","year":2025,
         "summary":"Operator transitioning 40% of analyst workforce to AI-augmented roles. RAG apprenticeship piloted. Domain-specialist hiring model designed.","outcome":"First 45 AI-augmented analysts operational in 4 months.","tags":["telecoms","reskilling","AI workforce","UK","RAG"]},
        {"id":"ENERGY-001","title":"Nordic Energy Transition — Leadership Capability Redesign","sector":"Energy","geo":"Nordics","type":"Energy","year":2024,
         "summary":"Utility transitioning fossil→renewable. Entirely new leadership competencies required. 180-day C-suite acceleration.","outcome":"New business unit staffed. CEO named externally in 60 days.","tags":["energy transition","renewable","Nordics","C-suite","reskilling"]},
        {"id":"PE-FR-003","title":"French Consumer — Post-Merger Integration Talent Risk","sector":"PE","geo":"France","type":"Consumer","year":2022,
         "summary":"34% voluntary turnover risk in first 6 months post-merger. Cultural misalignment identified. Retention programme designed.","outcome":"Turnover reduced to 8%. Integration on track Month 9.","tags":["merger","retention","France","consumer","culture"]},
    ]

    queries = {"Custom — type your own":"","Leadership risk in a DACH industrial acquisition":"leadership risk DACH industrial",
               "Succession planning UK portfolio company":"succession UK portfolio company",
               "AI readiness for PE portfolio":"AI readiness portfolio company",
               "Exit preparation and leadership audit":"exit preparation leadership audit",
               "Energy sector talent transformation":"energy transition leadership reskilling"}

    sel_q = st.selectbox("Choose a query:",list(queries.keys()))
    user_q = st.text_input("Your query:",value=queries[sel_q],
        placeholder="e.g. leadership succession risk in German manufacturing...")

    def search_kb(query, kb, n=3):
        qw = set(query.lower().split())
        scored = []
        for doc in kb:
            dw = set(" ".join(doc["tags"]+[doc["title"],doc["sector"],doc["geo"],doc["type"]]).lower().split())
            score = len(qw&dw)*12 + (2026-doc["year"])*-1.5 + np.random.randint(0,4)
            scored.append((score,doc))
        scored.sort(key=lambda x:x[0],reverse=True)
        return [(max(0.35,min(0.97,s/45)),d) for s,d in scored[:n]]

    def generic_response(query):
        q = query.lower()
        if "succession" in q or "leadership" in q: return "Leadership succession planning is a key priority for PE-backed companies. Research indicates founder dependency creates significant risk during ownership transitions. Best practice involves early identification of successors and structured development programmes aligned with the value creation plan."
        if "ai" in q or "readiness" in q: return "AI readiness varies significantly across organisations. Companies should assess current capabilities against future requirements and develop a structured adoption roadmap. Change management and talent development are critical enablers of successful AI integration."
        if "exit" in q: return "Exit preparation typically requires 12–18 months of focused preparation. Leadership stability and demonstrable operational improvements are key factors in achieving premium valuations. Companies should ensure succession plans are documented and succession candidates are visibly capable."
        if "energy" in q or "transition" in q: return "Energy transition requires significant organisational capability development. New competencies in renewable technologies, regulatory navigation, and stakeholder management are essential. Leadership teams must be retrained or replaced to deliver the new business model."
        return "This is an important strategic and organisational question. A comprehensive assessment of the specific situation, including stakeholder analysis, capability mapping, and market context, would be required to provide targeted recommendations."

    if user_q and len(user_q)>5:
        if st.button("🔍 Search ADL Knowledge Base",type="primary"):
            with st.spinner("Retrieving..."):
                time.sleep(0.9)
                results = search_kb(user_q, KB)
                generic = generic_response(user_q)

            col_gen, col_rag = st.columns(2)
            with col_gen:
                st.markdown(f"#### 🤖 Generic Azure AI")
                st.markdown(f"<p style='font-size:12px;color:{C['silver']};'>What any competitor using Azure OpenAI would produce</p>",unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background:{C['surface']};border:1px solid {C['red']};border-left:4px solid {C['red']};
                    border-radius:10px;padding:18px;margin:8px 0;">
                    <p style="font-size:13px;color:{C['silver']};line-height:1.7;margin:0;">{generic}</p>
                    <p style="font-size:11px;color:{C['red']};margin-top:12px;margin-bottom:0;font-weight:600;">
                    ⚠ Generic training data only. No ADL sector experience. No specific outcomes. 
                    Identical to any competitor using the same Azure tools.</p>
                </div>
                """, unsafe_allow_html=True)

            with col_rag:
                st.markdown(f"#### 🔷 ADL RAG-Augmented")
                st.markdown(f"<p style='font-size:12px;color:{C['silver']};'>Retrieves from ADL's 250+ PE engagement archive first</p>",unsafe_allow_html=True)
                top_r, top_d = results[0]
                st.markdown(f"""
                <div style="background:{C['surface']};border:1px solid {C['green']};border-left:4px solid {C['green']};
                    border-radius:10px;padding:18px;margin:8px 0;">
                    <div style="font-size:10px;color:{C['green']};font-weight:700;letter-spacing:1px;margin-bottom:4px;">
                    MATCH: {top_d['id']} — Relevance {top_r:.0%}</div>
                    <div style="font-size:14px;font-weight:700;color:{C['white']};margin-bottom:8px;">{top_d['title']}</div>
                    <p style="font-size:13px;color:{C['silver']};line-height:1.7;margin:0 0 10px 0;">{top_d['summary']}</p>
                    <p style="font-size:13px;color:{C['green']};margin:0;font-weight:600;">✓ Outcome: {top_d['outcome']}</p>
                    <p style="font-size:11px;color:{C['green']};margin-top:10px;margin-bottom:0;">
                    ✓ Grounded in real ADL engagement ✓ Specific measurable outcome ✓ Not available to any competitor</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"#### All Retrieved Engagements")
            for rel, doc in results:
                rc2 = C["green"] if rel>0.7 else C["amber"] if rel>0.5 else C["silver"]
                with st.expander(f"[{doc['id']}]  {doc['title']}  —  Relevance: {rel:.0%}"):
                    ec1,ec2,ec3,ec4 = st.columns(4)
                    for col_e,k in zip([ec1,ec2,ec3,ec4],["sector","geo","type","year"]):
                        with col_e: st.markdown(f"**{k.title()}:** {doc[k]}")
                    st.markdown(f"**Summary:** {doc['summary']}")
                    st.markdown(f"**Outcome:** ✓ {doc['outcome']}")
                    tags = " ".join([f'<span style="background:{C["blue"]}22;color:{C["blue2"]};padding:2px 8px;border-radius:10px;font-size:11px;margin:2px;display:inline-block;">#{t}</span>' for t in doc["tags"]])
                    st.markdown(tags, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ENGAGEMENT ECONOMICS
# ══════════════════════════════════════════════════════════════════════════════
elif "Engagement Economics" in page:
    page_header("Engagement Economics Simulator","Adjust assumptions — see margin improvement in real time")
    banner("The AI does not replace revenue. It improves economics. ADL delivers the same quality engagement in less time, with a leaner team, at a higher margin. The specialist premium more than offsets the AI investment.")

    col_l,col_r = st.columns(2)
    with col_l:
        st.markdown(f"<p style='font-size:14px;font-weight:600;color:{C['white']};margin-bottom:8px;'>Traditional Parameters</p>",unsafe_allow_html=True)
        tw = st.slider("Duration (weeks)",4,16,8)
        pr = st.slider("Partner rate ($/hr)",300,800,520,step=10)
        mr = st.slider("Manager rate ($/hr)",200,500,340,step=10)
        ar = st.slider("Analyst rate ($/hr)",150,350,220,step=10)
        na = st.slider("Number of analysts",1,4,2)
    with col_r:
        st.markdown(f"<p style='font-size:14px;font-weight:600;color:{C['white']};margin-bottom:8px;'>AI-Augmented Parameters</p>",unsafe_allow_html=True)
        comp = st.slider("AI time compression (%)",20,60,37,step=1,help="NBER 2023: 66% compression on analytical phases. Applied conservatively at 37%.")
        prem = st.slider("Specialist billing premium (%)",5,30,15,step=1,help="Premium over traditional rates — justified by AI-augmented quality and domain expertise.")
        incl_ke = st.checkbox("Include Knowledge Engineer (not billed to client)",value=True)

    HRS = 40
    aw = tw*(1-comp/100)
    t_rev = (tw*HRS*0.5*pr + tw*HRS*mr + tw*HRS*na*ar)
    ai_rev = max(t_rev*1.05, aw*HRS*0.5*pr*(1+prem/100) + aw*HRS*mr*(1+prem/100) + aw*HRS*ar*(1+prem/100))
    P,M,A,K = 280000,170000,125000,110000
    t_cost = P*(tw/52)*0.5 + M*(tw/52) + A*(tw/52)*na
    t_cost += t_cost*0.2 + tw*2500
    ai_cost = P*(aw/52)*0.5 + M*(aw/52) + A*1.1*(aw/52) + (K*(aw/52)*0.6 if incl_ke else 0)
    ai_cost += ai_cost*0.2 + aw*2000 + 5000
    t_mg = (t_rev-t_cost)/t_rev*100
    ai_mg = (ai_rev-ai_cost)/ai_rev*100

    def fmt(v):
        if v >= 1e6: return f"${v/1e6:.2f}M"
        if v >= 1e3: return f"${v/1e3:.0f}K"
        return f"${v:.0f}"

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.metric("Traditional Revenue", fmt(t_rev))
    with c2: st.metric("Traditional Cost",    fmt(t_cost))
    with c3: st.metric("Traditional Margin",  f"{t_mg:.1f}%")
    with c4: st.metric("AI Revenue",  fmt(ai_rev),  f"+{fmt(ai_rev-t_rev)}")
    with c5: st.metric("AI Cost",     fmt(ai_cost), f"-{fmt(t_cost-ai_cost)}")
    with c6: st.metric("AI Margin",   f"{ai_mg:.1f}%", f"+{ai_mg-t_mg:.1f}pp")

    if not pitch_mode: src("Billing rates: GSA Federal Schedule 2024. Salaries: Management Consulted 2026. AI compression: NBER Brynjolfsson et al. 2023 (WP31161).")
    col_a,col_b = st.columns(2)
    cats = ["Partner","Manager","Analyst(s)","KE","Overhead","Travel"]
    tv = [P*(tw/52)*0.5,M*(tw/52),A*(tw/52)*na,0,(P*(tw/52)*0.5+M*(tw/52)+A*(tw/52)*na)*0.2,tw*2500]
    av = [P*(aw/52)*0.5,M*(aw/52),A*1.1*(aw/52),K*(aw/52)*0.6 if incl_ke else 0,
          (P*(aw/52)*0.5+M*(aw/52)+A*1.1*(aw/52))*0.2,aw*2000+5000]
    with col_a:
        fc = go.Figure()
        fc.add_trace(go.Bar(name="Traditional",x=cats,y=tv,marker_color=C["silver"],
            text=[f"${v:,.0f}" for v in tv],textposition="auto",textfont=dict(color=C["bg"],size=11,family="Inter")))
        fc.add_trace(go.Bar(name="AI-Augmented",x=cats,y=av,marker_color=C["blue2"],
            text=[f"${v:,.0f}" for v in av],textposition="auto",textfont=dict(color=C["white"],size=11,family="Inter")))
        chart(fc,"Cost Structure Breakdown ($)",h=340)
        fc.update_layout(barmode="group",legend=dict(orientation="h",y=-0.22,font=dict(size=12)))
        st.plotly_chart(fc, use_container_width=True, config=CFG)
    with col_b:
        fm = go.Figure()
        fm.add_trace(go.Bar(x=["Traditional","AI-Augmented"],y=[t_mg,ai_mg],
            marker_color=[C["silver"],C["gold"]],
            text=[f"{t_mg:.1f}%",f"{ai_mg:.1f}%"],textposition="outside",
            textfont=dict(color=C["white"],size=16,family="Inter"),width=0.45))
        fm.add_annotation(x=0.5,y=(t_mg+ai_mg)/2+2,
            text=f"<b>+{ai_mg-t_mg:.1f}pp</b>",showarrow=False,
            font=dict(color=C["gold"],size=18,family="Inter"))
        chart(fm,"Gross Margin Comparison",h=340)
        fm.update_yaxes(range=[0,max(t_mg,ai_mg)*1.45])
        st.plotly_chart(fm, use_container_width=True, config=CFG)

    insight(f"""AI-augmented delivery: <strong style='color:{C['gold']};'>{aw:.1f} weeks</strong> vs {tw} traditional ({comp}% compression). 
    Margin: <strong style='color:{C['red']};'>{t_mg:.1f}%</strong> → <strong style='color:{C['green']};'>{ai_mg:.1f}%</strong> 
    (+{ai_mg-t_mg:.1f} percentage points) on every single engagement.""")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: REVENUE SCENARIOS
# ══════════════════════════════════════════════════════════════════════════════
elif "Revenue Scenarios" in page:
    page_header("Revenue Scenario Model","Three-year trajectory — Private Equity vertical")
    banner("Three scenarios varying adoption pace, Phase 1→2 conversion, and geographic expansion. Pricing and cost structure are identical — only adoption speed changes.")

    c1,c2 = st.columns(2)
    with c1:
        p1p = st.slider("Phase 1 price ($K)",100,250,150,step=10)
        p2p = st.slider("Phase 2 price ($K)",250,600,385,step=15)
        p3p = st.slider("Phase 3 price ($K/yr)",150,400,250,step=10)
    with c2:
        cnv = st.slider("Phase 1→2 conversion (%)",10,70,35,step=5)
        cert = st.checkbox("Include Certification revenue",value=True)
        me = st.checkbox("Middle East expansion Year 2",value=False)

    scens = {
        "Conservative":{"firms":[2,5,9],"pf":[2,2.5,3],"conv":0.20,"col":C["red"]},
        "Base Case":{"firms":[3,7,12],"pf":[2,2.5,3],"conv":cnv/100,"col":C["blue2"]},
        "Aggressive":{"firms":[5,10,16],"pf":[2.5,3,4],"conv":0.50,"col":C["green"]},
    }
    YEARS = ["Year 1","Year 2","Year 3"]
    results = {}
    for name,sc in scens.items():
        yv = []
        for y in range(3):
            p1c = sc["firms"][y]*sc["pf"][y]; p2c = p1c*sc["conv"]; p3c = (p1c*sc["conv"]) if y>=1 else 0
            me_b = (sc["firms"][y]*0.3*p1p*1000) if (me and y>=1) else 0
            cr = ([1.5e6,3.5e6,5.5e6][y] if cert else 0)
            yv.append((p1c*p1p*1000+p2c*p2p*1000+p3c*p3p*1000+cr+me_b)/1e6)
        results[name] = yv

    rc1,rc2,rc3 = st.columns(3)
    for (name,vals),col_m in zip(results.items(),[rc1,rc2,rc3]):
        with col_m: st.metric(f"{name} — Year 3",f"${vals[2]:.1f}M",f"Y1: ${vals[0]:.1f}M")

    fr = go.Figure()
    for name,sc in scens.items():
        fr.add_trace(go.Scatter(x=YEARS,y=results[name],name=name,
            line=dict(color=sc["col"],width=3),
            mode="lines+markers+text",marker=dict(size=12,color=sc["col"]),
            text=[f"${v:.1f}M" for v in results[name]],
            textposition="top center",textfont=dict(color=sc["col"],size=13,family="Inter")))
    chart(fr,"3-Year Revenue Trajectory by Scenario ($M)",h=400)
    fr.update_yaxes(title_text="Revenue ($M)")
    fr.update_layout(legend=dict(orientation="h",y=-0.18,font=dict(size=13)))
    st.plotly_chart(fr, use_container_width=True, config=CFG)

    if not pitch_mode: src("Unit economics from D4. Pricing: Phase 1 $150K, Phase 2 $385K, Phase 3 $250K base. Bain Global PE Report 2026. ADL/Invest Europe European PE 2025.")
    insight(f"""<strong style='color:{C['gold']};'>Market context:</strong> 
    $414B European PE dry powder. 7-year avg holding period (Bain 2026). 
    94% of PE GPs prioritising AI. 32,000 unsold companies worth $3.8T. 
    ADL does not need market leadership — just a defensible boutique position.""")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: METHODOLOGY
# ══════════════════════════════════════════════════════════════════════════════
elif "Methodology" in page:
    page_header("Methodology","How every dataset was collected and what every term means")
    banner("All data self-collected by Team 15. No figures invented. Every number traces to a named source. This page is the evidence trail for the entire dashboard.")

    tab_d,tab_c,tab_g = st.tabs(["📥 Data Collection","📐 Key Calculations","📖 Glossary"])

    with tab_d:
        methods = [
            ("Google Trends (6 CSV files)","Python — pytrends library",
             "Custom Python scripts queried the Google Trends API for 87-month windows (Jan 2019 – Apr 2026). Queries: ADL career searches, firm comparisons, skill demand shifts, consulting vs AI job interest. Data normalised to 0–100 by Google."),
            ("Alumni Analysis (n=100)","Manual LinkedIn Review",
             "100 ADL alumni LinkedIn profiles reviewed and coded. Fields: join year, leave year, destination company, industry category, post-ADL role. Pre-AI cohort: joined before 2022. AI-era: joined 2022+. All publicly available data."),
            ("Firm Headcount (7 firms)","LinkedIn company pages",
             "LinkedIn company pages for 7 consulting firms. Junior analyst headcount vs total counted. Average junior ratio across firms: 38.8%."),
            ("Primary Interviews (4)","Direct outreach",
             "Person A: McKinsey Partner (ex-ADL) — 45 min structured interview. Person B: AT Kearney consultant — 30 min. MasterCard Senior Consultant — 30 min. ADL Junior Analyst — 20 min. All anonymised."),
        ]
        for name,method,desc in methods:
            st.markdown(f"""<div style="background:rgba(17,34,64,0.7);border:1px solid {C['border']};
                border-radius:12px;padding:16px 20px;margin:8px 0;">
                <p style="font-size:14px;font-weight:700;color:{C['white']};margin:0 0 4px 0;">
                    {name}&nbsp;<span style="color:{C['blue2']};font-weight:400;font-size:13px;">— {method}</span></p>
                <p style="font-size:13px;color:{C['silver']};margin:0;line-height:1.7;">{desc}</p>
            </div>""", unsafe_allow_html=True)
    with tab_c:
        calcs = [
            ("87 months zero ADL search","Counted rows where 'Arthur D Little careers' == 0 in career_search_trends.csv. Total rows: 88. Zero count: 87. Not filtered — this is the entire dataset."),
            ("69% tenure compression","Pre-AI avg: alumni with join date before 2022 (n=95). AI-era avg: join date 2022+ (n=5, directional). Formula: (AI-era avg − Pre-AI avg) / Pre-AI avg × 100."),
            ("47% → 70% gross margin","Traditional: 4-person team, 8 weeks, T&M billing (GSA Federal Schedule 2024). Revenue $333K, Cost $205K, Margin ~38%. AI-augmented: redesigned team, 5-week duration (37% compression from NBER 2023). Fixed fee $450K. Cost $138K. Margin ~69%."),
            ("$414B European PE dry powder","Direct figure from ADL State of European PE 2025 (6th ed., Invest Europe partnership, n=362). Not estimated."),
            ("94% of GPs prioritising AI","ADL European PE survey 2025, same report. New response category not present in prior editions."),
            ("7-year avg PE holding period","Bain Global PE Report 2026. Direct figure — not calculated. Supersedes 6-year figure from ADL 2025 report."),
        ]
        for name,explanation in calcs:
            insight(f"<strong style='color:{C['gold']};'>{name}</strong><br><span style='font-size:12px;'>{explanation}</span>")

    with tab_g:
        glossary = {
            "RAG — Retrieval-Augmented Generation":"A standard AI answers using only generic training data. A RAG system first retrieves relevant documents from a private knowledge base, then generates an answer grounded in that material. ADL's RAG uses 250+ PE engagements. Clients see better analysis. The system stays internal. This is ADL's competitive moat.",
            "Diamond Pyramid":"The traditional pyramid is wide at base (many juniors). As AI automates junior work, the base shrinks. A Diamond Pyramid is widest in the middle — where domain specialist judgment sits — because this layer cannot be automated. ADL deliberately over-invests here.",
            "4-Layer Decomposition":"ADL's quality gate: (1) Hypothesis — is the assumption sound? (2) Evidence — is the data real? (3) Source — is the source credible? (4) Risk — what is being ignored? Every AI output passes all four before a client sees it.",
            "Domain Specialist Analyst":"New junior hire profile. 5–8 years sector experience (PE/Telecom/Energy) plus AI interrogation skills. Recruited from industry not MBA programmes. Knows what a significant finding looks like in their sector — a generalist cannot.",
            "Knowledge Engineer":"New role maintaining ADL's RAG knowledge base. Decides what to capture, structures it for retrieval, evaluates accuracy. Not client-billed — infrastructure investment. Without this role the KB degrades rather than improves.",
            "Alumni Pipeline":"Former consultants become future clients. When development works, analysts leave after 4–7 years and buy consulting services. When the apprenticeship breaks down and analysts leave after 23 months with no real skills, this pipeline drains. Estimated value destroyed: $2.5M per cohort per year.",
        }
        for term,definition in glossary.items():
            st.markdown(f"""<div style="background:rgba(17,34,64,0.7);border:1px solid {C['border']};
                border-left:3px solid {C['blue2']};border-radius:0 12px 12px 0;padding:14px 18px;margin:6px 0;">
                <p style="font-size:14px;font-weight:700;color:{C['white']};margin:0 0 6px 0;">{term}</p>
                <p style="font-size:13px;color:{C['silver']};margin:0;line-height:1.7;">{definition}</p>
            </div>""", unsafe_allow_html=True)
# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.divider()
st.markdown(f"""<p style='text-align:center;color:{C["muted"]};font-size:11px;'>
Built by Husna Rafi for Arthur D. Little  ·  Hult MBA Capstone 2026  ·  hrafi@student.hult.edu  ·  CONFIDENTIAL
</p>""", unsafe_allow_html=True)
