# app/app.py

import streamlit as st
import pandas as pd

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
    st.success(" Dataset loaded successfully!")
except Exception as e:
    st.error(f" Error loading dataset: {e}")
    st.stop()

# ---------- DATA PREVIEW ----------
st.subheader(" Data Preview")
st.dataframe(df.head(50), use_container_width=True)

# ---------- KPI SECTION ----------
st.subheader("Key Performance Indicators")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")

st.caption(" Data Source: Sample Superstore Dataset (Kaggle)")

# ---------- KPI SECTION ----------
st.subheader(" Key Performance Indicators")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")

st.caption(" Data Source: Sample Superstore Dataset (Kaggle)")

# ---------- VISUALIZATIONS ----------
import plotly.express as px
st.markdown("---")
st.subheader(" Visual Insights")

# --- Chart 1: Sales by Region ---
region_sales = df.groupby("Region")["Sales"].sum().reset_index()
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
category_profit = df.groupby("Category")["Profit"].sum().reset_index()
fig2 = px.pie(
    category_profit,
    names="Category",
    values="Profit",
    title="Profit Distribution by Category",
    hole=0.4
)
st.plotly_chart(fig2, use_container_width=True)

