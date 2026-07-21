import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_csv("a120c.csv", low_memory=False)

st.title("📊 Overview")


data = {
    "Biscuits": [
        "Britannia", "ITC", "Unibic", "Mrs Bector", "Mondelez",
        "Anmol", "Sona Biscuits", "United Biscuits", "Ravi Foods",
        "Saj Food Products", "Patanjali"
    ],
    "Confectionery": [
        "Hersheys", "ITC", "Mondelez", "Mars", "Nestle",
        "Perfetti Van Melle", "Prayagh", "Wringleys", "Ferrero",
        "Lotte", "Patanjali", "AMUL"
    ],
    "Salty Snacks": [
        "Pepsico", "Haldiraam", "Guiltfree", "Pratap", "ITC",
        "Bikanerwala", "Bikaji", "Haldiram Bhujiawala", "DFM",
        "Haldiram International", "Chheda"
    ],
    "Bakery": [
        "Bauli", "Britannia", "Elite", "Dream Bake", "ITC",
        "Lotte", "Modern", "Saj", "Prayagh", "Sona"
    ],
    "Breakfast": [
        "Nestle", "Kelloggs", "Bagrrys", "Agrotech", "Ameya",
        "Pepsico", "Sproutlife", "Tata Consumer", "Paragiya",
        "Marico"
    ],
    "Packaged Atta": [
        "ITC", "AWL", "Patanjali", "Reliance Retail", "General Mills",
        "Ganesh Grains", "Sanghvi", "Nutrapoorna", "Elite Foods",
        "Cargil"
    ]
}

df_table = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))


data_mumbai = {
    "Biscuits": [
        "Britannia Industries Limited",
        "ITC Foods Limited",
        "Unibic Food India Private Limited",
        "Mondelez India Foods Private Limited",
        "Surya Food & Agro Limited",
        "Pickwick Hygienic Products Pvt Ltd",
        "Mrs. Bectors Food Specialties Limited",
        "United Biscuit Pvt Ltd",
        "Sona Biscuits Ltd",
        "Patanjali Foods Limited"
    ],
    
    "Confectionery": [
        "Perfetti Van Melle India Pvt Ltd",
        "Nestle India Limited",
        "Mondelez India Foods Private Limited",
        "Wrigley's India Pvt Ltd",
        "Prayagh Nutri Prodcts Pvt Ltd",
        "SUNCREST FOOD MAKERS",
        "Ferrero India Pvt Ltd",
        "ITC Foods Limited",
        "Dabur India Limited",
        "Malas Food Products Pvt Ltd"
    ],
    
    "Salty Snacks": [
        "Haldiram Food International Pvt Ltd",
        "Pepsico India Holding Pvt Ltd",
        "Balaji Wafers Private Limited",
        "Chheda Specialities Foods Pvt Ltd",
        "Heemankash Bakers Pvt Ltd",
        "Gopal Snacks Private Limited",
        "Pratap Snacks Pvt Ltd",
        "Bikanervala Foods Private Limited",
        "Hari Om Enterprises",
        "Bikaji Food International Ltd"
    ],
    
    "Bakery": [
        "Britannia Industries Limited",
        "Kwality Confectioners & Bakers India Pvt Ltd",
        "Elite Foods Pvt Ltd",
        "Delicia Foods",
        "Dream Bake India Pvt Ltd",
        "Om Hariom Bakery",
        "Denish Food Products",
        "Prayagh Nutri Prodcts Pvt Ltd",
        "Concert Food Products",
        "Nazneen Bakery"
    ],
    
    "Breakfast": [
        "Kellogg's India Pvt Ltd",
        "Ameya Food",
        "Bagrry’s India Private Limited",
        "Tata Consumer Products Ltd",
        "Sproutlife Foods Pvt Ltd",
        "Rebala Nutri Foodee Pvt Ltd",
        "Agro Tech Foods Limited",
        "VLS Foods Pvt Ltd",
        "HW Wellness Solutions Pvt Ltd",
        "Pepsico India Holding Pvt Ltd"
    ],
    
    "Packaged Atta": [
        "ITC Foods Limited",
        "ITC Foods Limited",
        "ITC Foods Limited",
        "ITC Foods Limited",
        "ITC Foods Limited",
        "Adani Wilmar Limited",
        "Adani Wilmar Limited",
        "Reliance Retail Limited",
        "Reliance Retail Limited",
        "Sanghvi Foods Pvt Ltd",
        "Sanghvi Foods Pvt Ltd",
        "General Mills",
        "General Mills",
        "General Mills"
    ],
    
    "Atta-Brand": [
        "Aashirvaad Shudh Chakki",
        "Aashirvaad Superior MP",
        "Aashirvaad Multigrains",
        "Aashirvaad Sugar Control",
        "Aashirvaad MP Chakki Atta",
        "Fortune Chakki Fresh",
        "Fortune Sharbati",
        "Independence",
        "Good Life",
        "Silver Coin MP Sharbati Atta",
        "Silver Coin Whole Wheat",
        "Pillsbury Chakki Fresh",
        "Pillsbury Multigrain",
        "Pillsbury Multigrain"
    ]
}

# Handle uneven lengths
df_mumbai = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data_mumbai.items()]))

delhi_data = {
    "Biscuits": [
        "Britannia Industries Limited","ITC Foods Limited","Mrs. Bectors Food Specialties Limited",
        "Mondelez India Foods Private Limited","Anmol Industries Limited","Unibic Food India Private Limited",
        "United Biscuit Pvt Ltd","Patanjali Foods Limited","Surya Food & Agro Limited","S S Food Industries"
    ],
    "Confectionery": [
        "Perfetti Van Melle India Pvt Ltd","Mondelez India Foods Private Limited","Nestle India Limited",
        "Mars International India Pvt Ltd","ITC Foods Limited","Prayagh Nutri Products Pvt Ltd",
        "Hershey India Pvt Ltd","Wrigley's India Pvt Ltd","Ferrero India Pvt Ltd",
        "Gujarat Co-operative Milk Marketing Federation Ltd"
    ],
    "Salty Snacks": [
        "Haldiram Food International Pvt Ltd","Pepsico India Holding Pvt Ltd","ITC Foods Limited",
        "Pratap Snacks Pvt Ltd","Bikanervala Foods Private Limited","Guiltfree Industries Limited",
        "Bikaji Food International Ltd","DFM Foods Limited","Priniti Foods Pvt Ltd","SSG Pharma Pvt Ltd"
    ],
    "Bakery": [
        "Britannia Industries Limited","Ready Roti India Pvt Ltd","Dream Bake India Pvt Ltd",
        "TRDP Happy World Pvt Ltd","Saj Food Products Pvt Ltd","Harish Bakers & Confectionaries Pvt Ltd",
        "ITC Foods Limited","Kidys Food Products Pvt Ltd","Lotte India Corporation Ltd","Anmol Industries Limited"
    ],
    "Breakfast": [
        "Kellogg's India Pvt Ltd","Bagrry’s India Private Limited","Marico Limited",
        "Tata Consumer Products Ltd","Nestle India Limited","Sunrise Victuals Pvt Ltd",
        "Agro Tech Foods Limited","Sproutlife Foods Pvt Ltd","Patanjali Foods Limited",
        "Cosmic Nutracos Solutions Pvt Ltd"
    ],
    "Packaged Atta": [
        "ITC Foods Limited","ITC Foods Limited","ITC Foods Limited","ITC Foods Limited","ITC Foods Limited",
        "Adani Wilmar Limited","Adani Wilmar Limited","Patanjali Foods","Patanjali Foods","Sanghvi Foods Pvt Ltd",
        "Sanghvi Foods Pvt Ltd","Reliance Retail Limited","Reliance Retail Limited"
    ],
    "Atta-Brand": [
        "Aashirvaad Shudh Chakki","Aashirvaad Superior MP","Aashirvaad Multigrains",
        "Aashirvaad Sugar Control","Aashirvaad MP Chakki Atta","Fortune Chakki Fresh",
        "Fortune Sharbati","Chakki Whole Wheat","Sharbati",
        "Silver Coin MP Sharbati Atta","Silver Coin Whole Wheat","Independence","Good Life"
    ]
}

kolkata_data = {
    "Biscuits": [
        "Britannia Industries Limited","ITC Foods Limited","Saj Food Products Pvt Ltd",
        "Sona Biscuits Ltd","Raja Udyog Pvt Ltd","Anmol Industries Limited",
        "Unibic Food India Private Limited","Mondelez India Foods Private Limited",
        "Ravi Food Pvt Ltd","Jaya Industries Pvt Ltd"
    ],
    "Confectionery": [
        "Mondelez India Foods Private Limited","Perfetti Van Melle India Pvt Ltd","Nestle India Limited",
        "Mars International India Pvt Ltd","ITC Foods Limited","Prayagh Nutri Products Pvt Ltd",
        "Ferrero India Pvt Ltd","Dharampal Satyapal Foods Limited","Hershey India Pvt Ltd","Kamco Chew Food Pvt Ltd"
    ],
    "Salty Snacks": [
        "Pepsico India Holding Pvt Ltd","Haldiram Bhujiawala Limited","Guiltfree Industries Limited",
        "ITC Foods Limited","Bikaji Food International Ltd","DFM Foods Limited",
        "Pratap Snacks Pvt Ltd","Mukharochak","Haldiram Bhujiawala Ltd","Bhikharam Chandmal"
    ],
    "Bakery": [
        "Britannia Industries Limited","Sona Biscuits Ltd","Saj Food Products Pvt Ltd",
        "Raja Udyog Pvt Ltd","Kamala Consumer Care Pvt Ltd","Samridh Overseas Trading Pvt Ltd",
        "Dream Bake India Pvt Ltd","Anmol Industries Limited","East Village Bakers LLP",
        "Prayagh Nutri Products Pvt Ltd"
    ],
    "Breakfast": [
        "Kellogg's India Pvt Ltd","Marico Limited","Tata Consumer Products Ltd",
        "Bagrry’s India Private Limited","Agro Tech Foods Limited","Nestle India Limited",
        "Pepsico India Holding Pvt Ltd","Patanjali Foods Limited","Sproutlife Foods Pvt Ltd",
        "Cosmic Nutracos Solutions Pvt Ltd"
    ],
    "Packaged Atta": [
        "ITC Foods Limited","ITC Foods Limited","ITC Foods Limited","ITC Foods Limited",
        "ITC Foods Limited","Ganesh Grains","Ganesh Grains","Ganesh Grains","Ganesh Grains",
        "Adani Wilmar Limited","Adani Wilmar Limited","Reliance Retail Limited",
        "Reliance Retail Limited","General Mills","General Mills","General Mills"
    ],
    "Atta-Brand": [
        "Aashirvaad Shudh Chakki","Aashirvaad Superior MP","Aashirvaad Multigrains",
        "Aashirvaad Sugar Control","Aashirvaad MP Chakki Atta","Premium Sharbati","Chakki Fresh",
        "Gluten Free","Multigrain","Fortune Chakki Fresh","Fortune Sharbati",
        "Independence","Good Life","Pillsbury Chakki Fresh","Pillsbury Multigrain","Pillsbury Multigrain"
    ]
}

chennai_data = {
    "Biscuits": [
        "Britannia Industries Limited","ITC Foods Limited","Unibic Food India Private Limited",
        "Ravi Food Pvt Ltd","United Biscuit Pvt Ltd","Mondelez India Foods Private Limited",
        "Karachi Bakery","Enerlife India Pvt Ltd","Aruna Food Products","Patanjali Foods Limited"
    ],
    "Confectionery": [
        "Perfetti Van Melle India Pvt Ltd","Mondelez India Foods Private Limited","Nestle India Limited",
        "Mars International India Pvt Ltd","Hershey India Pvt Ltd","Prayagh Nutri Products Pvt Ltd",
        "ITC Foods Limited","Poonam Confectionery LLP","Lotte India Corporation Ltd",
        "Naturo Food And Fruit Products"
    ],
    "Salty Snacks": [
        "Pepsico India Holding Pvt Ltd","Haldiram Food International Pvt Ltd","ITC Foods Limited",
        "Guiltfree Industries Limited","Adyar Ananda Bhavan Sweets India Pvt Ltd",
        "Bikanervala Foods Private Limited","Aadyar Anandha Bhavan Sweets India Pvt Ltd",
        "Sweet Karam Coffee India Pvt Ltd","GRB Dairy Foods Pvt Ltd",
        "Green Dot Health Foods Pvt Ltd"
    ],
    "Bakery": [
        "Britannia Industries Limited","Elite Foods Pvt Ltd","Dream Bake India Pvt Ltd",
        "Modern Food Enterprises Pvt Ltd","Elite Natural Pvt Ltd","ITC Foods Limited",
        "Bauli India Bake & Sweets Pvt Ltd","Lotte India Corporation Ltd","Karachi Bakery",
        "CK'S Foods Pvt Ltd"
    ],
    "Breakfast": [
        "Kellogg's India Pvt Ltd","Bagrry’s India Private Limited","Tata Consumer Products Ltd",
        "Marico Limited","Agro Tech Foods Limited","Pepsico India Holding Pvt Ltd",
        "Nestle India Limited","Sproutlife Foods Pvt Ltd","Pagariya Food Products Pvt Ltd",
        "Niva Nutrifoods LLP"
    ],
    "Packaged Atta": [
        "ITC Foods Limited","ITC Foods Limited","ITC Foods Limited","ITC Foods Limited",
        "ITC Foods Limited","General Mills","General Mills","General Mills",
        "Reliance Retail Limited","Reliance Retail Limited","Adani Wilmar Limited",
        "Adani Wilmar Limited","Naga Limited"
    ],
    "Atta-Brand": [
        "Aashirvaad Shudh Chakki","Aashirvaad Superior MP","Aashirvaad Multigrains",
        "Aashirvaad Sugar Control","Aashirvaad MP Chakki Atta","Pillsbury Chakki Fresh",
        "Pillsbury Multigrain","Pillsbury Multigrain","Independence","Good Life",
        "Fortune Chakki Fresh","Fortune Sharbati","Whole Wheat Atta"
    ]
}

bengaluru_data = {
    "Biscuits": [
        "Britannia Industries Limited","ITC Foods Limited","Unibic Food India Private Limited",
        "Saj Food Products Pvt Ltd","Mrs. Bectors Food Specialties Limited","United Biscuit Pvt Ltd",
        "Karachi Bakery","Mondelez India Foods Private Limited","Ravi Food Pvt Ltd","Patanjali Foods Limited"
    ],
    "Confectionery": [
        "Mondelez India Foods Private Limited","Perfetti Van Melle India Pvt Ltd","Nestle India Limited",
        "Mars International India Pvt Ltd","Prayagh Nutri Products Pvt Ltd","Hershey India Pvt Ltd",
        "ITC Foods Limited","Lotte India Corporation Ltd","Dugar Overseas Pvt Ltd",
        "RAINBOW CONFECTIONERY"
    ],
    "Salty Snacks": [
        "Pepsico India Holding Pvt Ltd","Haldiram Food International Pvt Ltd","Guiltfree Industries Limited",
        "ITC Foods Limited","Pratap Snacks Pvt Ltd","Bikaji Food International Ltd",
        "GRB Dairy Foods Pvt Ltd","Reliance Retail Limited","Isha Foods",
        "Green Dot Health Foods Pvt Ltd"
    ],
    "Bakery": [
        "Elite Foods Pvt Ltd","Britannia Industries Limited","Dream Bake India Pvt Ltd",
        "Elite Natural Pvt Ltd","Modern Food Enterprises Pvt Ltd","Prayagh Nutri Products Pvt Ltd",
        "Sona Biscuits Ltd","Saj Food Products Pvt Ltd","Modern Food Enterprises Pvt Ltd",
        "Bauli India Bake & Sweets Pvt Ltd"
    ],
    "Breakfast": [
        "Kellogg's India Pvt Ltd","Bagrry’s India Private Limited","Tata Consumer Products Ltd",
        "Marico Limited","Agro Tech Foods Limited","Sproutlife Foods Pvt Ltd",
        "Pagariya Food Products Pvt Ltd","Niva Nutrifoods LLP","HW Wellness Solutions Pvt Ltd",
        "Pepsico India Holding Pvt Ltd"
    ],
    "Packaged Atta": [
        "ITC Foods Limited","ITC Foods Limited","ITC Foods Limited","ITC Foods Limited",
        "ITC Foods Limited","General Mills","General Mills","General Mills",
        "Adani Wilmar Limited","Adani Wilmar Limited","Reliance Retail Limited",
        "Reliance Retail Limited","Elite Foods"
    ],
    "Atta-Brand": [
        "Aashirvaad Shudh Chakki","Aashirvaad Superior MP","Aashirvaad Multigrains",
        "Aashirvaad Sugar Control","Aashirvaad MP Chakki Atta","Pillsbury Chakki Fresh",
        "Pillsbury Multigrain","Pillsbury Multigrain","Fortune Chakki Fresh",
        "Fortune Sharbati","Independence","Good Life","Elite Chakki Atta"
    ]
}


# -----------------------------
# 📊 TABS FOR TABLES
# -----------------------------

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overall", "Mumbai", "Delhi", "Kolkata", "Chennai", "Bengaluru"
])

# -----------------------------
# OVERALL
# -----------------------------
with tab1:
    st.subheader("📊 Overall Category Top 10 Companies")
    st.dataframe(df_table, use_container_width=True, height=500, hide_index=True)

# -----------------------------
# MUMBAI
# -----------------------------
with tab2:
    df_mumbai = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data_mumbai.items()]))
    st.subheader("📊 Mumbai Category Mapping")
    st.dataframe(df_mumbai, use_container_width=True, height=500, hide_index=True)

# -----------------------------
# DELHI
# -----------------------------
with tab3:
    df_delhi = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in delhi_data.items()]))
    st.subheader("📊 Delhi Category Mapping")
    st.dataframe(df_delhi, use_container_width=True, height=500, hide_index=True)

# -----------------------------
# KOLKATA
# -----------------------------
with tab4:
    df_kolkata = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in kolkata_data.items()]))
    st.subheader("📊 Kolkata Category Mapping")
    st.dataframe(df_kolkata, use_container_width=True, height=500, hide_index=True)

# -----------------------------
# CHENNAI
# -----------------------------
with tab5:
    df_chennai = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in chennai_data.items()]))
    st.subheader("📊 Chennai Category Mapping")
    st.dataframe(df_chennai, use_container_width=True, height=500, hide_index=True)

# -----------------------------
# BENGALURU
# -----------------------------
with tab6:
    df_bengaluru = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in bengaluru_data.items()]))
    st.subheader("📊 Bengaluru Category Mapping")
    st.dataframe(df_bengaluru, use_container_width=True, height=500, hide_index=True)


st.subheader("📊 Subcategory Breakdown (Pivot Style)")

# FIX HERE 👇
categories = df['Category'].dropna().unique().tolist()

# Tabs
tabs = st.tabs(categories)

for tab, cat in zip(tabs, categories):

    with tab:
        st.markdown(f"### 📦 {cat}")

        df_cat = df[df['Category'] == cat]

        # Count
        subcat_count = df_cat['Sub Category'].value_counts().reset_index()
        subcat_count.columns = ['Sub Category', 'Count']

        # Percentage
        total = subcat_count['Count'].sum()
        subcat_count['Percentage'] = (subcat_count['Count'] / total) * 100

        # Format %
        subcat_count['Percentage'] = subcat_count['Percentage'].map(lambda x: f"{x:.2f}%")

        # Sort
        subcat_count = subcat_count.sort_values(by='Count', ascending=False)

        # Reorder
        subcat_count = subcat_count[['Sub Category', 'Percentage', 'Count']]

        st.dataframe(
            subcat_count,
            use_container_width=True,
            height=450,
            hide_index=True
        )

        st.info("📌 Shows contribution of each subcategory within this category.")