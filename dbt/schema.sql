CREATE TABLE dim_company (
    company_id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL UNIQUE
);

CREATE TABLE dim_location (
    location_id SERIAL PRIMARY KEY,
    location_name TEXT NOT NULL UNIQUE
);

CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    month INT NOT NULL,
    year INT NOT NULL
);

CREATE TABLE dim_skill (
    skill_id SERIAL PRIMARY KEY,
    skill_name TEXT NOT NULL UNIQUE
);

CREATE TABLE job_postings_fact (
    job_id BIGINT PRIMARY KEY,
    title TEXT NOT NULL,
    company_id INT REFERENCES dim_company(company_id),
    location_id INT REFERENCES dim_location(location_id),
    date_id INT REFERENCES dim_date(date_id),
    absolute_url TEXT
);

CREATE TABLE job_skills_bridge (
    job_id BIGINT REFERENCES job_postings_fact(job_id),
    skill_id INT REFERENCES dim_skill(skill_id),
    PRIMARY KEY (job_id, skill_id)
);