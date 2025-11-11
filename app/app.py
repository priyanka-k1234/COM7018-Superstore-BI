# app/app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- PAGE SETTINGS ----------
st.set_page_config(page_title="Superstore BI Dashboard", layout="wide")
st.title(" Superstore Business Intelligence Dashboard")

# ---------- LOAD DATA ----------
DATA_PATH = r"C:\Users\HP\OneDrive\Desktop\assesment_task\data\Sample - Superstore.csv"

@st.cache_data
def load_data(path):
    """Load dataset with correct encoding"""
    df = pd.read_csv(path, encoding='latin1')
    return df

try:
    df = load_data(DATA_PATH)
    st.success("Dataset loaded successfully!")
except Exception as e:
    st.error(f" Error loading dataset: {e}")
    st.stop()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header(" Filter Options")

regions = st.sidebar.multiselect(
    "Select Region(s):",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Select Category(ies):",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Apply filters dynamically
filtered_df = df.query("Region == @regions and Category == @categories")

# ---------- DATA PREVIEW ----------
st.subheader(" Data Preview")
st.dataframe(filtered_df.head(50), use_container_width=True)

# ---------- KPI SECTION ----------
st.subheader(" Key Performance Indicators")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")

st.caption("Data Source: Sample Superstore Dataset (Kaggle)")

# ---------- VISUALIZATIONS ----------
st.markdown("---")
st.subheader(" Visual Insights")

# --- Chart 1: Sales by Region ---
region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()
fig1 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="Sales by Region",
    color="Region",
    text_auto=".2s"
)
st.plotly_chart(fig1, use_container_width=True)

# --- Chart 2: Profit by Category ---
category_profit = filtered_df.groupby("Category")["Profit"].sum().reset_index()
fig2 = px.pie(
    category_profit,
    names="Category",
    values="Profit",
    title="Profit Distribution by Category",
    hole=0.4
)
st.plotly_chart(fig2, use_container_width=True)

# ---------- TREND ANALYSIS & TOP PRODUCTS ----------
st.markdown("---")
st.subheader(" Trend Analysis & Top Products")

# --- Chart 3: Monthly Sales Trend ---
# Ensure Order Date is datetime for both dataframes
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
filtered_df["Order Date"] = pd.to_datetime(filtered_df["Order Date"], errors="coerce")

# Group sales by month (use filtered data)
monthly_sales = (
    filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)
monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

fig3 = px.area(
    monthly_sales,
    x="Order Date",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True
)
st.plotly_chart(fig3, use_container_width=True)

# --- Chart 4: Top 10 Products by Sales ---
top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Sales",
    text_auto=".2s",
    color="Sales"
)
fig4.update_yaxes(categoryorder="total ascending")
st.plotly_chart(fig4, use_container_width=True)
