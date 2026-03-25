import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("jobs.db")
df = pd.read_sql("SELECT * FROM jobs", conn)

st.title("Job Market Dashboard")

# show data
st.write(df)

# salary chart
st.bar_chart(df['salary_in_usd'])

# filter by experience
exp = st.selectbox("Select Experience Level", df['experience_level'].unique())

filtered_df = df[df['experience_level'] == exp]

st.write(filtered_df)
st.write("Average Salary:", df['salary_in_usd'].mean())