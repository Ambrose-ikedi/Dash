import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE SETTINGS
# ----------------------------

st.set_page_config(
    page_title="Kiwimbi Impact Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Kiwimbi Impact Dashboard")
st.markdown("Monitoring the reach and impact of Kiwimbi programs")

# ----------------------------
# GOOGLE SHEET CSV LINK
# ----------------------------

sheet_url = "https://docs.google.com/spreadsheets/d/1PakVqihxdWAomNUEOUYtL_36HEFv8rQD/export?format=csv"

# ----------------------------
# LOAD DATA
# ----------------------------

df = pd.read_csv(sheet_url)

# Convert date column
df["Date"] = pd.to_datetime(df["Date"])

# ----------------------------
# KPI CALCULATIONS
# ----------------------------

total_participants = df["Participants"].sum()
total_sessions = df.shape[0]
programs = df["Program"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Beneficiaries (Reach)", total_participants)
col2.metric("Total Sessions (Engagement)", total_sessions)
col3.metric("Active Programs", programs)

st.divider()

# ----------------------------
# PROGRAM PARTICIPATION
# ----------------------------

st.subheader("Program Participation")

program_counts = df.groupby("Program")["Participants"].sum().reset_index()

fig1 = px.bar(
    program_counts,
    x="Program",
    y="Participants",
    color="Program",
    title="Participants by Program"
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# PARTICIPATION OVER TIME
# ----------------------------

st.subheader("Growth Over Time")

trend = df.groupby("Date")["Participants"].sum().reset_index()

fig2 = px.line(
    trend,
    x="Date",
    y="Participants",
    markers=True,
    title="Participation Trend"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# PROGRAM DISTRIBUTION
# ----------------------------

st.subheader("Program Distribution")

fig3 = px.pie(
    program_counts,
    values="Participants",
    names="Program",
    title="Program Share of Beneficiaries"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# DATA TABLE
# ----------------------------

st.subheader("Program Data")

st.dataframe(df)