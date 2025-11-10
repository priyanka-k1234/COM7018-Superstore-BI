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
