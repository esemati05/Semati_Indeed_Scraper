# Job Skills Pipeline

An end-to-end data pipeline that scrapes live job postings from major tech companies,
stores them in a structured data warehouse, and extracts in-demand data engineering
skills — using the results to directly inform my own resume.

## What it does
1. **Scrapes** job postings from multiple companies via their public Greenhouse ATS APIs
2. **Lands** raw data in a local data lake (dated JSON snapshots)
3. **Loads** the data into a Postgres warehouse using a star schema (fact + dimension tables)
4. **Extracts** skill mentions from job descriptions using keyword matching
5. **Visualizes** the results in an interactive Streamlit dashboard

## Architecture

Greenhouse API → raw JSON (data lake) → Postgres star schema (warehouse) → skill extraction → Streamlit dashboard

## Tech Stack
- **Python** (requests, psycopg2) — scraping and data loading
- **PostgreSQL** — data warehouse, dimensional modeling
- **Streamlit + Plotly** — interactive dashboard
- **Git/GitHub** — version control

## Key Findings (as of latest run)
- Analyzed 2,500+ job postings across 6 major tech companies
- Python and SQL are the most in-demand skills, followed by cloud platforms (AWS, Azure, GCP)
- [Add more findings as you expand the company list]

## Project Structure
scraper/ — scraping and data loading scripts
dbt/ — database schema definitions
dashboard/ — Streamlit dashboard app
data/ — raw scraped JSON (gitignored)


## Running it locally
1. `pip install -r requirements.txt`
2. Set up a `.env` file with your Postgres credentials
3. `python3 scraper/greenhouse_scraper.py`
4. `python3 scraper/load_to_db.py`
5. `python3 scraper/extract_skills.py`
6. `streamlit run dashboard/app.py`