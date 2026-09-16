import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

st.title("Data Engineering Job Market — Skills Analysis")
st.write("Analysis of live job postings from Stripe, Databricks, Anthropic, Airbnb, Figma, and Asana")

# Query: skill frequency
query = """
    SELECT skill_name, COUNT(*) AS mentions
    FROM job_skills_bridge
    JOIN dim_skill ON job_skills_bridge.skill_id = dim_skill.skill_id
    GROUP BY skill_name
    ORDER BY mentions DESC
"""
df = pd.read_sql(query, conn)

st.subheader("Most In-Demand Skills")
fig = px.bar(df, x="skill_name", y="mentions", title="Skill Mentions Across All Job Postings")
st.plotly_chart(fig)

st.subheader("Raw Data")
st.dataframe(df)

conn.close()