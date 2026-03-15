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
st.markdown("### Coffee Shop Business Performance Overview")
st.markdown("---")

# -----------------------------
# LOAD DATA
# -----------------------------
data = pd.read_excel("brew_haven_2025_dataset.xlsx")
data.columns = data.columns.str.strip()
data["Date"] = pd.to_datetime(data["Date"])
data["Month"] = data["Date"].dt.month_name()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

# Branch filter
branch_filter = st.sidebar.multiselect(
    "Select Branch",
    options=data["Branch"].unique(),
    default=data["Branch"].unique()
)

# Payment Method filter
payment_filter = st.sidebar.multiselect(
    "Payment Method",
    options=data["Payment_Method"].unique(),
    default=data["Payment_Method"].unique()
)

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    [data["Date"].min(), data["Date"].max()]
)

# Apply filters
filtered_data = data[
    (data["Branch"].isin(branch_filter)) &
    (data["Payment_Method"].isin(payment_filter)) &
    (data["Date"] >= pd.to_datetime(date_range[0])) &
    (data["Date"] <= pd.to_datetime(date_range[1]))
]

# -----------------------------
# KPI CARDS
# -----------------------------
total_revenue = filtered_data["Sales_Revenue"].sum()
total_profit = filtered_data["Gross_Profit"].sum()
total_orders = filtered_data["Transaction_ID"].count()

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
kpi_col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
kpi_col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
kpi_col3.metric("🛒 Total Orders", total_orders)

st.markdown("---")

# -----------------------------
# CHARTS ROW 1: Revenue Trend & Category
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    monthly_sales = (
        filtered_data.groupby("Month")["Sales_Revenue"]
        .sum()
        .reset_index()
    )
    fig1 = px.line(
        monthly_sales,
        x="Month",
        y="Sales_Revenue",
        title="Monthly Revenue Trend",
        markers=True,
        template="plotly_white",
        color_discrete_sequence=["#6f4e37"]  # Coffee brown
    )
    fig1.update_layout(title_font_size=18, xaxis_title="Month", yaxis_title="Revenue")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    category_sales = (
        filtered_data.groupby("Category")["Sales_Revenue"]
        .sum()
        .reset_index()
    )
    fig2 = px.pie(
        category_sales,
        names="Category",
        values="Sales_Revenue",
        title="Revenue by Category",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Burgyl
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# CHARTS ROW 2: Top Products & Payment Method
# -----------------------------
col3, col4 = st.columns(2)

with col3:
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
        color="Quantity",
        color_continuous_scale=px.colors.sequential.Oranges
    )
    fig3.update_layout(title_font_size=18, xaxis_title="Product", yaxis_title="Quantity Sold")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    payment_sales = (
        filtered_data.groupby("Payment_Method")["Sales_Revenue"]
        .sum()
        .reset_index()
    )
    fig4 = px.bar(
        payment_sales,
        x="Payment_Method",
        y="Sales_Revenue",
        title="Sales by Payment Method",
        color="Sales_Revenue",
        color_continuous_scale=px.colors.sequential.Teal
    )
    fig4.update_layout(title_font_size=18, xaxis_title="Payment Method", yaxis_title="Revenue")
    st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# OPTIONAL DATA TABLE
# -----------------------------
if st.checkbox("Show Transaction Data"):
    st.dataframe(filtered_data)
