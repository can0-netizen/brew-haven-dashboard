import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE SETTINGS
# -----------------------------

st.set_page_config(
    page_title="Brew Haven Dashboard",
    page_icon="☕",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------

st.title("☕ Brew Haven Sales Dashboard 2025")
st.markdown("### Coffee Shop Business Performance")
st.markdown("---")

# -----------------------------
# LOAD DATA
# -----------------------------

data = pd.read_excel("brew_haven_2025_dataset.xlsx")

# Clean column names
data.columns = data.columns.str.strip()

# Convert date
data["Date"] = pd.to_datetime(data["Date"])
data["Month"] = data["Date"].dt.month_name()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------

st.sidebar.header("Filters")

branch_filter = st.sidebar.multiselect(
    "Select Branch",
    options=data["Branch"].unique(),
    default=data["Branch"].unique()
)

payment_filter = st.sidebar.multiselect(
    "Payment Method",
    options=data["Payment_Method"].unique(),
    default=data["Payment_Method"].unique()
)

filtered_data = data[
    (data["Branch"].isin(branch_filter)) &
    (data["Payment_Method"].isin(payment_filter))
]

# -----------------------------
# KPI CARDS
# -----------------------------

total_revenue = filtered_data["Sales_Revenue"].sum()
total_profit = filtered_data["Gross_Profit"].sum()
total_orders = filtered_data["Transaction_ID"].count()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", total_orders)

st.markdown("---")

# -----------------------------
# CHARTS ROW 1
# -----------------------------

col4, col5 = st.columns(2)

with col4:
    monthly_sales = filtered_data.groupby("Month")["Sales_Revenue"].sum().reset_index()
    fig1 = px.line(
        monthly_sales,
        x="Month",
        y="Sales_Revenue",
        title="Monthly Revenue Trend",
        markers=True
    )
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    category_sales = filtered_data.groupby("Category")["Sales_Revenue"].sum().reset_index()
    fig2 = px.pie(
        category_sales,
        names="Category",
        values="Sales_Revenue",
        title="Revenue by Category",
        hole=0.4
    )
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# CHARTS ROW 2
# -----------------------------

col6, col7 = st.columns(2)

with col6:
    top_products = (
        filtered_data.groupby("Product")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    fig3 = px.bar(
        top_products,
        x="Product",
        y="Quantity",
        title="Top 5 Selling Products",
        color="Quantity"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col7:
    payment_sales = filtered_data.groupby("Payment_Method")["Sales_Revenue"].sum().reset_index()
    fig4 = px.bar(
        payment_sales,
        x="Payment_Method",
        y="Sales_Revenue",
        title="Sales by Payment Method",
        color="Sales_Revenue"
    )
    st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# OPTIONAL DATA TABLE
# -----------------------------

if st.checkbox("Show Transaction Data"):
    st.dataframe(filtered_data)
