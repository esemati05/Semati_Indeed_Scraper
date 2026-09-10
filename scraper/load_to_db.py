import psycopg2
import os
import json
import glob
from datetime import datetime
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


def get_or_create_company(name):
    cur.execute("""
        INSERT INTO dim_company (company_name) VALUES (%s)
        ON CONFLICT (company_name) DO UPDATE SET company_name = EXCLUDED.company_name
        RETURNING company_id
    """, (name,))
    return cur.fetchone()[0]


def get_or_create_location(name):
    cur.execute("""
        INSERT INTO dim_location (location_name) VALUES (%s)
        ON CONFLICT (location_name) DO UPDATE SET location_name = EXCLUDED.location_name
        RETURNING location_id
    """, (name,))
    return cur.fetchone()[0]


def get_or_create_date(date_str):
    # date_str looks like "2026-09-03T13:32:53-04:00" — we just want the date part
    full_date = date_str[:10]
    dt = datetime.strptime(full_date, "%Y-%m-%d")
    cur.execute("""
        INSERT INTO dim_date (full_date, month, year) VALUES (%s, %s, %s)
        ON CONFLICT (full_date) DO UPDATE SET full_date = EXCLUDED.full_date
        RETURNING date_id
    """, (full_date, dt.month, dt.year))
    return cur.fetchone()[0]


# Loop through every JSON file in the data folder
files = glob.glob("data/*.json")
print(f"Found {len(files)} data files")

total_inserted = 0

for filepath in files:
    with open(filepath) as f:
        data = json.load(f)

    jobs = data["jobs"]

    for job in jobs:
        company_id = get_or_create_company(job["company_name"])
        location_id = get_or_create_location(job["location"]["name"])
        date_id = get_or_create_date(job["first_published"])

        cur.execute("""
            INSERT INTO job_postings_fact (job_id, title, company_id, location_id, date_id, absolute_url)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (job_id) DO NOTHING
        """, (job["id"], job["title"], company_id, location_id, date_id, job["absolute_url"]))

        total_inserted += 1

conn.commit()
print(f"Processed {total_inserted} job records")

cur.close()
conn.close()