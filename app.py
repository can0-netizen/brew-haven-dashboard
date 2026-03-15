import streamlit as st
import pandas as pd

st.title("Brew Haven Sales Dashboard 2025")

# Load Excel data
data = pd.read_excel("brew_haven_2025_dataset.xlsx")

# KPIs
total_revenue = data["Revenue"].sum()
total_profit = data["Profit"].sum()
total_orders = data["Order_ID"].count()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", total_revenue)
col2.metric("Total Profit", total_profit)
col3.metric("Total Orders", total_orders)

# Revenue trend
st.subheader("Revenue Trend")
revenue_trend = data.groupby("Month")["Revenue"].sum()
st.line_chart(revenue_trend)

# Revenue by category
st.subheader("Revenue by Category")
category_sales = data.groupby("Category")["Revenue"].sum()
st.bar_chart(category_sales)

# Top products
st.subheader("Top Selling Products")
top_products = data.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(5)
st.bar_chart(top_products)
