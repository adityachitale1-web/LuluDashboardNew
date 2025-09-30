import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Lulu Hypermarket Sales Dashboard", layout="wide")

# Load data
df = pd.read_csv("lulu_sales_data.csv", parse_dates=["Date"])

st.title("📊 Lulu Hypermarket UAE - Sales Dashboard")

# Sidebar filters
st.sidebar.header("Apply Filters")

gender_filter = st.sidebar.multiselect("Select Gender", options=df["Gender"].unique())
nationality_filter = st.sidebar.multiselect("Select Nationality", options=df["Nationality"].unique())
location_filter = st.sidebar.multiselect("Select Store Location", options=df["Store_Location"].unique())
category_filter = st.sidebar.multiselect("Select Product Category", options=df["Product_Category"].unique())

# Apply filters
filtered_df = df.copy()
if gender_filter:
    filtered_df = filtered_df[filtered_df["Gender"].isin(gender_filter)]
if nationality_filter:
    filtered_df = filtered_df[filtered_df["Nationality"].isin(nationality_filter)]
if location_filter:
    filtered_df = filtered_df[filtered_df["Store_Location"].isin(location_filter)]
if category_filter:
    filtered_df = filtered_df[filtered_df["Product_Category"].isin(category_filter)]

# Sales by location
st.subheader("Sales by Store Location")
sales_fig = px.bar(
    filtered_df.groupby("Store_Location")["Amount"].sum().reset_index(),
    x="Store_Location", y="Amount",
    labels={"Amount": "Sales Amount (AED)"}
)
st.plotly_chart(sales_fig, use_container_width=True)

# Transactions over time
st.subheader("Transaction Amount Over Time")
time_fig = px.scatter(
    filtered_df,
    x="Date", y="Amount",
    color="Product_Category",
    hover_data=["Transaction_ID", "Customer_Age", "Gender", "Nationality"]
)
st.plotly_chart(time_fig, use_container_width=True)

# Display table
st.subheader("Filtered Transactions")
st.dataframe(filtered_df)