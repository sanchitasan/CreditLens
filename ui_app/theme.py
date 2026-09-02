import streamlit as st


# ============================================================
# CreditLens Design System — "Refined Ledger"
# ============================================================

COLORS = {
    # Core Surfaces & Accents
    "paper": "#F4EFE6",
    "paper_raised": "#FCFAF5",
    "paper_card": "#FFFFFF",
    "paper_sidebar": "#EBE4D5",
    "rule": "#D4C8B0",
    "border_card": "#C9BDA2",
    "ink": "#1A1713",
    "ink_soft": "#524A3B",
    "ink_faint": "#8C8467",
    "accent": "#9E3D2E",
    # Status & Decision Colors
    "approve": "#2E6B38",
    "approve_bg": "#EBF4EC",
    "review": "#B37400",
    "review_bg": "#FEF6E6",
    "reject": "#A32D22",
    "reject_bg": "#FDF0ED",
}


def apply_theme():
    """Apply the CreditLens visual design system."""

    st.markdown(
        f"""
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

        /* =====================================================
           Global
           ===================================================== */

        .stApp {{
            background-color: {COLORS["paper"]};
            color: {COLORS["ink"]};
            font-family: 'IBM Plex Sans', sans-serif;
        }}

        .main .block-container {{
            max-width: 1200px;
            padding-top: 2.5rem;
            padding-bottom: 4rem;
            padding-left: 3.5rem;
            padding-right: 3.5rem;
        }}


        /* =====================================================
           Typography
           ===================================================== */

        h1, h2, h3 {{
            font-family: 'Source Serif 4', serif;
            color: {COLORS["ink"]};
            letter-spacing: -0.015em;
            font-weight: 600;
        }}

        h1 {{ font-size: 2.2rem; }}
        h2 {{ font-size: 1.55rem; border-bottom: 1.5px solid {COLORS["rule"]}; padding-bottom: 0.6rem; }}
        h3 {{ font-size: 1.2rem; }}

        p {{
            color: {COLORS["ink_soft"]};
            line-height: 1.6;
        }}

        [data-testid="stMetricValue"],
        [data-testid="stNumberInput"] input,
        .stTextInput input,
        code {{
            font-family: 'IBM Plex Mono', monospace !important;
        }}


        /* =====================================================
           Sidebar — Spacing & Styling
           ===================================================== */

        [data-testid="stSidebar"] {{
            background-color: {COLORS["paper_sidebar"]};
            border-right: 1.5px solid {COLORS["rule"]};
        }}

        /* Generous interior spacing */
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 2.5rem !important;
            padding-bottom: 2.5rem !important;
            padding-left: 1.75rem !important;
            padding-right: 1.75rem !important;
        }}

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {{
            color: {COLORS["ink"]};
        }}

        [data-testid="stSidebar"] hr {{
            border-color: {COLORS["rule"]};
            margin: 1.5rem 0 !important;
            opacity: 0.7;
        }}

        /* Styled Nav Options */
        [data-testid="stSidebar"] [role="radiogroup"] {{
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
            margin: 0.5rem 0 1.25rem 0;
        }}

        [data-testid="stSidebar"] [role="radiogroup"] label {{
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 0.95rem;
            color: {COLORS["ink_soft"]};
            background-color: transparent;
            padding: 0.65rem 0.9rem !important;
            border-radius: 6px;
            border: 1px solid transparent;
            transition: all 0.2s ease-in-out;
            cursor: pointer;
        }}

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
            background-color: rgba(212, 200, 176, 0.35);
            color: {COLORS["ink"]};
        }}

        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{
            background-color: {COLORS["paper_raised"]};
            color: {COLORS["accent"]} !important;
            border: 1px solid {COLORS["rule"]};
            font-weight: 600;
            box-shadow: 0 1px 4px rgba(26, 23, 19, 0.05);
        }}


/* =====================================================
   Application Cards
   ===================================================== */

[data-testid="stVerticalBlockBorderWrapper"] {{
    background-color: #FFFFFF !important;

    border: 1.5px solid #C9BDA2 !important;
    border-radius: 8px !important;

    box-shadow:
        0 2px 5px rgba(26, 23, 19, 0.10),
        0 8px 20px rgba(26, 23, 19, 0.08) !important;

    padding: 0.75rem !important;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        border-color 0.18s ease;
}}

[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    transform: translateY(-2px);

    border-color: #A99676 !important;

    box-shadow:
        0 4px 8px rgba(26, 23, 19, 0.12),
        0 12px 28px rgba(26, 23, 19, 0.10) !important;
}}

        /* Metric Cards */
        [data-testid="stMetric"] {{
            background-color: {COLORS["paper_raised"]};
            border: 1px solid {COLORS["rule"]};
            border-left: 4px solid {COLORS["accent"]};
            border-radius: 6px;
            padding: 1rem 1.2rem;
            box-shadow: 0 1px 3px rgba(26, 23, 19, 0.04);
        }}

        [data-testid="stMetricLabel"] {{
            color: {COLORS["ink_soft"]};
            font-size: 0.85rem;
            font-weight: 500;
        }}

        [data-testid="stMetricValue"] {{
            color: {COLORS["ink"]};
            font-weight: 600;
        }}
        /* =====================================================
           Form Inputs (Force Pure Black Text & Match Theme)
           ===================================================== */
        
        input, textarea {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }}

        [data-testid="stNumberInput"] input,
        .stTextInput input,
        [data-baseweb="base-input"] input,
        [data-baseweb="select"] > div {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            border-color: {COLORS["rule"]} !important;
            border-radius: 5px;
        }}

        [data-testid="stWidgetLabel"] p {{
            color: #000000 !important;
            font-size: 0.88rem;
            font-weight: 600;
        }}


/* =====================================================
   Buttons & Inputs
   ===================================================== */

.stButton > button {{
    border: 1.5px solid {COLORS["ink"]};
    border-radius: 5px;
    background-color: transparent;
    color: {COLORS["ink"]};
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 500;
    min-height: 2.5rem;
    transition: all 0.15s ease-in-out;
}}

.stButton > button:hover {{
    background-color: {COLORS["ink"]};
    border-color: {COLORS["ink"]};
    color: {COLORS["paper"]};
}}

.stButton > button,
.stFormSubmitButton > button {{
    border-radius: 5px;
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 500;
}}

.stButton > button[kind="primary"],
.stFormSubmitButton > button {{
    background-color: #822F22 !important;
    border: 1.5px solid #822F22 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button:hover {{
    background-color: #6F251B !important;
    border-color: #6F251B !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}
hr {{
    border-color: {COLORS["rule"]};
}}


        /* =====================================================
           Status Banners & Display Badges
           ===================================================== */

        .creditlens-status {{
            padding: 1.25rem 1.5rem;
            border-radius: 6px;
            border: 1px solid {COLORS["rule"]};
            border-left-width: 5px;
            margin-bottom: 1.25rem;
            box-shadow: 0 1px 3px rgba(26, 23, 19, 0.04);
        }}

        .creditlens-status-approve {{
            background-color: {COLORS["approve_bg"]};
            border-left-color: {COLORS["approve"]};
        }}
        .creditlens-status-review {{
            background-color: {COLORS["review_bg"]};
            border-left-color: {COLORS["review"]};
        }}
        .creditlens-status-reject {{
            background-color: {COLORS["reject_bg"]};
            border-left-color: {COLORS["reject"]};
        }}

        .creditlens-status-title {{
            font-family: 'Source Serif 4', serif;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }}

        .creditlens-status-approve .creditlens-status-title {{ color: {COLORS["approve"]}; }}
        .creditlens-status-review .creditlens-status-title {{ color: {COLORS["review"]}; }}
        .creditlens-status-reject .creditlens-status-title {{ color: {COLORS["reject"]}; }}

        .risk-badge {{
            display: inline-block;
            padding: 0.25rem 0.65rem;
            border-radius: 4px;
            border: 1px solid;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.75rem;
            font-weight: 600;
        }}

        .risk-low {{
            background-color: {COLORS["approve_bg"]};
            border-color: {COLORS["approve"]};
            color: {COLORS["approve"]};
        }}

        .risk-medium {{
            background-color: {COLORS["review_bg"]};
            border-color: {COLORS["review"]};
            color: {COLORS["review"]};
        }}

        .risk-high {{
            background-color: {COLORS["reject_bg"]};
            border-color: {COLORS["reject"]};
            color: {COLORS["reject"]};
        }}
        
        

        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Render the CreditLens application sidebar with refined margins and padding."""

    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 0.25rem 0 0.5rem 0; margin-bottom: 0.5rem;">
                <div style="
                    font-family: 'Source Serif 4', serif;
                    font-size: 1.55rem;
                    font-weight: 700;
                    color: {COLORS["ink"]};
                    letter-spacing: -0.02em;
                ">
                    CreditLens
                </div>
                <div style="
                    color: {COLORS["ink_soft"]};
                    font-size: 0.85rem;
                    margin-top: 0.25rem;
                    font-weight: 400;
                ">
                    Underwriting & Risk Desk
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.markdown(
            f"""<div style="
                font-size: 0.72rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: {COLORS["ink_faint"]};
                margin-bottom: 0.25rem;
                font-weight: 600;
            ">Navigation</div>""",
            unsafe_allow_html=True,
        )

        page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "New Application",
                "Applications",
            ],
            label_visibility="collapsed",
        )

        st.divider()

        st.markdown(
            f"""
            <div style="
                padding: 0.85rem 1rem;
                background-color: {COLORS["paper_raised"]};
                border: 1px solid {COLORS["rule"]};
                border-radius: 6px;
                margin-top: 1rem;
            ">
                <div style="color: {COLORS["ink"]}; font-size: 0.85rem; font-weight: 600;">
                    Local Engine
                </div>
                <div style="color: {COLORS["ink_soft"]}; font-size: 0.78rem; margin-top: 0.2rem;">
                    Active API Session
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return page


def render_page_header(title: str, subtitle: str | None = None):
    """Render a consistent CreditLens page header."""

    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <div style="margin-top: 0.35rem; color: {COLORS["ink_soft"]}; font-size: 0.95rem;">
            {subtitle}
        </div>
        """

    st.markdown(
        f"""
        <div style="margin-bottom: 1.75rem; padding-bottom: 1.25rem; border-bottom: 1.5px solid {COLORS["rule"]};">
            <div style="
                font-family: 'Source Serif 4', serif;
                font-size: 2.1rem;
                font-weight: 600;
                letter-spacing: -0.015em;
                color: {COLORS["ink"]};
            ">
                {title}
            </div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_risk_badge(risk_level: str):
    """Render a visual risk-level badge with contrast tint."""

    risk = risk_level.upper()
    css_class = {
        "LOW": "risk-low",
        "MEDIUM": "risk-medium",
        "HIGH": "risk-high",
    }.get(risk, "risk-medium")

    st.markdown(
        f'<span class="risk-badge {css_class}">{risk} RISK</span>',
        unsafe_allow_html=True,
    )


def render_decision_status(decision: str, risk_level: str, reason: str):
    """Render the primary lending decision banner."""

    decision = decision.upper()

    if decision == "APPROVE":
        css_class = "creditlens-status-approve"
        title = "Approved"
    elif decision == "MANUAL_REVIEW":
        css_class = "creditlens-status-review"
        title = "Manual Review Required"
    elif decision == "REJECT":
        css_class = "creditlens-status-reject"
        title = "Application Rejected"
    else:
        css_class = "creditlens-status-review"
        title = decision

    st.markdown(
        f"""
        <div class="creditlens-status {css_class}">
            <div class="creditlens-status-title">{title}</div>
            <div style="font-size: 0.92rem; font-weight: 500; margin-bottom: 0.2rem; color: {COLORS["ink"]};">
                Classification: {risk_level} Risk
            </div>
            <div style="font-size: 0.88rem; color: {COLORS["ink_soft"]};">
                {reason}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )