import warnings

import pandas as pd
import plotly.express as px
import streamlit as st

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Asterix Intelligence - Insights",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Consistent meaning across every chart: red = costs shoppers more / shrinks, green = better for shoppers.
RED, GREEN, GREY, BLUE = "#ef4444", "#22c55e", "#94a3b8", "#6366f1"
DIRECTION_COLORS = {"Increase": RED, "Decrease": GREEN, "Unchanged": GREY}
HEALTH_CLAIMS = {
    "HC_High_Protein": "High Protein",
    "HC_Sugar_Free": "Sugar Free",
    "HC_Multigrain": "Multigrain",
    "HC_Fibre": "Fibre",
    "HC_Whole_Grain": "Whole Grain",
    "HC_Low_Fat": "Low Fat",
    "HC_Gluten_Free": "Gluten Free",
    "HC_No_Maida": "No Maida",
    "HC_Baked_Not_Fried": "Baked, Not Fried",
    "HC_Cholesterol": "Cholesterol",
}

st.markdown(
    """
<style>
    .main-header {
        font-size: 2.6rem; font-weight: 800; text-align: center; margin-bottom: 0.2rem;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .sub-header { text-align: center; color: #94a3b8; margin-bottom: 1.5rem; }
    .takeaway {
        border-left: 4px solid #6366f1; padding: 0.4rem 0.9rem; margin: 0.2rem 0 0.8rem 0;
        background: rgba(99, 102, 241, 0.08); border-radius: 4px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ===================== DATA LOADING =====================
@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv("a127_final_v35.csv", low_memory=False)
    df["Date"] = pd.to_datetime(df["Date_ISO"], format="%Y-%m-%d", errors="coerce")
    df["Brand_First_Seen"] = pd.to_datetime(df["Brand_First_Seen"], errors="coerce")
    for col in ["Offer_Effective_Discount_Pct", "Price_per_100g_ml", "Health_Claim_Count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def takeaway(text):
    st.markdown(f"<div class='takeaway'>💡 {text}</div>", unsafe_allow_html=True)


def pct(part, whole):
    return 100 * part / whole if whole else 0.0


def style(fig, height=380):
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=40, b=10), legend_title_text="", title_x=0.0
    )
    return fig


df = load_data()

# ===================== SIDEBAR FILTERS =====================
with st.sidebar:
    st.title("🔍 Filters")
    categories = sorted(df["Category"].dropna().unique())
    category = st.selectbox("📦 Category", ["All Categories"] + categories)
    cities = sorted(df["City"].dropna().unique())
    selected_cities = st.multiselect("🏙️ City", cities, default=cities)
    min_date, max_date = df["Date"].min().date(), df["Date"].max().date()
    date_range = st.date_input(
        "📅 Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )

data = df[df["City"].isin(selected_cities)]
if category != "All Categories":
    data = data[data["Category"] == category]
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    data = data[
        (data["Date"] >= pd.Timestamp(date_range[0])) & (data["Date"] <= pd.Timestamp(date_range[1]))
    ]

st.markdown("<div class='main-header'>💡 Key Insights</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='sub-header'>{category} · {len(data):,} SKU observations</div>",
    unsafe_allow_html=True,
)

if data.empty:
    st.warning("No data for the selected filters.")
    st.stop()

# ===================== HEADLINE KPIs =====================
priced = data[data["Price_Direction_Combined"].notna()]
flagged = data[data["Shrinkflation_Flag"].notna()]
k1, k2, k3, k4 = st.columns(4)
k1.metric("SKU observations", f"{len(data):,}")
k2.metric("With an offer", f"{pct((data['Has_Offer'] == 'Yes').sum(), len(data)):.0f}%")
k3.metric(
    "Prices that rose",
    f"{pct((priced['Price_Direction_Combined'] == 'Increase').sum(), len(priced)):.0f}%",
    help="Share of SKUs with a price comparison available",
)
k4.metric(
    "Flagged as shrinkflation",
    f"{pct((flagged['Shrinkflation_Flag'] == 'Yes').sum(), len(flagged)):.0f}%",
    help="Share of SKUs with a size or price change record",
)

tab_price, tab_promo, tab_health, tab_market = st.tabs(
    ["💰 Pricing", "🏷️ Promotions", "🥗 Health", "🚀 Innovation & Market"]
)

# ===================== PRICING =====================
with tab_price:
    # 1. Shrinkflation tracker
    st.subheader("1. Shrinkflation tracker")
    if flagged.empty:
        st.info("No size or price change records for the selected filters.")
    else:
        yes = (flagged["Shrinkflation_Flag"] == "Yes").sum()
        takeaway(
            f"<b>{pct(yes, len(flagged)):.0f}%</b> of SKUs with a size or price change "
            f"({yes:,} of {len(flagged):,}) were flagged as shrinkflation: "
            "less product for the same or a higher price."
        )
        c1, c2 = st.columns([1, 1.4])
        with c1:
            counts = flagged["Shrinkflation_Flag"].value_counts().reset_index()
            counts.columns = ["Shrinkflation", "SKUs"]
            fig = px.pie(
                counts,
                names="Shrinkflation",
                values="SKUs",
                hole=0.55,
                color="Shrinkflation",
                color_discrete_map={"Yes": RED, "No": GREEN},
                title="Share of changed SKUs flagged",
            )
            st.plotly_chart(style(fig), use_container_width=True)
        with c2:
            by_brand = (
                flagged.groupby("Brand name")["Shrinkflation_Flag"]
                .agg(Flagged=lambda s: (s == "Yes").sum(), Total="count")
                .reset_index()
            )
            by_brand = by_brand[by_brand["Total"] >= 5]
            by_brand["Share %"] = 100 * by_brand["Flagged"] / by_brand["Total"]
            top = by_brand.sort_values(["Share %", "Total"], ascending=False).head(10)
            fig = px.bar(
                top.sort_values("Share %"),
                x="Share %",
                y="Brand name",
                orientation="h",
                text=top.sort_values("Share %")["Share %"].map(lambda v: f"{v:.0f}%"),
                hover_data=["Flagged", "Total"],
                title="Top 10 brands by shrinkflation share (min. 5 changes)",
            )
            fig.update_traces(marker_color=RED)
            st.plotly_chart(style(fig), use_container_width=True)
        st.caption(
            "Most flags assume the price stayed the same when no new price was stated on the pack."
        )

    # 2. Price moves
    st.subheader("2. Price moves")
    if priced.empty:
        st.info("No price comparisons available for the selected filters.")
    else:
        dir_counts = priced["Price_Direction_Combined"].value_counts()
        up, down, same = (dir_counts.get(k, 0) for k in ["Increase", "Decrease", "Unchanged"])
        takeaway(
            f"Of {len(priced):,} SKUs with a price comparison, <b>{up:,}</b> went up, "
            f"<b>{down:,}</b> went down and <b>{same:,}</b> stayed the same."
        )
        m1, m2, m3 = st.columns(3)
        m1.metric("🔺 Increase", f"{up:,}", f"{pct(up, len(priced)):.0f}%", delta_color="inverse")
        m2.metric("🔻 Decrease", f"{down:,}", f"{pct(down, len(priced)):.0f}%", delta_color="normal")
        m3.metric("➖ Unchanged", f"{same:,}", f"{pct(same, len(priced)):.0f}%", delta_color="off")
        monthly = (
            priced.groupby(["Year_Month", "Price_Direction_Combined"]).size().reset_index(name="SKUs")
        )
        fig = px.bar(
            monthly,
            x="Year_Month",
            y="SKUs",
            color="Price_Direction_Combined",
            color_discrete_map=DIRECTION_COLORS,
            category_orders={"Price_Direction_Combined": ["Increase", "Unchanged", "Decrease"]},
            title="Price direction by month",
        )
        fig.update_xaxes(title="")
        st.plotly_chart(style(fig), use_container_width=True)
        st.caption("Only SKUs where a previous price is available are counted.")

    # 8. Regional comparison
    st.subheader("8. Regional price comparison")
    regional = data[data["Price_per_100g_ml"].notna()]
    if regional.empty:
        st.info("No unit price data for the selected filters.")
    else:
        # Medians, clipped to the 1st-99th percentile, because unit prices have extreme outliers
        lo, hi = regional["Price_per_100g_ml"].quantile([0.01, 0.99])
        regional = regional[regional["Price_per_100g_ml"].between(lo, hi)]
        by_region = (
            regional.groupby("City_Region")["Price_per_100g_ml"].median().reset_index().sort_values(
                "Price_per_100g_ml", ascending=False
            )
        )
        takeaway(
            f"<b>{by_region.iloc[0]['City_Region']}</b> has the highest median price "
            f"(₹{by_region.iloc[0]['Price_per_100g_ml']:.1f} per 100g/ml) and "
            f"<b>{by_region.iloc[-1]['City_Region']}</b> the lowest "
            f"(₹{by_region.iloc[-1]['Price_per_100g_ml']:.1f})."
        )
        fig = px.bar(
            by_region,
            x="City_Region",
            y="Price_per_100g_ml",
            text=by_region["Price_per_100g_ml"].map(lambda v: f"₹{v:.1f}"),
            title="Median price per 100g/ml by region",
            labels={"City_Region": "", "Price_per_100g_ml": "₹ per 100g/ml"},
        )
        fig.update_traces(marker_color=BLUE)
        st.plotly_chart(style(fig, 340), use_container_width=True)
        st.caption("Median of values between the 1st and 99th percentile. Compare within one category for a fair view.")

# ===================== PROMOTIONS =====================
with tab_promo:
    offers = data[data["Has_Offer"] == "Yes"]

    # 3. Offer mix
    st.subheader("3. Offer mix")
    if offers.empty:
        st.info("No offers for the selected filters.")
    else:
        mix = offers["Offer_Type"].value_counts().reset_index()
        mix.columns = ["Offer type", "SKUs"]
        mix["Share"] = 100 * mix["SKUs"] / mix["SKUs"].sum()
        takeaway(
            f"<b>{pct(len(offers), len(data)):.0f}%</b> of SKUs carry an offer. "
            f"The most common is <b>{mix.iloc[0]['Offer type']}</b> "
            f"({mix.iloc[0]['Share']:.0f}% of offers)."
        )
        mix = mix.sort_values("SKUs")
        fig = px.bar(
            mix,
            x="SKUs",
            y="Offer type",
            orientation="h",
            text=mix["Share"].map(lambda v: f"{v:.0f}%"),
            title="Offers by type",
        )
        fig.update_traces(marker_color=BLUE)
        st.plotly_chart(style(fig, 340), use_container_width=True)

    # 4. Promo intensity
    st.subheader("4. Promo intensity")
    discounted = data[data["Offer_Effective_Discount_Pct"].notna()]
    if discounted.empty:
        st.info("No offers with a measurable discount for the selected filters.")
    else:
        view = st.radio("Compare by", ["City", "Brand"], horizontal=True)
        group_col, min_n = ("City", 1) if view == "City" else ("Brand name", 30)
        intensity = (
            discounted.groupby(group_col)["Offer_Effective_Discount_Pct"]
            .agg(["mean", "count"])
            .reset_index()
        )
        intensity = intensity[intensity["count"] >= min_n].sort_values("mean", ascending=False)
        if view == "Brand":
            intensity = intensity.head(15)
        if intensity.empty:
            st.info("Not enough offers to compare.")
        else:
            intensity = intensity.sort_values("mean")
            takeaway(
                f"<b>{intensity.iloc[-1][group_col]}</b> discounts hardest, at an average of "
                f"<b>{intensity.iloc[-1]['mean']:.0f}%</b> off."
                + (" Brands need at least 30 offers to be shown." if view == "Brand" else "")
            )
            fig = px.bar(
                intensity,
                x="mean",
                y=group_col,
                orientation="h",
                text=intensity["mean"].map(lambda v: f"{v:.0f}%"),
                hover_data={"count": True},
                title=f"Average offer discount by {view.lower()}",
                labels={"mean": "Avg discount %", group_col: "", "count": "Offers"},
            )
            fig.update_traces(marker_color=GREEN)
            st.plotly_chart(style(fig, 420), use_container_width=True)

# ===================== HEALTH =====================
with tab_health:
    st.subheader("5. Health claims")
    claim_cols = [c for c in HEALTH_CLAIMS if c in data.columns]
    claim_share = pd.DataFrame(
        {
            "Claim": [HEALTH_CLAIMS[c] for c in claim_cols],
            "Share %": [100 * pd.to_numeric(data[c], errors="coerce").fillna(0).mean() for c in claim_cols],
        }
    ).sort_values("Share %")
    with_claim = pct((data["Health_Claim_Count"] > 0).sum(), len(data))
    top_claim = claim_share.iloc[-1]
    takeaway(
        f"<b>{with_claim:.0f}%</b> of SKUs make at least one health claim. "
        f"The most common is <b>{top_claim['Claim']}</b> ({top_claim['Share %']:.1f}% of SKUs)."
    )
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            claim_share,
            x="Share %",
            y="Claim",
            orientation="h",
            text=claim_share["Share %"].map(lambda v: f"{v:.1f}%"),
            title="Share of SKUs making each claim",
        )
        fig.update_traces(marker_color=GREEN)
        st.plotly_chart(style(fig, 420), use_container_width=True)
    with c2:
        trend = data.groupby("Year_Month")["Health_Claim_Count"].mean().reset_index()
        fig = px.line(
            trend,
            x="Year_Month",
            y="Health_Claim_Count",
            markers=True,
            title="Average health claims per SKU, by month",
            labels={"Year_Month": "", "Health_Claim_Count": "Claims per SKU"},
        )
        fig.update_traces(line_color=BLUE)
        st.plotly_chart(style(fig, 420), use_container_width=True)

# ===================== INNOVATION & MARKET =====================
with tab_market:
    # 6. New entrants
    st.subheader("6. New brand entrants")
    brands = (
        data.dropna(subset=["Brand_First_Seen"])
        .drop_duplicates("Brand name")[["Brand name", "Company name", "Brand_First_Seen"]]
        .copy()
    )
    # The first month of the dataset holds every brand already on shelf, not true launches
    baseline_end = df["Brand_First_Seen"].min() + pd.DateOffset(months=1)
    launches = brands[brands["Brand_First_Seen"] >= baseline_end].copy()
    if launches.empty:
        st.info("No new brands for the selected filters.")
    else:
        launches["Month"] = launches["Brand_First_Seen"].dt.to_period("M").astype(str)
        per_month = launches.groupby("Month").size().reset_index(name="New brands")
        takeaway(
            f"<b>{len(launches):,}</b> new brands appeared after the first month of tracking, "
            f"averaging <b>{per_month['New brands'].mean():.0f}</b> per month."
        )
        c1, c2 = st.columns([1.4, 1])
        with c1:
            fig = px.line(
                per_month,
                x="Month",
                y="New brands",
                markers=True,
                title="New brands first seen per month",
            )
            fig.update_traces(line_color=BLUE)
            fig.update_xaxes(title="")
            st.plotly_chart(style(fig), use_container_width=True)
        with c2:
            st.markdown("**Newest brands**")
            newest = launches.sort_values("Brand_First_Seen", ascending=False).head(10)
            newest["First seen"] = newest["Brand_First_Seen"].dt.strftime("%d %b %Y")
            st.dataframe(
                newest[["Brand name", "Company name", "First seen"]],
                hide_index=True,
                use_container_width=True,
                height=380,
            )

    # 7. Flavour families
    st.subheader("7. Flavour family share")
    flavours = data[~data["Flavour_Family"].isin(["Other", "No Variant"])]["Flavour_Family"]
    if flavours.empty:
        st.info("No flavour data for the selected filters.")
    else:
        fam = flavours.value_counts().reset_index()
        fam.columns = ["Flavour family", "SKUs"]
        # Keep the donut readable: top 6 families, the rest grouped
        if len(fam) > 6:
            rest = fam.iloc[6:]["SKUs"].sum()
            fam = pd.concat(
                [fam.iloc[:6], pd.DataFrame({"Flavour family": ["Others"], "SKUs": [rest]})]
            )
        takeaway(
            f"<b>{fam.iloc[0]['Flavour family']}</b> leads with "
            f"{pct(fam.iloc[0]['SKUs'], fam['SKUs'].sum()):.0f}% of flavoured SKUs."
        )
        fig = px.pie(fam, names="Flavour family", values="SKUs", hole=0.5, title="Share of SKUs by flavour family")
        st.plotly_chart(style(fig, 400), use_container_width=True)
        st.caption("'Other' and 'No Variant' are excluded.")

    # 9. Market concentration
    st.subheader("9. Market concentration")
    hhi = data.groupby("Category")["Category_HHI"].first().reset_index()

    def hhi_label(v):
        if v < 1500:
            return "🟢 Competitive"
        if v <= 2500:
            return "🟡 Moderately concentrated"
        return "🔴 Concentrated"

    hhi["Status"] = hhi["Category_HHI"].map(hhi_label)
    if category == "All Categories":
        st.dataframe(
            hhi.rename(columns={"Category_HHI": "HHI"}).sort_values("HHI", ascending=False),
            hide_index=True,
            use_container_width=True,
        )
        st.caption("HHI = sum of squared market shares (0-10,000). Below 1,500 means many competing players.")
        st.info("Select a single category in the sidebar to see its top 5 companies.")
    else:
        value = hhi.iloc[0]["Category_HHI"]
        shares = (
            data.groupby("Company name")["Company_Share_in_Category_Pct"].first().nlargest(5).reset_index()
        )
        takeaway(
            f"{category} is <b>{hhi_label(value)[2:].lower()}</b> (HHI {value:,.0f}). "
            f"The top 5 companies hold <b>{shares['Company_Share_in_Category_Pct'].sum():.0f}%</b> "
            "of the category."
        )
        c1, c2 = st.columns([1, 1.6])
        with c1:
            st.metric("Market concentration (HHI)", f"{value:,.0f}", hhi_label(value), delta_color="off")
            st.caption("HHI = sum of squared market shares (0-10,000). Below 1,500 means many competing players.")
        with c2:
            shares = shares.sort_values("Company_Share_in_Category_Pct")
            fig = px.bar(
                shares,
                x="Company_Share_in_Category_Pct",
                y="Company name",
                orientation="h",
                text=shares["Company_Share_in_Category_Pct"].map(lambda v: f"{v:.1f}%"),
                title="Top 5 companies by category share",
                labels={"Company_Share_in_Category_Pct": "Share %", "Company name": ""},
            )
            fig.update_traces(marker_color=BLUE)
            st.plotly_chart(style(fig, 340), use_container_width=True)
