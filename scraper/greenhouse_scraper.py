import requests
import json
from datetime import date

companies = ["stripe", "databricks", "anthropic", "airbnb", "figma", "asana"]

today = date.today().isoformat()

for company in companies:
    url = url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"
    response = requests.get(url)
    data = response.json()
    jobs = data["jobs"]

    print(f"Found {len(jobs)} jobs at {company}")

    filename = f"data/{company}_{today}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved to {filename}")