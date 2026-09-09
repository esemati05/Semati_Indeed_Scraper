import requests
import json
from datetime import date

# The company's Greenhouse board token (their slug in the API URL)
company = "stripe"
url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

# Send the request and get the response back
response = requests.get(url)

# Convert the raw JSON text into a Python data structure
data = response.json()

# Pull out just the list of jobs
jobs = data["jobs"]
print(f"Found {len(jobs)} jobs at {company}")

# Save the raw, untouched data to a file, named with today's date
today = date.today().isoformat()  # e.g. "2026-09-08"
filename = f"data/{company}_{today}.json"

with open(filename, "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved raw data to {filename}")