import streamlit as st
import pandas as pd
import sqlite3

st.markdown("""
# 📊 Job Market Analysis Dashboard

#### 🚀 Explore salaries, roles, and trends in the data job market
""")

st.markdown("### 📊 Key Insights")

st.markdown("---")

df_csv = pd.read_csv("cleaned_data.csv")

conn = sqlite3.connect(":memory:")
df_csv.to_sql("jobs", conn, index=False, if_exists="replace")

exp = st.sidebar.selectbox(
    "Select Experience Level",
    df_csv['experience_level'].unique()
)

country = st.sidebar.selectbox(
    "Select Country",
    df_csv['company_location'].unique()
)

job = st.sidebar.selectbox(
    "Select Job Title",
    ["All"] + sorted(df_csv['job_title'].unique())
)

query = f"""
SELECT job_title, salary_in_usd, company_location, experience_level
FROM jobs
WHERE experience_level = '{exp}'
AND company_location = '{country}'
"""

# Apply job filter
if job != "All":
    query += f" AND job_title = '{job}'"

filtered_df = pd.read_sql(query, conn)
if filtered_df.empty:
    st.warning("No data available for selected filters")
    st.stop()

if filtered_df.empty:
    st.warning("No data available for selected filters")
    st.stop()

st.success(f"Showing data for: {exp}, {country}, {job}")
# 📊 Insights calculations
avg_salary = filtered_df['salary_in_usd'].mean()
max_salary = filtered_df['salary_in_usd'].max()
top_job = filtered_df.loc[filtered_df['salary_in_usd'].idxmax(), 'job_title']

st.markdown("### 💡 Key Insights")

st.info(f"""
💰 Average salary is around ${int(avg_salary) if pd.notna(avg_salary) else 0:,}  
🚀 Highest paying role is **{top_job}**  
📊 Maximum salary reaches ${int(max_salary):,}
""")
st.markdown("### 📊 Overview")
col1, col2, col3 = st.columns(3)

avg_salary = filtered_df['salary_in_usd'].mean()
max_salary = filtered_df['salary_in_usd'].max()
col1.metric(
    "💰 Avg Salary",
    f"${int(avg_salary):,}" if pd.notna(avg_salary) else "$0"
)

col2.metric(
    "🚀 Max Salary",
    f"${int(max_salary):,}" if pd.notna(max_salary) else "$0"
)

col3.metric(
    "📊 Total Jobs",
    f"{len(filtered_df):,}"
)

st.markdown("---")
# ----------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Salary Distribution")

import altair as alt

salary_df = filtered_df.copy()

# Step 1: create bins (ordered automatically)
salary_df['salary_range'] = pd.cut(
    salary_df['salary_in_usd'],
    bins=5
)

# Step 2: group (keeps correct order)
chart_data = salary_df.groupby('salary_range').size().reset_index(name='count')

# Step 3: convert labels AFTER grouping (important!)
chart_data['salary_range'] = chart_data['salary_range'].apply(
    lambda x: f"{int(x.left/1000)}k - {int(x.right/1000)}k"
)

# Step 4: create chart
chart = alt.Chart(chart_data).mark_bar().encode(
    x=alt.X('salary_range:N', title='Salary Range'),
    y=alt.Y('count:Q', title='Number of Jobs'),
    color=alt.Color('count:Q', scale=alt.Scale(scheme='blues')),
    tooltip=['salary_range', 'count']
)

st.altair_chart(chart, use_container_width=True)
st.info("💡 Insight: Most data roles fall in mid salary ranges, showing a balanced job market with fewer extreme high-paying roles.")

with col2:
    st.subheader("Top 10 Highest Paying Jobs")
    top_jobs = filtered_df.sort_values(by="salary_in_usd", ascending=False).head(10)
    st.dataframe(top_jobs[['job_title', 'salary_in_usd']])

st.subheader("Average Salary by Job Title")
job_salary = filtered_df.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False).head(10)
st.bar_chart(job_salary)

st.markdown("---")

st.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="filtered_jobs.csv"
)
st.subheader("🌍 Average Salary by Country")
country_salary = df_csv.groupby('company_location')['salary_in_usd'].mean().sort_values(ascending=False).head(10)
st.bar_chart(country_salary)

