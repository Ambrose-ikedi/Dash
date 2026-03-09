import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Kiwimbi Impact Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Kiwimbi Impact Dashboard")

# Google Sheet CSV link
sheet_url = "https://docs.google.com/spreadsheets/d/1PakVqihxdWAomNUEOUYtL_36HEFv8rQD/export?format=csv"

# Load data
df = pd.read_csv(sheet_url)

# Clean column names
df.columns = df.columns.str.strip()

# Show detected columns (important for debugging)
st.write("Detected columns:", df.columns)

# Check required columns
required_columns = ["Date", "Program", "Participants"]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"Missing columns in Google Sheet: {missing}")
    st.stop()

# Convert date
df["Date"] = pd.to_datetime(df["Date"])

# KPIs
total_participants = df["Participants"].sum()
total_sessions = len(df)
programs = df["Program"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Beneficiaries (Reach)", total_participants)
col2.metric("Total Sessions (Engagement)", total_sessions)
col3.metric("Active Programs", programs)

st.divider()

# Program participation
program_counts = df.groupby("Program")["Participants"].sum().reset_index()

fig1 = px.bar(
    program_counts,
    x="Program",
    y="Participants",
    color="Program",
    title="Participants by Program"
)

st.plotly_chart(fig1, use_container_width=True)

# Growth over time
trend = df.groupby("Date")["Participants"].sum().reset_index()

fig2 = px.line(
    trend,
    x="Date",
    y="Participants",
    markers=True,
    title="Participation Trend"
)

st.plotly_chart(fig2, use_container_width=True)

# Distribution
fig3 = px.pie(
    program_counts,
    values="Participants",
    names="Program",
    title="Program Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

# Data table
st.subheader("Program Data")
st.dataframe(df)