import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Kiwimbi Impact Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Kiwimbi Impact Dashboard")
st.write("Monitoring reach and engagement across programs")

# Google Sheets CSV link
sheet_url = "https://docs.google.com/spreadsheets/d/1PakVqihxdWAomNUEOUYtL_36HEFv8rQD/export?format=csv"

# Load data
df = pd.read_csv(sheet_url)

# Clean column names
df.columns = df.columns.str.strip()

# KPIs
total_attendance = df["Totals attandance"].sum()
total_meals = df["Meals Served"].sum()
total_books = df["Books Borrowed"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Attendance", total_attendance)
col2.metric("Meals Served", total_meals)
col3.metric("Books Borrowed", total_books)

st.divider()

# Attendance trend
st.subheader("Monthly Attendance Trend")

fig1 = px.line(
    df,
    x="Month",
    y="Totals attandance",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# Program participation comparison
st.subheader("Program Participation")

program_data = df[[
    "Month",
    "Library Attendance",
    "Mentorship Attendance",
    "STEM Participants",
    "Arts Participants",
    "Sports Participants"
]]

program_data = program_data.melt(
    id_vars="Month",
    var_name="Program",
    value_name="Participants"
)

fig2 = px.bar(
    program_data,
    x="Month",
    y="Participants",
    color="Program",
    barmode="group"
)

st.plotly_chart(fig2, use_container_width=True)

# Meals trend
st.subheader("Meals Served per Month")

fig3 = px.bar(
    df,
    x="Month",
    y="Meals Served"
)

st.plotly_chart(fig3, use_container_width=True)

# Table
st.subheader("Dataset")
st.dataframe(df)