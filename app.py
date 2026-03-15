st.set_page_config(layout="wide")
import streamlit as st
import pandas as pd

# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("☕ Brew Haven Sales Dashboard 2025")

# -----------------------------
# LOAD DATA
# -----------------------------

data = pd.read_excel("brew_haven_2025_dataset.xlsx")

# Clean column names (removes spaces)
data.columns = data.columns.str.strip()

# Convert date column to datetime
data["Date"] = pd.to_datetime(data["Date"])

# Create Month column
data["Month"] = data["Date"].dt.month_name()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------

st.sidebar.header("Dashboard Filters")

branch_filter = st.sidebar.multiselect(
    "Select Branch",
    options=data["Branch"].unique(),
    default=data["Branch"].unique()
)

payment_filter = st.sidebar.multiselect(
    "Select Payment Method",
    options=data["Payment_Method"].unique(),
    default=data["Payment_Method"].unique()
)

# Apply filters
filtered_data = data[
    (data["Branch"].isin(branch_filter)) &
    (data["Payment_Method"].isin(payment_filter))
]

# -----------------------------
# KPI METRICS
# -----------------------------

total_revenue = filtered_data["Sales_Revenue"].sum()
total_profit = filtered_data["Gross_Profit"].sum()
total_orders = filtered_data["Transaction_ID"].count()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", total_orders)

# -----------------------------
# MONTHLY REVENUE TREND
# -----------------------------

st.subheader("📈 Monthly Revenue Trend")

monthly_revenue = filtered_data.groupby("Month")["Sales_Revenue"].sum()

st.line_chart(monthly_revenue)

# -----------------------------
# REVENUE BY CATEGORY
# -----------------------------

st.subheader("☕ Revenue by Coffee Category")

category_sales = filtered_data.groupby("Category")["Sales_Revenue"].sum()

st.bar_chart(category_sales)

# -----------------------------
# TOP SELLING PRODUCTS
# -----------------------------

st.subheader("🔥 Top 5 Selling Products")

top_products = (
    filtered_data.groupby("Product")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.bar_chart(top_products)

# -----------------------------
# SALES BY PAYMENT METHOD
# -----------------------------

st.subheader("💳 Sales by Payment Method")

payment_sales = filtered_data.groupby("Payment_Method")["Sales_Revenue"].sum()

st.bar_chart(payment_sales)

# -----------------------------
# SHOW DATA TABLE
# -----------------------------

st.subheader("📄 Transaction Data")

st.dataframe(filtered_data)
