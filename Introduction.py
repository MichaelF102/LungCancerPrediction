import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="FMCG Market Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
)

# -----------------------------------------------------------------------------
# CUSTOM CSS STYLING
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
    /* Main Hero Header */
    .hero-header {
        font-size: 2.6rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.2rem;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.15rem;
        color: #94a3b8;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* Section Banner Box */
    .asterix-banner {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid #3730a3;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    
    .asterix-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }
    
    .asterix-desc {
        font-size: 1.05rem;
        color: #cbd5e1;
        line-height: 1.6;
    }

    /* Feature Cards */
    .feature-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        border-color: #6366f1;
    }

    .feature-icon {
        font-size: 1.6rem;
        margin-bottom: 10px;
    }

    .feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 6px;
    }

    .feature-text {
        font-size: 0.88rem;
        color: #94a3b8;
        line-height: 1.45;
    }

    /* Tag Badges */
    .use-case-badge {
        display: inline-block;
        background: #1e293b;
        color: #38bdf8;
        border: 1px solid #0284c7;
        border-radius: 20px;
        padding: 6px 16px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px 2px;
    }

    .motto-footer {
        text-align: center;
        font-size: 1.1rem;
        font-weight: 600;
        color: #a855f7;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px dashed #334155;
    }
</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# HERO HEADER SECTION
# -----------------------------------------------------------------------------
st.markdown(
    "<div class='hero-header'>📊 FMCG Market Intelligence Dashboard</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='hero-subtitle'>Real-time insights into pricing strategies, SKU dynamics, and competitive benchmarking across India</div>",
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# ASTERIX INTELLIGENCE OVERVIEW BANNER
# -----------------------------------------------------------------------------
st.markdown(
    """
<div class='asterix-banner'>
    <div class='asterix-title'>🧠 Powered by Asterix Intelligence</div>
    <div class='asterix-desc'>
        <b>Asterix Intelligence</b> is an enterprise-grade FMCG data analytics platform built to transform fragmented retail execution data into strategic market clarity. It empowers analysts, category managers, and leadership teams to instantly track pricing dynamics, monitor competitor moves, and optimize product portfolios across key metro markets.
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# WHAT IT DOES - FEATURE GRID (6 CARDS)
# -----------------------------------------------------------------------------
st.markdown("### ⚡ Core Analytics Capabilities")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class='feature-card'>
            <div class='feature-icon'>📦</div>
            <div class='feature-title'>Category & Subcategory Intelligence</div>
            <div class='feature-text'>Deep-dive performance tracking across key categories including Biscuits, Confectionery, Bakery, and Salty Snacks.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class='feature-card'>
            <div class='feature-icon'>🏷️</div>
            <div class='feature-title'>Brand & Competitor Tracking</div>
            <div class='feature-text'>Identify market share concentration, portfolio depth, and competitive line extensions across top national players.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class='feature-card'>
            <div class='feature-icon'>💰</div>
            <div class='feature-title'>Pricing & Discount Analytics</div>
            <div class='feature-text'>Benchmark MRP Current vs. Retailer Price, promotional depth, and margin spreads to optimize revenue growth.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown(
        """
        <div class='feature-card'>
            <div class='feature-icon'>⚖️</div>
            <div class='feature-title'>SKU & Unit Economics</div>
            <div class='feature-text'>Evaluate pack size performance, unit pricing (₹/100g), and packaging tier distributions across single-serve to bulk formats.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col5:
    st.markdown(
        """
        <div class='feature-card'>
            <div class='feature-icon'>🏙️</div>
            <div class='feature-title'>Geographic Market Mapping</div>
            <div class='feature-text'>Compare pricing dynamics, product density, and regional preferences across metro centers like Mumbai, Delhi, and Bengaluru.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col6:
    st.markdown(
        """
        <div class='feature-card'>
            <div class='feature-icon'>📈</div>
            <div class='feature-title'>Launch & Trend Analytics</div>
            <div class='feature-text'>Track product launch activity over time with dynamic aggregation (Monthly, Quarterly, Yearly) and date range filtering.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# USE CASES & STRATEGIC VALUE
# -----------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🎯 Strategic Applications")

use_case_col1, use_case_col2 = st.columns([1.8, 1])

with use_case_col1:
    st.markdown(
        """
        <div>
            <span class='use-case-badge'>📊 Category & Market Research</span>
            <span class='use-case-badge'>🏢 Competitive Intelligence</span>
            <span class='use-case-badge'>💡 Price & Margin Optimization</span>
            <span class='use-case-badge'>📦 Packaging Format Strategy</span>
            <span class='use-case-badge'>📈 Revenue Management</span>
            <span class='use-case-badge'>🏙️ Regional Distribution Planning</span>
            <span class='use-case-badge'>💡 Shrinkflation, Offers & Health Insights</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with use_case_col2:
    st.info(
        "🚀 **Why Asterix Intelligence?**\n"
        "Bridges the gap between raw retail data and strategic decision-making to drive **faster market execution**, **smarter pricing**, and **stronger competitive positioning**."
    )

st.markdown(
    "<div class='motto-footer'>👉 <i>Asterix Intelligence — Turning Raw Retail Data into Strategic Market Action</i></div>",
    unsafe_allow_html=True,
)