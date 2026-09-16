import psycopg2
import os
import re
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

SKILLS = [
    "Python", "SQL", "Java", "Scala", "R",
    "Airflow", "dbt", "Spark", "Kafka", "Hadoop",
    "AWS", "GCP", "Azure", "Snowflake", "Redshift", "BigQuery",
    "Docker", "Kubernetes", "Terraform",
    "PostgreSQL", "MySQL", "MongoDB",
    "ETL", "Tableau", "Power BI", "Looker"
]


def get_or_create_skill(name):
    cur.execute("""
        INSERT INTO dim_skill (skill_name) VALUES (%s)
        ON CONFLICT (skill_name) DO UPDATE SET skill_name = EXCLUDED.skill_name
        RETURNING skill_id
    """, (name,))
    return cur.fetchone()[0]


# Pre-create all skill rows once, and remember their IDs
skill_ids = {}
for skill in SKILLS:
    skill_ids[skill] = get_or_create_skill(skill)

conn.commit()

# Build one regex pattern per skill for whole-word, case-insensitive matching
patterns = {
    skill: re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
    for skill in SKILLS
}

# Pull every job's title + description together
cur.execute("SELECT job_id, title, description FROM job_postings_fact")
jobs = cur.fetchall()
print(f"Scanning {len(jobs)} jobs for skill mentions")

total_matches = 0

for job_id, title, description in jobs:
    text = (title or "") + " " + (description or "")

    for skill, pattern in patterns.items():
        if pattern.search(text):
            cur.execute("""
                INSERT INTO job_skills_bridge (job_id, skill_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (job_id, skill_ids[skill]))
            total_matches += 1

conn.commit()
print(f"Inserted {total_matches} job-skill matches")

cur.close()
conn.close()