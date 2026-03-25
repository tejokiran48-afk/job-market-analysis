import pandas as pd
import sqlite3

# load data
df = pd.read_csv("ds_salaries.csv")

# clean data
df = df.dropna()
df = df[['job_title', 'salary_in_usd', 'company_location', 'experience_level']]

# save to database
conn = sqlite3.connect("jobs.db")
df.to_sql("jobs", conn, if_exists="replace", index=False)
conn.close()

print("Data saved to database successfully")