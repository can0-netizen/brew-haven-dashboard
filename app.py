import streamlit as st
import pandas as pd

# Dashboard title
st.title("Brew Haven Sales Dashboard 2025")

# Load Excel dataset
data = pd.read_excel("brew_haven_2025_dataset.xlsx")
print(data.columns)
# Convert date column to datetime
data["date"] = pd.to_datetime(data["date"])

# Create a month column from the date
data["month"] = data["date"].dt.month

# ---------------------------
# KPI SECTION
# ---------------------------

total_revenue = data["sales_revenue"].sum()
total_profit = data["gross_profit"].sum()
total_orders = data["transaction_id"].count()

# Create 3 columns for KPI cards
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", total_orders)

# ---------------------------
# REVENUE TREND
# ---------------------------

st.subheader("Monthly Revenue Trend")

revenue_trend = data.groupby("month")["sales_revenue"].sum()

st.line_chart(revenue_trend)

# ---------------------------
# CATEGORY SALES
# ---------------------------

st.subheader("Revenue by Coffee Category")

category_sales = data.groupby("category")["sales_revenue"].sum()

st.bar_chart(category_sales)

# ---------------------------
# TOP PRODUCTS
# ---------------------------

st.subheader("Top Selling Coffee Products")

top_products = (
    data.groupby("product")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.bar_chart(top_products)
