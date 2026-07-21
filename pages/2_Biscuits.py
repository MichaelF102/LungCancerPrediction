
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="Asterix Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.6rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.2rem;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1f2937 !important;
        color: #d1d5db !important;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
        border: 1px solid #374151;
    }
    .stTabs [data-baseweb="tab"] p, .stTabs [data-baseweb="tab"] span, .stTabs [data-baseweb="tab"] div {
        color: #d1d5db !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #374151 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4f46e5 !important;
        border: 1px solid #6366f1 !important;
    }
    .stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] span, .stTabs [aria-selected="true"] div {
        color: #ffffff !important;
    }
    .filter-section {
        background: #f9fafb;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# ===================== DATA LOADING =====================
@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv('a120c.csv')
    # Clean and prepare data
    df['Date of Discovery'] = pd.to_datetime(df['Date of Discovery'], errors='coerce')
    df['Year-Month'] = df['Date of Discovery'].dt.to_period('M').astype(str)
    df['Quarter_Label'] = 'Q' + df['Quarter'].astype(str) + ' ' + df['Year'].astype(str)

    # Clean numeric columns
    df['MRP Current'] = pd.to_numeric(df['MRP Current'], errors='coerce')
    df['Retailer Price'] = pd.to_numeric(df['Retailer Price'], errors='coerce')
    df['Discount %'] = pd.to_numeric(df['Discount %'], errors='coerce')
    df['Retail Margin'] = pd.to_numeric(df['Retail Margin'], errors='coerce')
    df['SKU size current -(previous)'] = pd.to_numeric(df['SKU size current -(previous)'], errors='coerce')

    # Create price difference
    df['Price Gap'] = df['MRP Current'] - df['Retailer Price']

    # Clean discount (remove extreme outliers)
    df.loc[df['Discount %'] < 0, 'Discount %'] = np.nan
    df.loc[df['Discount %'] > 100, 'Discount %'] = np.nan

    # Month order
    month_order = ['January','February','March','April','May','June',
                   'July','August','September','October','November','December']
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

    return df

df = load_data()

# ===================== SIDEBAR FILTERS =====================
df_filtered = df[df["Category"] == "Biscuits"].copy()

# Ensure 'Date of Discovery' is in datetime format for the calendar picker
if "Date of Discovery" in df_filtered.columns:
    df_filtered["Date of Discovery"] = pd.to_datetime(
        df_filtered["Date of Discovery"], errors="coerce"
    )

with st.sidebar:
    st.image("https://img.icons8.com/color/96/shopping-cart-loaded--v1.png", width=60)
    st.title("🔍 Filters")

    with st.container():
        st.markdown("<div class='filter-section'>", unsafe_allow_html=True)

        # 📂 Sub Category Filter
        subcategories = sorted(df_filtered["Sub Category"].dropna().unique())
        selected_subcategories = st.multiselect(
            "📂 Sub Category", subcategories, default=subcategories
        )
        
        # 🏙️ City Filter
        cities = sorted(df_filtered["City"].dropna().unique())
        selected_cities = st.multiselect("🏙️ City", cities, default=cities)

        # 📆 Day Filter
        days = sorted(df_filtered["Day"].dropna().unique())
        selected_days = st.multiselect("📆 Day", days, default=days)

        # 🗓️ Month Filter
        months = sorted(df_filtered["Month"].dropna().unique())
        selected_months = st.multiselect("🗓️ Month", months, default=months)

        # 📅 Year Filter
        years = sorted(df_filtered["Year"].dropna().unique())
        selected_years = st.multiselect("📅 Year", years, default=years)

        # 📅 Date of Discovery Calendar Filter
        min_date = (
            df_filtered["Date of Discovery"].min().date()
            if not df_filtered["Date of Discovery"].isna().all()
            else datetime.date(2020, 1, 1)
        )
        max_date = (
            df_filtered["Date of Discovery"].max().date()
            if not df_filtered["Date of Discovery"].isna().all()
            else datetime.date.today()
        )

        selected_date_range = st.date_input(
            "📅 Date of Discovery Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        # 🏢 Company Name Filter (Option to select Top 30 or All Data)
        company_scope = st.radio(
            "🏢 Company Selection Scope",
            options=["Top 30", "All Data"],
            horizontal=True,
        )

        if company_scope == "Top 30":
            company_list = sorted(
                df_filtered["Company name"].value_counts().head(30).index.tolist()
            )
        else:
            company_list = sorted(df_filtered["Company name"].dropna().unique())

        selected_companies = st.multiselect(
            f"🏢 Company Name ({company_scope})",
            company_list,
            default=company_list,
        )

        

        # ⚡ Type of Change Filter
        change_types = sorted(df_filtered["Type of Change"].dropna().unique())
        selected_changes = st.multiselect(
            "⚡ Type of Change", change_types, default=change_types
        )

        # 📦 SKU Range Filter
        sku_ranges = sorted(df_filtered["SKU Range"].dropna().unique())
        selected_sku_ranges = st.multiselect(
            "📦 SKU Range", sku_ranges, default=sku_ranges
        )

        # 🏷️ Price Band Filter
        price_bands = sorted(df_filtered["Price Band"].dropna().unique())
        selected_price_bands = st.multiselect(
            "🏷️ Price Band", price_bands, default=price_bands
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("📊 FMCG Market Intelligence Dashboard v1.0")
    st.caption(f"Data refreshed: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

# 2. Applying all selected filters to the DataFrame
if len(selected_date_range) == 2:
    start_date, end_date = selected_date_range
    df_filtered = df_filtered[
        (df_filtered["City"].isin(selected_cities))
        & (df_filtered["Day"].isin(selected_days))
        & (df_filtered["Month"].isin(selected_months))
        & (df_filtered["Year"].isin(selected_years))
        & (
            df_filtered["Date of Discovery"].dt.date.between(
                start_date, end_date
            )
        )
        & (df_filtered["Company name"].isin(selected_companies))
        & (df_filtered["Sub Category"].isin(selected_subcategories))
        & (df_filtered["Type of Change"].isin(selected_changes))
        & (df_filtered["SKU Range"].isin(selected_sku_ranges))
        & (df_filtered["Price Band"].isin(selected_price_bands))
    ]

filtered_df = df_filtered

# ===================== HEADER =====================
st.markdown("<div class='main-header'>📊 FMCG Market Intelligence Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Real-time insights into product launches, pricing strategies & market trends across India</div>", unsafe_allow_html=True)

# ===================== KPI CARDS =====================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_products = len(filtered_df)
    st.metric("🛍️ Total Products", f"{total_products:,}", 
              delta=f"{len(df):,} total")

with col2:
    unique_brands = filtered_df['Brand name'].nunique()
    st.metric("🏷️ Unique Brands", f"{unique_brands:,}")

with col3:
    avg_discount = filtered_df['Discount %'].mean()
    st.metric("🏷️ Avg Discount", f"{avg_discount:.1f}%" if pd.notna(avg_discount) else "N/A")

with col4:
    avg_mrp = filtered_df['MRP Current'].mean()
    st.metric("💰 Avg MRP", f"₹{avg_mrp:.0f}" if pd.notna(avg_mrp) else "N/A")

with col5:
    avg_margin = filtered_df['Retail Margin'].mean()
    st.metric("📈 Avg Margin", f"₹{avg_margin:.0f}" if pd.notna(avg_margin) else "N/A")

st.markdown("---")

# ===================== TABS =====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Market Overview", 
    "💰 Pricing Analytics", 
    "🏙️ City Comparison",
    "🏷️ Brand Intelligence",
    "📦 SKU Analysis",
    "📋 Data Explorer"
])

# ===================== TAB 1: MARKET OVERVIEW =====================
with tab1:
    st.markdown("### 📈 Market Overview")

    # -----------------------------------------------------------------------------
    # 1. BAR CHARTS: Diversity across Subcategories
    # -----------------------------------------------------------------------------
    st.markdown("#### 🔍 Subcategory Diversity & Breadth")

    subcat_metrics = (
        filtered_df.groupby("Sub Category")
        .agg(
            Unique_Companies=("Company name", "nunique"),
            Unique_Brands=("Brand name", "nunique"),
            Unique_Variants=("Variant/Flavour", "nunique"),
        )
        .reset_index()
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        fig_comp = px.bar(
            subcat_metrics,
            x="Sub Category",
            y="Unique_Companies",
            title="🏢 Companies by Subcategory",
            color="Unique_Companies",
            color_continuous_scale="Blues",
            text="Unique_Companies",
        )
        fig_comp.update_layout(
            height=380, showlegend=False, xaxis_tickangle=-45, coloraxis_showscale=False
        )
        max_y1 = subcat_metrics["Unique_Companies"].max() if not subcat_metrics.empty else 10
        fig_comp.update_yaxes(range=[0, max_y1 * 1.25])
        fig_comp.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_comp, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Shows manufacturer participation density per subcategory. Higher counts indicate competitive markets.")

    with col2:
        fig_brand = px.bar(
            subcat_metrics,
            x="Sub Category",
            y="Unique_Brands",
            title="🏷️ Brands by Subcategory",
            color="Unique_Brands",
            color_continuous_scale="Teal",
            text="Unique_Brands",
        )
        fig_brand.update_layout(
            height=380, showlegend=False, xaxis_tickangle=-45, coloraxis_showscale=False
        )
        max_y2 = subcat_metrics["Unique_Brands"].max() if not subcat_metrics.empty else 10
        fig_brand.update_yaxes(range=[0, max_y2 * 1.25])
        fig_brand.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_brand, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Measures brand proliferation. Subcategories with high brand counts show strong brand fragmentation.")

    with col3:
        fig_var = px.bar(
            subcat_metrics,
            x="Sub Category",
            y="Unique_Variants",
            title="🎨 Variants by Subcategory",
            color="Unique_Variants",
            color_continuous_scale="Purples",
            text="Unique_Variants",
        )
        fig_var.update_layout(
            height=380, showlegend=False, xaxis_tickangle=-45, coloraxis_showscale=False
        )
        max_y3 = subcat_metrics["Unique_Variants"].max() if not subcat_metrics.empty else 10
        fig_var.update_yaxes(range=[0, max_y3 * 1.25])
        fig_var.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_var, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Highlights flavor and variant innovation breadth across subcategories.")

    # -----------------------------------------------------------------------------
    # 2. FREQUENCY DISTRIBUTION OF KEY MARKET ENTITIES
    # -----------------------------------------------------------------------------
    st.markdown("#### 🥧 Top Market Entities Distribution")

    entity_view = st.radio(
        "Select Presentation Style:",
        options=["📊 Horizontal Bar Chart (Recommended)", "🍩 Polished Donut Chart"],
        horizontal=True,
    )

    p_col1, p_col2, p_col3 = st.columns(3)

    if entity_view.startswith("📊"):
        with p_col1:
            top_companies = (
                filtered_df["Company name"]
                .value_counts()
                .head(10)
                .reset_index(name="Count")
                .sort_values(by="Count", ascending=True)
            )
            fig_bar_comp = px.bar(
                top_companies,
                x="Count",
                y="Company name",
                orientation="h",
                title="🏢 Top 10 Companies",
                color="Count",
                color_continuous_scale="Blues",
                text="Count",
            )
            fig_bar_comp.update_layout(
                height=450, showlegend=False, coloraxis_showscale=False,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            max_x1 = top_companies["Count"].max() if not top_companies.empty else 10
            fig_bar_comp.update_xaxes(range=[0, max_x1 * 1.25])
            fig_bar_comp.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(fig_bar_comp, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Top companies ranked by total product listings, showing market concentration among leaders.")

        with p_col2:
            top_brands = (
                filtered_df["Brand name"]
                .value_counts()
                .head(10)
                .reset_index(name="Count")
                .sort_values(by="Count", ascending=True)
            )
            fig_bar_brand = px.bar(
                top_brands,
                x="Count",
                y="Brand name",
                orientation="h",
                title="🏷️ Top 10 Brands",
                color="Count",
                color_continuous_scale="Teal",
                text="Count",
            )
            fig_bar_brand.update_layout(
                height=450, showlegend=False, coloraxis_showscale=False,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            max_x2 = top_brands["Count"].max() if not top_brands.empty else 10
            fig_bar_brand.update_xaxes(range=[0, max_x2 * 1.25])
            fig_bar_brand.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(fig_bar_brand, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Leading product brands by shelf presence and active variant volume.")

        with p_col3:
            top_variants = (
                filtered_df["Variant/Flavour"]
                .value_counts()
                .head(10)
                .reset_index(name="Count")
                .sort_values(by="Count", ascending=True)
            )
            fig_bar_var = px.bar(
                top_variants,
                x="Count",
                y="Variant/Flavour",
                orientation="h",
                title="🎨 Top 10 Variants / Flavours",
                color="Count",
                color_continuous_scale="Purples",
                text="Count",
            )
            fig_bar_var.update_layout(
                height=450, showlegend=False, coloraxis_showscale=False,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            max_x3 = top_variants["Count"].max() if not top_variants.empty else 10
            fig_bar_var.update_xaxes(range=[0, max_x3 * 1.25])
            fig_bar_var.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(fig_bar_var, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Most popular product flavors and variants reflecting consumer taste preferences.")
    else:
        with p_col1:
            top_companies = (
                filtered_df["Company name"]
                .value_counts()
                .head(10)
                .reset_index(name="Count")
            )
            fig_pie_comp = px.pie(
                top_companies,
                values="Count",
                names="Company name",
                title="🏢 Top 10 Companies",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Set3,
            )
            fig_pie_comp.update_traces(textposition="inside", textinfo="percent")
            fig_pie_comp.update_layout(
                height=450,
                legend=dict(orientation="h", y=-0.1, font=dict(size=10)),
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig_pie_comp, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Relative market share representation among top 10 companies.")

        with p_col2:
            top_brands = (
                filtered_df["Brand name"]
                .value_counts()
                .head(10)
                .reset_index(name="Count")
            )
            fig_pie_brand = px.pie(
                top_brands,
                values="Count",
                names="Brand name",
                title="🏷️ Top 10 Brands",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig_pie_brand.update_traces(textposition="inside", textinfo="percent")
            fig_pie_brand.update_layout(
                height=450,
                legend=dict(orientation="h", y=-0.1, font=dict(size=10)),
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig_pie_brand, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Relative share distribution among leading consumer brands.")

        with p_col3:
            top_variants = (
                filtered_df["Variant/Flavour"]
                .value_counts()
                .head(10)
                .reset_index(name="Count")
            )
            fig_pie_var = px.pie(
                top_variants,
                values="Count",
                names="Variant/Flavour",
                title="🎨 Top 10 Variants / Flavours",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Safe,
            )
            fig_pie_var.update_traces(textposition="inside", textinfo="percent")
            fig_pie_var.update_layout(
                height=450,
                legend=dict(orientation="h", y=-0.1, font=dict(size=10)),
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig_pie_var, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Proportional volume contribution by flavor profile.")

    # -----------------------------------------------------------------------------
    # 3. COMPARATIVE PRICING ANALYSIS (Grouped Bar Chart & Toggle)
    # -----------------------------------------------------------------------------
    st.markdown("#### 💰 Pricing Analysis by Subcategory")

    price_mode = st.radio(
        "Select Pricing Metric View:",
        options=["Compare Both (MRP vs Retail Price)", "MRP Only", "Retail Price Only"],
        horizontal=True,
    )

    subcat_price = (
        filtered_df.groupby("Sub Category")
        .agg(
            Avg_MRP=("MRP Current", "mean"),
            Avg_RP=("Retailer Price", "mean"),
        )
        .reset_index()
    )

    fig_price = go.Figure()

    if price_mode in ["Compare Both (MRP vs Retail Price)", "MRP Only"]:
        fig_price.add_trace(
            go.Bar(
                x=subcat_price["Sub Category"],
                y=subcat_price["Avg_MRP"],
                name="Average MRP Current (₹)",
                marker_color="#6366f1",
                text=subcat_price["Avg_MRP"].round(1),
                textposition="outside",
            )
        )

    if price_mode in ["Compare Both (MRP vs Retail Price)", "Retail Price Only"]:
        fig_price.add_trace(
            go.Bar(
                x=subcat_price["Sub Category"],
                y=subcat_price["Avg_RP"],
                name="Average Retailer Price (₹)",
                marker_color="#10b981",
                text=subcat_price["Avg_RP"].round(1),
                textposition="outside",
            )
        )

    fig_price.update_layout(
        title="Average MRP vs. Retailer Price by Subcategory",
        barmode="group",
        xaxis_title="Subcategory",
        yaxis_title="Price (₹)",
        height=450,
        xaxis_tickangle=-35,
        legend=dict(orientation="h", y=1.1, x=0),
    )
    max_p1 = subcat_price[["Avg_MRP", "Avg_RP"]].max().max() if not subcat_price.empty else 100
    fig_price.update_yaxes(range=[0, max_p1 * 1.2])
    st.plotly_chart(fig_price, use_container_width=True)
    with st.expander("💡 Insights"):
        st.caption("Compares list price (MRP) against actual selling price (Retailer Price) per subcategory to reveal discounting margins.")

    # -----------------------------------------------------------------------------
    # 4. NEW PRODUCT LAUNCHES OVER TIME (Time Series Chart)
    # -----------------------------------------------------------------------------
    st.markdown("#### 🚀 Product Launch Trends")

    # AggregationGranularity Picker
    agg_choice = st.radio(
        "Select Time Horizon Aggregation:",
        options=["Monthly", "Quarterly", "Yearly"],
        horizontal=True,
    )

    if agg_choice == "Monthly":
        time_df = (
            filtered_df.groupby(["Year", "Month"])
            .size()
            .reset_index(name="Launches")
        )
        time_df["Time_Period"] = (
            time_df["Year"].astype(str) + " " + time_df["Month"].astype(str)
        )
    elif agg_choice == "Quarterly":
        if "Quarter" in filtered_df.columns:
            filtered_df["Quarter_Label"] = (
                filtered_df["Year"].astype(str)
                + " Q"
                + filtered_df["Quarter"].astype(str)
            )
            time_df = (
                filtered_df.groupby("Quarter_Label")
                .size()
                .reset_index(name="Launches")
            )
            time_df.rename(columns={"Quarter_Label": "Time_Period"}, inplace=True)
        else:
            time_df = (
                filtered_df.groupby("Year").size().reset_index(name="Launches")
            )
            time_df.rename(columns={"Year": "Time_Period"}, inplace=True)
    else:  # Yearly
        time_df = (
            filtered_df.groupby("Year").size().reset_index(name="Launches")
        )
        time_df["Time_Period"] = time_df["Year"].astype(str)

    fig_launches = px.line(
        time_df,
        x="Time_Period",
        y="Launches",
        title=f"New Product Activity ({agg_choice})",
        markers=True,
        text="Launches",
        color_discrete_sequence=["#ef4444"],
    )
    fig_launches.update_traces(textposition="top center")
    fig_launches.update_layout(height=420, xaxis_tickangle=-45, yaxis_title="Number of Launches")
    st.plotly_chart(fig_launches, use_container_width=True)
    with st.expander("💡 Insights"):
        st.caption("Tracks product introduction velocity and seasonal release peaks across selected time horizons.")

# ===================== TAB 2: PRICING ANALYTICS =====================
with tab2:
    st.markdown("### 💰 Pricing Analytics")

    # -----------------------------------------------------------------------------
    # CHART 1 & 2: Overview Distributions (Bar & Pie)
    # -----------------------------------------------------------------------------
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # 📊 Chart 1: Products Count by Price Band (Bar Chart)
        pb_counts = (
            filtered_df["Price Band"]
            .value_counts()
            .reset_index(name="Count")
            .rename(columns={"index": "Price Band"})
        )
        fig1 = px.bar(
            pb_counts,
            x="Price Band",
            y="Count",
            title="1. 🏷️ Product Count by Price Band",
            color="Count",
            color_continuous_scale="Viridis",
            text="Count",
        )
        fig1.update_layout(height=400, showlegend=False)
        max_pb = pb_counts["Count"].max() if not pb_counts.empty else 10
        fig1.update_yaxes(range=[0, max_pb * 1.2])
        fig1.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig1, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Distribution of SKUs across pricing tiers, highlighting volume concentration in mass vs premium brackets.")

    with row1_col2:
        # 🥧 Chart 2: Share of Price Bands (Pie Chart)
        fig2 = px.pie(
            pb_counts,
            values="Count",
            names="Price Band",
            title="2. 🥧 Market Share Breakdown by Price Band",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Proportional volume share contributed by each price band segment.")

    # -----------------------------------------------------------------------------
    # CHART 3 & 4: Subcategory Pricing & Margins (Bar & Double Bar)
    # -----------------------------------------------------------------------------
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        # 📊 Chart 3: Average MRP vs Retailer Price by Sub-Category (Grouped Bar Chart)
        subcat_price = (
            filtered_df.groupby("Sub Category")[["MRP Current", "Retailer Price"]]
            .mean()
            .reset_index()
            .sort_values("MRP Current", ascending=False)
        )

        fig3 = go.Figure()
        fig3.add_trace(
            go.Bar(
                x=subcat_price["Sub Category"],
                y=subcat_price["MRP Current"].round(1),
                name="Avg MRP (₹)",
                marker_color="#6366f1",
                text=subcat_price["MRP Current"].round(1),
                textposition="outside",
            )
        )
        fig3.add_trace(
            go.Bar(
                x=subcat_price["Sub Category"],
                y=subcat_price["Retailer Price"].round(1),
                name="Avg Retailer Price (₹)",
                marker_color="#10b981",
                text=subcat_price["Retailer Price"].round(1),
                textposition="outside",
            )
        )
        fig3.update_layout(
            title="3. 💵 Avg MRP vs. Retailer Price by Sub-Category",
            barmode="group",
            height=420,
            xaxis_tickangle=-35,
            legend=dict(orientation="h", y=1.1, x=0),
        )
        max_p3 = subcat_price[["MRP Current", "Retailer Price"]].max().max() if not subcat_price.empty else 100
        fig3.update_yaxes(range=[0, max_p3 * 1.2])
        st.plotly_chart(fig3, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Compares benchmark MRP against actual retailer realization across subcategories.")

    with row2_col2:
        # 📊 Chart 4: Average Retail Margin (₹) by Sub-Category (Bar Chart)
        if "Retail Margin" in filtered_df.columns:
            margin_subcat = (
                filtered_df.groupby("Sub Category")["Retail Margin"]
                .mean()
                .reset_index()
                .sort_values("Retail Margin", ascending=False)
            )
            fig4 = px.bar(
                margin_subcat,
                x="Sub Category",
                y="Retail Margin",
                title="4. 📈 Average Retailer Margin (₹) by Sub-Category",
                color="Retail Margin",
                color_continuous_scale="Purples",
                text=margin_subcat["Retail Margin"].round(1),
            )
            fig4.update_layout(
                height=420, showlegend=False, xaxis_tickangle=-35
            )
            max_m4 = margin_subcat["Retail Margin"].max() if not margin_subcat.empty else 10
            fig4.update_yaxes(range=[0, max_m4 * 1.2])
            fig4.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(fig4, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Average monetary margin retained per unit across subcategories.")

    # -----------------------------------------------------------------------------
    # CHART 5 & 6: Pricing Trends & Changes (Line & Horizontal Bar)
    # -----------------------------------------------------------------------------
    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        # 📈 Chart 5: Average Price Trend Over Time (Line Chart)
        price_trend = (
            filtered_df.groupby(["Year", "Month"])[
                ["MRP Current", "Retailer Price"]
            ]
            .mean()
            .reset_index()
        )
        price_trend["Period"] = (
            price_trend["Year"].astype(str) + " " + price_trend["Month"].astype(str)
        )

        fig5 = px.line(
            price_trend,
            x="Period",
            y=["MRP Current", "Retailer Price"],
            title="5. 📈 Average MRP and Retail Price Trend Over Time",
            markers=True,
            color_discrete_map={
                "MRP Current": "#8b5cf6",
                "Retailer Price": "#06b6d4",
            },
        )
        fig5.update_layout(
            height=400, xaxis_tickangle=-45, legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig5, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Tracks inflation, list price adjustments, and retail price movements over time.")

    with row3_col2:
        # 📊 Chart 6: Average MRP by Type of Change (Horizontal Bar Chart)
        change_price = (
            filtered_df.groupby("Type of Change")["MRP Current"]
            .mean()
            .reset_index()
            .sort_values("MRP Current", ascending=True)
        )
        fig6 = px.bar(
            change_price,
            y="Type of Change",
            x="MRP Current",
            orientation="h",
            title="6. ⚡ Average MRP by Type of Change",
            color="MRP Current",
            color_continuous_scale="Oranges",
            text=change_price["MRP Current"].round(1),
        )
        fig6.update_layout(height=400, showlegend=False)
        max_c6 = change_price["MRP Current"].max() if not change_price.empty else 100
        fig6.update_xaxes(range=[0, max_c6 * 1.25])
        fig6.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig6, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Average list price associated with specific product modifications (re-launch, grammage change, price hike).")

    # -----------------------------------------------------------------------------
    # CHART 7 & 8: Company & City Pricing Metrics (Bar Charts)
    # -----------------------------------------------------------------------------
    row4_col1, row4_col2 = st.columns(2)

    with row4_col1:
        # 📊 Chart 7: Top 10 Companies by Highest Average MRP (Bar Chart)
        top_comp_mrp = (
            filtered_df.groupby("Company name")["MRP Current"]
            .mean()
            .reset_index()
            .sort_values("MRP Current", ascending=False)
            .head(10)
        )
        fig7 = px.bar(
            top_comp_mrp,
            x="Company name",
            y="MRP Current",
            title="7. 🏢 Top 10 Companies by Average MRP (₹)",
            color="MRP Current",
            color_continuous_scale="Blugrn",
            text=top_comp_mrp["MRP Current"].round(1),
        )
        fig7.update_layout(
            height=400, showlegend=False, xaxis_tickangle=-45
        )
        max_c7 = top_comp_mrp["MRP Current"].max() if not top_comp_mrp.empty else 100
        fig7.update_yaxes(range=[0, max_c7 * 1.2])
        fig7.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig7, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Highest average price positioning among top FMCG manufacturers.")

    with row4_col2:
        # 📊 Chart 8: Average Discount % across Top Cities (Bar Chart)
        city_disc = (
            filtered_df.groupby("City")["Discount %"]
            .mean()
            .reset_index()
            .sort_values("Discount %", ascending=False)
            .head(10)
        )
        fig8 = px.bar(
            city_disc,
            x="City",
            y="Discount %",
            title="8. 🏙️ Top 10 Cities by Average Discount %",
            color="Discount %",
            color_continuous_scale="YlGnBu",
            text=city_disc["Discount %"].round(2),
        )
        fig8.update_layout(
            height=400, showlegend=False, xaxis_tickangle=-45
        )
        max_d8 = city_disc["Discount %"].max() if not city_disc.empty else 10
        fig8.update_yaxes(range=[0, max_d8 * 1.2])
        fig8.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig8, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("City-level promotional aggressiveness and retail discount depth.")

    # -----------------------------------------------------------------------------
    # CHART 9 & 10: SKU Range & Price Band Discount Deep Dives (Bar & Pie)
    # -----------------------------------------------------------------------------
    row5_col1, row5_col2 = st.columns(2)

    with row5_col1:
        # 📊 Chart 9: Average MRP by SKU Range (Bar Chart)
        if "SKU Range" in filtered_df.columns:
            sku_mrp = (
                filtered_df.groupby("SKU Range")["MRP Current"]
                .mean()
                .reset_index()
                .sort_values("MRP Current", ascending=False)
                .head(10)
            )
            fig9 = px.bar(
                sku_mrp,
                x="SKU Range",
                y="MRP Current",
                title="9. 📦 Average MRP by Top SKU Ranges (g/ml)",
                color="MRP Current",
                color_continuous_scale="Tealgrn",
                text=sku_mrp["MRP Current"].round(1),
            )
            fig9.update_layout(
                height=400, showlegend=False, xaxis_tickangle=-45
            )
            max_s9 = sku_mrp["MRP Current"].max() if not sku_mrp.empty else 100
            fig9.update_yaxes(range=[0, max_s9 * 1.2])
            fig9.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(fig9, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Price progression relative to pack size grammage brackets.")

    with row5_col2:
        # 📊 Chart 10: Average Discount % by Price Band (Bar Chart)
        avg_disc_pb = (
            filtered_df.groupby("Price Band")["Discount %"]
            .mean()
            .reset_index()
            .dropna()
            .sort_values("Discount %", ascending=False)
        )
        fig10 = px.bar(
            avg_disc_pb,
            x="Price Band",
            y="Discount %",
            color="Discount %",
            color_continuous_scale="RdYlGn",
            title="10. 🏷️ Average Discount % by Price Band",
            text=avg_disc_pb["Discount %"].round(2),
        )
        fig10.update_layout(height=400, showlegend=False)
        max_d10 = avg_disc_pb["Discount %"].max() if not avg_disc_pb.empty else 10
        fig10.update_yaxes(range=[0, max_d10 * 1.2])
        fig10.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig10, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Promotional discount sensitivity across low, mid, and premium price bands.")

# ===================== TAB 3: CITY COMPARISON =====================
with tab3:
    st.markdown("### 🏙️ City Comparison")

    # -----------------------------------------------------------------------------
    # ROW 1: Volume & Pricing Overview
    # -----------------------------------------------------------------------------
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # 📊 Chart 1: Total Product Volume by City (Bar Chart)
        city_counts = (
            filtered_df["City"]
            .value_counts()
            .reset_index(name="Count")
            .rename(columns={"index": "City"})
        )

        fig1 = px.bar(
            city_counts,
            x="City",
            y="Count",
            color="Count",
            color_continuous_scale="Viridis",
            title="1. 📍 Total Product Records by City",
            text="Count",
        )
        fig1.update_layout(
            height=400, showlegend=False, coloraxis_showscale=False
        )
        max_pb = pb_counts["Count"].max() if not pb_counts.empty else 10
        fig1.update_yaxes(range=[0, max_pb * 1.2])
        fig1.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig1, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Regional audit record volume across key metropolitan markets.")

    with row1_col2:
        # 📊 Chart 2: Average MRP vs. Retailer Price by City (Grouped Bar Chart)
        city_price = (
            filtered_df.groupby("City")[["MRP Current", "Retailer Price"]]
            .mean()
            .reset_index()
            .sort_values("MRP Current", ascending=False)
        )

        fig2 = go.Figure()
        fig2.add_trace(
            go.Bar(
                x=city_price["City"],
                y=city_price["MRP Current"].round(1),
                name="Avg MRP (₹)",
                marker_color="#6366f1",
                text=city_price["MRP Current"].round(1),
                textposition="outside",
            )
        )
        fig2.add_trace(
            go.Bar(
                x=city_price["City"],
                y=city_price["Retailer Price"].round(1),
                name="Avg Retail Price (₹)",
                marker_color="#10b981",
                text=city_price["Retailer Price"].round(1),
                textposition="outside",
            )
        )
        fig2.update_layout(
            title="2. 💰 Average MRP vs. Retail Price by City",
            barmode="group",
            height=400,
            legend=dict(orientation="h", y=1.1, x=0),
        )
        max_cp2 = city_price[["MRP Current", "Retailer Price"]].max().max() if not city_price.empty else 100
        fig2.update_yaxes(range=[0, max_cp2 * 1.2])
        st.plotly_chart(fig2, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("City-by-city price level variances and retail price realization.")

    # -----------------------------------------------------------------------------
    # ROW 2: Discounts & Market Competitiveness
    # -----------------------------------------------------------------------------
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        # 📊 Chart 3: Average Discount % by City (Bar Chart)
        city_disc = (
            filtered_df.groupby("City")["Discount %"]
            .mean()
            .reset_index()
            .sort_values("Discount %", ascending=False)
        )

        fig3 = px.bar(
            city_disc,
            x="City",
            y="Discount %",
            color="Discount %",
            color_continuous_scale="Blues",
            title="3. 🏷️ Average Promotional Discount % by City",
            text=city_disc["Discount %"].round(2),
        )
        fig3.update_layout(
            height=400, showlegend=False, coloraxis_showscale=False
        )
        fig3.update_traces(textposition="outside", cliponaxis=False)
        max_p3 = subcat_price[["MRP Current", "Retailer Price"]].max().max() if not subcat_price.empty else 100
        fig3.update_yaxes(range=[0, max_p3 * 1.2])
        st.plotly_chart(fig3, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Promotional discount intensity across different retail geographic zones.")

    with row2_col2:
        # 📊 Chart 4: Unique Companies & Brands per City (Grouped Bar Chart)
        city_diversity = (
            filtered_df.groupby("City")
            .agg(
                Companies=("Company name", "nunique"),
                Brands=("Brand name", "nunique"),
            )
            .reset_index()
            .sort_values("Brands", ascending=False)
        )

        fig4 = go.Figure()
        fig4.add_trace(
            go.Bar(
                x=city_diversity["City"],
                y=city_diversity["Companies"],
                name="Unique Companies",
                marker_color="#8b5cf6",
                text=city_diversity["Companies"],
                textposition="outside", cliponaxis=False,
            )
        )
        fig4.add_trace(
            go.Bar(
                x=city_diversity["City"],
                y=city_diversity["Brands"],
                name="Unique Brands",
                marker_color="#ec4899",
                text=city_diversity["Brands"],
                textposition="outside", cliponaxis=False,
            )
        )
        fig4.update_layout(
            title="4. 🏢 Market Competitiveness (Companies & Brands)",
            barmode="group",
            height=400,
            legend=dict(orientation="h", y=1.1, x=0),
        )
        max_cd4 = city_diversity[["Companies", "Brands"]].max().max() if not city_diversity.empty else 10
        fig4.update_yaxes(range=[0, max_cd4 * 1.2])
        st.plotly_chart(fig4, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Retail market fragmentation and supplier penetration per city.")

    # -----------------------------------------------------------------------------
    # ROW 3: Sub-Category Mix & Price Band Segmentation
    # -----------------------------------------------------------------------------
    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        # 🔥 Chart 5: Sub-Category Concentration Heatmap
        # Filter to top 8 sub-categories to keep heatmap readable
        top_subcats = (
            filtered_df["Sub Category"].value_counts().head(8).index.tolist()
        )
        subcat_filtered = filtered_df[
            filtered_df["Sub Category"].isin(top_subcats)
        ]
        city_subcat = pd.crosstab(
            subcat_filtered["City"], subcat_filtered["Sub Category"]
        )

        fig5 = px.imshow(
            city_subcat,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="YlOrRd",
            title="5. 🔥 Product Density: City × Top Sub-Categories",
        )
        fig5.update_layout(height=430)
        st.plotly_chart(fig5, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Regional consumption preference matrix across primary subcategories.")

    with row3_col2:
        # 📊 Chart 6: Price Band Preferences by City (100% Stacked Bar Chart)
        city_pb = (
            filtered_df.groupby(["City", "Price Band"], observed=False)
            .size()
            .reset_index(name="Count")
        )

        fig6 = px.bar(
            city_pb,
            x="City",
            y="Count",
            color="Price Band",
            title="6. 🎚️ Price Band Segmentation across Cities",
            color_discrete_sequence=px.colors.qualitative.Safe,
            barmode="stack",
        )
        fig6.update_layout(
            height=430, legend=dict(orientation="h", y=-0.25, x=0)
        )
        max_cp6 = city_pb.groupby("City")["Count"].sum().max() if not city_pb.empty else 10
        fig6.update_yaxes(range=[0, max_cp6 * 1.2])
        st.plotly_chart(fig6, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Price tier adoption and affordability profile per city.")

# ===================== TAB 4: BRAND INTELLIGENCE =====================
with tab4:
    st.markdown("### 🏷️ Brand Intelligence")

    # -----------------------------------------------------------------------------
    # ROW 1: Market Leaders Overview (Horizontal Bar Charts)
    # -----------------------------------------------------------------------------
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # 🏆 Chart 1: Top 20 Brands by Product Count
        top_brands = (
            filtered_df["Brand name"]
            .value_counts()
            .head(20)
            .reset_index(name="Count")
            .rename(columns={"index": "Brand"})
        )

        fig1 = px.bar(
            top_brands,
            y="Brand name",
            x="Count",
            orientation="h",
            color="Count",
            color_continuous_scale="Cividis",
            title="1. 🏆 Top 20 Brands by Product Count",
            text="Count",
        )
        fig1.update_layout(
            height=520, yaxis=dict(autorange="reversed"), showlegend=False
        )
        max_pb = pb_counts["Count"].max() if not pb_counts.empty else 10
        fig1.update_yaxes(range=[0, max_pb * 1.2])
        fig1.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig1, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Dominant brands ranked by total active SKU portfolio volume.")

    with row1_col2:
        # 🏢 Chart 2: Top 15 Companies by Product Count
        company_counts = (
            filtered_df["Company name"]
            .value_counts()
            .head(15)
            .reset_index(name="Count")
            .rename(columns={"index": "Company"})
        )

        fig2 = px.bar(
            company_counts,
            y="Company name",
            x="Count",
            orientation="h",
            color="Count",
            color_continuous_scale="Turbo",
            title="2. 🏢 Top 15 Companies by Product Count",
            text="Count",
        )
        fig2.update_layout(
            height=520, yaxis=dict(autorange="reversed"), showlegend=False
        )
        max_tc2 = company_counts["Count"].max() if not company_counts.empty else 10
        fig2.update_xaxes(range=[0, max_tc2 * 1.25])
        fig2.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig2, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Parent company market leadership ranked by combined brand portfolio size.")

    # -----------------------------------------------------------------------------
    # ROW 2: Brand Strategy & Portfolio Depth (Scatter & Bar)
    # -----------------------------------------------------------------------------
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        # 🎯 Chart 3: Brand Pricing Strategy (MRP vs. Discount %)
        brand_price = (
            filtered_df.groupby("Brand name")
            .agg(
                {
                    "MRP Current": "mean",
                    "Discount %": "mean",
                    "Brand name": "count",
                }
            )
            .rename(columns={"Brand name": "Product Count"})
            .reset_index()
            .dropna(subset=["MRP Current", "Discount %", "Product Count"])
        )
        # Filter for significant brands to reduce noise
        brand_price = (
            brand_price[brand_price["Product Count"] >= 10]
            .sort_values("Product Count", ascending=False)
            .head(25)
        )

        if not brand_price.empty:
            fig3 = px.scatter(
                brand_price,
                x="MRP Current",
                y="Discount %",
                size="Product Count",
                color="Brand name",
                title="3. 🎯 Brand Strategy: Avg Price vs. Avg Discount %",
                hover_data=["Brand name", "Product Count"],
            )
            fig3.update_layout(height=420, showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Strategic positioning matrix plotting premium price points against promotional discount depth.")
        else:
            st.info("No data available for Brand Strategy scatter plot.")

    with row2_col2:
        # 🎨 Chart 4: Brand Portfolio Depth (Unique Variants / Flavours per Brand)
        brand_variants = (
            filtered_df.groupby("Brand name")["Variant/Flavour"]
            .nunique()
            .reset_index()
            .sort_values("Variant/Flavour", ascending=False)
            .head(15)
        )

        fig4 = px.bar(
            brand_variants,
            x="Brand name",
            y="Variant/Flavour",
            title="4. 🎨 Portfolio Depth: Unique Variants/Flavours per Brand",
            color="Variant/Flavour",
            color_continuous_scale="Purples",
            text="Variant/Flavour",
        )
        fig4.update_layout(
            height=420, showlegend=False, xaxis_tickangle=-45
        )
        max_bv4 = brand_variants["Variant/Flavour"].max() if not brand_variants.empty else 10
        fig4.update_yaxes(range=[0, max_bv4 * 1.2])
        fig4.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig4, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Flavor innovation and SKU variety per brand.")

    # -----------------------------------------------------------------------------
    # ROW 3: Brand Pricing & Discount Rankings (Bar Charts)
    # -----------------------------------------------------------------------------
    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        # 💰 Chart 5: Top 10 Premium Brands (Highest Average MRP)
        # Filter brands with at least 5 products to avoid outliers
        valid_brands = (
            filtered_df["Brand name"]
            .value_counts()[lambda x: x >= 5]
            .index.tolist()
        )
        premium_brands = (
            filtered_df[filtered_df["Brand name"].isin(valid_brands)]
            .groupby("Brand name")["MRP Current"]
            .mean()
            .reset_index()
            .sort_values("MRP Current", ascending=False)
            .head(10)
        )

        fig5 = px.bar(
            premium_brands,
            x="Brand name",
            y="MRP Current",
            title="5. 💎 Top 10 Premium Brands by Average MRP (₹)",
            color="MRP Current",
            color_continuous_scale="Teal",
            text=premium_brands["MRP Current"].round(1),
        )
        fig5.update_layout(
            height=400, showlegend=False, xaxis_tickangle=-45
        )
        max_pb5 = premium_brands["MRP Current"].max() if not premium_brands.empty else 100
        fig5.update_yaxes(range=[0, max_pb5 * 1.2])
        fig5.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig5, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Highest unit list price brands commanding premium market positioning.")

    with row3_col2:
        # 🏷️ Chart 6: Top 10 Heavily Discounted Brands
        discount_brands = (
            filtered_df[filtered_df["Brand name"].isin(valid_brands)]
            .groupby("Brand name")["Discount %"]
            .mean()
            .reset_index()
            .sort_values("Discount %", ascending=False)
            .head(10)
        )

        fig6 = px.bar(
            discount_brands,
            x="Brand name",
            y="Discount %",
            title="6. 🏷️ Top 10 Brands by Average Discount %",
            color="Discount %",
            color_continuous_scale="Blues",
            text=discount_brands["Discount %"].round(2),
        )
        fig6.update_layout(
            height=400, showlegend=False, xaxis_tickangle=-45
        )
        max_c6 = change_price["MRP Current"].max() if not change_price.empty else 100
        fig6.update_xaxes(range=[0, max_c6 * 1.25])
        max_db6 = discount_brands["Discount %"].max() if not discount_brands.empty else 10
        fig6.update_yaxes(range=[0, max_db6 * 1.2])
        fig6.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig6, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Brands with highest promotional discounting levels to drive consumer push.")

    # -----------------------------------------------------------------------------
    # ROW 4: Sub-Category Affinity & Price Band Segmentation
    # -----------------------------------------------------------------------------
    row4_col1, row4_col2 = st.columns(2)

    with row4_col1:
        # 🔗 Chart 7: Brand × Sub-Category Affinity Heatmap
        top_12_brands = (
            filtered_df["Brand name"].value_counts().head(12).index.tolist()
        )
        top_6_subcats = (
            filtered_df["Sub Category"].value_counts().head(6).index.tolist()
        )

        matrix_df = filtered_df[
            (filtered_df["Brand name"].isin(top_12_brands))
            & (filtered_df["Sub Category"].isin(top_6_subcats))
        ]
        brand_subcat = pd.crosstab(
            matrix_df["Brand name"], matrix_df["Sub Category"]
        )

        fig7 = px.imshow(
            brand_subcat,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="GnBu",
            title="7. 🔗 Brand × Sub-Category Concentration",
        )
        fig7.update_layout(height=450)
        st.plotly_chart(fig7, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Cross-tabulation showing subcategory focus and product specialization across top brands.")

    with row4_col2:
        # 🎚️ Chart 8: Price Band Segmentation across Top 10 Brands
        top_10_brands = (
            filtered_df["Brand name"].value_counts().head(10).index.tolist()
        )
        brand_pb = (
            filtered_df[filtered_df["Brand name"].isin(top_10_brands)]
            .groupby(["Brand name", "Price Band"], observed=False)
            .size()
            .reset_index(name="Count")
        )

        fig8 = px.bar(
            brand_pb,
            x="Brand name",
            y="Count",
            color="Price Band",
            title="8. 🎚️ Price Band Breakdown for Top 10 Brands",
            color_discrete_sequence=px.colors.qualitative.Safe,
            barmode="stack",
        )
        fig8.update_layout(
            height=450,
            xaxis_tickangle=-45,
            legend=dict(orientation="h", y=-0.3, x=0),
        )
        max_bp8 = brand_pb.groupby("Brand name")["Count"].sum().max() if not brand_pb.empty else 10
        fig8.update_yaxes(range=[0, max_bp8 * 1.2])
        st.plotly_chart(fig8, use_container_width=True)
        with st.expander("💡 Insights"):
            st.caption("Price tier composition for major brands showing budget vs premium product mix.")

# ===================== TAB 5: SKU ANALYSIS =====================
with tab5:
    st.markdown("### 📦 SKU & Packaging Analysis")

    # 0. Pre-compute Unit Pricing Metric (Price per 100g) for FMCG efficiency analysis
    if (
        "SKU size current -(previous)" in filtered_df.columns
        and "MRP Current" in filtered_df.columns
    ):
        filtered_df["Price_per_100g"] = (
            filtered_df["MRP Current"]
            / filtered_df["SKU size current -(previous)"]
        ) * 100

    # -----------------------------------------------------------------------------
    # ROW 1: Packaging Tiers & Grammage Segmentation (Bar & Pie)
    # -----------------------------------------------------------------------------
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # 📊 Chart 1: Product Count by SKU Size Group (Bar Chart)
        if "SKU Size Group" in filtered_df.columns:
            size_group_counts = (
                filtered_df["SKU Size Group"]
                .value_counts()
                .reset_index(name="Count")
                .rename(columns={"index": "SKU Size Group"})
            )

            fig1 = px.bar(
                size_group_counts,
                x="SKU Size Group",
                y="Count",
                title="1. 📦 Product Distribution by Packaging Tier",
                color="Count",
                color_continuous_scale="Viridis",
                text="Count",
            )
            fig1.update_layout(
                height=400, showlegend=False, coloraxis_showscale=False
            )
            max_sg1 = size_group_counts["Count"].max() if not size_group_counts.empty else 10
            fig1.update_yaxes(range=[0, max_sg1 * 1.2])
            fig1.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(fig1, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Volume breakdown across small, medium, and bulk packaging tiers.")

    with row1_col2:
        # 🥧 Chart 2: Top Grammage Segments / SKU Ranges (Donut Chart)
        if "SKU Range" in filtered_df.columns:
            sku_range_counts = (
                filtered_df["SKU Range"]
                .value_counts()
                .head(10)
                .reset_index(name="Count")
                .rename(columns={"index": "SKU Range"})
            )

            fig2 = px.pie(
                sku_range_counts,
                values="Count",
                names="SKU Range",
                title="2. 🥧 Market Share of Top Grammage Brackets (g/ml)",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3,
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Market share distribution of top consumer grammage brackets.")

    # -----------------------------------------------------------------------------
    # ROW 2: Pricing across Pack Sizes & Unit Economics (Grouped Bar & Bar)
    # -----------------------------------------------------------------------------
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        # 📊 Chart 3: Average MRP vs. Retail Price by SKU Size Group (Grouped Bar Chart)
        if "SKU Size Group" in filtered_df.columns:
            size_pricing = (
                filtered_df.groupby("SKU Size Group", observed=False)[
                    ["MRP Current", "Retailer Price"]
                ]
                .mean()
                .reset_index()
                .dropna()
            )

            fig3 = go.Figure()
            fig3.add_trace(
                go.Bar(
                    x=size_pricing["SKU Size Group"],
                    y=size_pricing["MRP Current"].round(1),
                    name="Avg MRP (₹)",
                    marker_color="#6366f1",
                    text=size_pricing["MRP Current"].round(1),
                    textposition="outside",
                )
            )
            fig3.add_trace(
                go.Bar(
                    x=size_pricing["SKU Size Group"],
                    y=size_pricing["Retailer Price"].round(1),
                    name="Avg Retail Price (₹)",
                    marker_color="#10b981",
                    text=size_pricing["Retailer Price"].round(1),
                    textposition="outside",
                )
            )
            fig3.update_layout(
                title="3. 💵 Average Price Points across Size Groups",
                barmode="group",
                height=420,
                legend=dict(orientation="h", y=1.1, x=0),
            )
            max_sp3 = size_pricing[["MRP Current", "Retailer Price"]].max().max() if not size_pricing.empty else 100
            fig3.update_yaxes(range=[0, max_sp3 * 1.2])
            st.plotly_chart(fig3, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Price scaling and retail realization across packaging size categories.")

    with row2_col2:
        # 📊 Chart 4: Unit Economics - Median Price per 100g by Sub-Category (Bar Chart)
        if "Price_per_100g" in filtered_df.columns:
            unit_price_subcat = (
                filtered_df.groupby("Sub Category")["Price_per_100g"]
                .median()
                .reset_index()
                .sort_values("Price_per_100g", ascending=False)
                .head(10)
            )

            fig4 = px.bar(
                unit_price_subcat,
                x="Sub Category",
                y="Price_per_100g",
                title="4. ⚖️ Unit Economics: Median Price per 100g (₹)",
                color="Price_per_100g",
                color_continuous_scale="Teal",
                text=unit_price_subcat["Price_per_100g"].round(1),
            )
            fig4.update_layout(
                height=420,
                showlegend=False,
                xaxis_tickangle=-35,
                coloraxis_showscale=False,
            )
            max_m4 = margin_subcat["Retail Margin"].max() if not margin_subcat.empty else 10
            fig4.update_yaxes(range=[0, max_m4 * 1.2])
            max_up4 = unit_price_subcat["Price_per_100g"].max() if not unit_price_subcat.empty else 100
            fig4.update_yaxes(range=[0, max_up4 * 1.2])
            fig4.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(fig4, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Standardized unit cost efficiency (price per 100g) across subcategories.")

    # -----------------------------------------------------------------------------
    # ROW 3: Promotional Strategy & Pack Size Spread (Bar & Box Plot)
    # -----------------------------------------------------------------------------
    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        # 📊 Chart 5: Average Discount % by SKU Size Group (Bar Chart)
        if "SKU Size Group" in filtered_df.columns:
            size_discount = (
                filtered_df.groupby("SKU Size Group", observed=False)["Discount %"]
                .mean()
                .reset_index()
                .dropna()
                .sort_values("Discount %", ascending=False)
            )

            fig5 = px.bar(
                size_discount,
                x="SKU Size Group",
                y="Discount %",
                title="5. 🏷️ Promotional Intensity: Avg Discount % by Pack Size",
                color="Discount %",
                color_continuous_scale="Blues",
                text=size_discount["Discount %"].round(2),
            )
            fig5.update_layout(
                height=420, showlegend=False, coloraxis_showscale=False
            )
            max_sd5 = size_discount["Discount %"].max() if not size_discount.empty else 10
            fig5.update_yaxes(range=[0, max_sd5 * 1.2])
            fig5.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(fig5, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Promotional discount depth targeted at specific pack size tiers.")

    with row3_col2:
        # 📦 Chart 6: Pack Weight Distribution (g/ml) across Top 10 Brands (Box Plot)
        if "SKU size current -(previous)" in filtered_df.columns:
            top_10_brands_sku = (
                filtered_df["Brand name"].value_counts().head(10).index.tolist()
            )
            box_data = filtered_df[
                filtered_df["Brand name"].isin(top_10_brands_sku)
            ].dropna(subset=["SKU size current -(previous)"])

            if not box_data.empty:
                fig6 = px.box(
                    box_data,
                    x="Brand name",
                    y="SKU size current -(previous)",
                    color="Brand name",
                    title="6. 📊 Grammage Spread across Top 10 Brands (g/ml)",
                    color_discrete_sequence=px.colors.qualitative.Bold,
                )
                fig6.update_layout(
                    height=420,
                    showlegend=False,
                    xaxis_tickangle=-35,
                    yaxis=dict(range=[0, 1000]),  # Focused view excluding industrial sacks
                )
                st.plotly_chart(fig6, use_container_width=True)
                with st.expander("💡 Insights"):
                    st.caption("Statistical distribution and spread of pack weights offered by leading brands.")

    # -----------------------------------------------------------------------------
    # ROW 4: Brand Packaging Diversity & Sub-Category Formats (Bar & Heatmap)
    # -----------------------------------------------------------------------------
    row4_col1, row4_col2 = st.columns(2)

    with row4_col1:
        # 📊 Chart 7: Top 10 Brands by SKU Versatility (Number of Unique Pack Sizes)
        if "SKU Range" in filtered_df.columns:
            brand_sku_diversity = (
                filtered_df.groupby("Brand name")["SKU Range"]
                .nunique()
                .reset_index()
                .sort_values("SKU Range", ascending=False)
                .head(10)
            )

            fig7 = px.bar(
                brand_sku_diversity,
                x="Brand name",
                y="SKU Range",
                title="7. 🎯 SKU Diversity: Distinct Pack Formats per Brand",
                color="SKU Range",
                color_continuous_scale="Purples",
                text="SKU Range",
            )
            fig7.update_layout(
                height=450,
                showlegend=False,
                xaxis_tickangle=-35,
                coloraxis_showscale=False,
            )
            max_bsd7 = brand_sku_diversity["SKU Range"].max() if not brand_sku_diversity.empty else 10
            fig7.update_yaxes(range=[0, max_bsd7 * 1.2])
            fig7.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(fig7, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Packaging versatility ranking brands by number of active pack format variants.")

    with row4_col2:
        # 🔥 Chart 8: Sub-Category × SKU Size Group Packaging Matrix (Heatmap)
        if "SKU Size Group" in filtered_df.columns:
            top_6_subcats = (
                filtered_df["Sub Category"].value_counts().head(6).index.tolist()
            )
            subcat_sku_matrix = filtered_df[
                filtered_df["Sub Category"].isin(top_6_subcats)
            ]
            crosstab_sku = pd.crosstab(
                subcat_sku_matrix["Sub Category"], subcat_sku_matrix["SKU Size Group"]
            )

            fig8 = px.imshow(
                crosstab_sku,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="YlOrRd",
                title="8. 🔥 Packaging Density: Sub-Category × Size Group",
            )
            fig8.update_layout(height=450)
            st.plotly_chart(fig8, use_container_width=True)
            with st.expander("💡 Insights"):
                st.caption("Packaging format concentration heatmap across primary subcategories.")

# ===================== TAB 6: DATA EXPLORER =====================
with tab6:
    st.markdown("### 📋 Data Explorer")

    # Search
    search_term = st.text_input("🔍 Search by Brand, Product or Variant", "")

    if search_term:
        search_df = filtered_df[
            filtered_df['Brand name'].str.contains(search_term, case=False, na=False) |
            filtered_df['Variant/Flavour'].str.contains(search_term, case=False, na=False) |
            filtered_df['Company name'].str.contains(search_term, case=False, na=False)
        ]
        st.success(f"Found {len(search_df)} matching records")
    else:
        search_df = filtered_df

    # Column selector
    display_cols = st.multiselect(
        "Select columns to display",
        search_df.columns.tolist(),
        default=['Category', 'City', 'Brand name', 'Variant/Flavour', 
                 'Type of Change', 'MRP Current', 'Retailer Price', 
                 'Discount %', 'Date of Discovery']
    )

    # Show data
    st.dataframe(
        search_df[display_cols].sort_values('Date of Discovery', ascending=False),
        use_container_width=True,
        height=500
    )

    # Download
    csv = search_df[display_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Filtered Data as CSV",
        csv,
        "fmcg_filtered_data.csv",
        "text/csv"
    )

    # Summary stats
    with st.expander("📊 Statistical Summary"):
        st.write(search_df[['MRP Current', 'Retailer Price', 'Discount %', 'Retail Margin']].describe())

# ===================== FOOTER =====================
st.markdown("---")
st.caption("""
<div style='text-align: center; color: #9ca3af;'>
    📊 FMCG Market Intelligence Dashboard | Built with Streamlit & Plotly | Data sourced from market research
</div>
""", unsafe_allow_html=True)