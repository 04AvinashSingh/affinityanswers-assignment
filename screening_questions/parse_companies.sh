#!/bin/bash
# Fetch the CSV and parse it using a robust inline python processor to handle commas inside quotes

URL="https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"

curl -sL "$URL" | python3 -c '
import csv, sys, re

reader = csv.DictReader(sys.stdin)
companies = []

for row in reader:
    name = row.get("Security", "").strip()
    loc = row.get("Headquarters Location", "").strip()
    founded = row.get("Founded", "").strip()
    
    # Extract the first 4-digit number for sorting (e.g., "1888 (1923)" -> 1888)
    match = re.search(r"\d{4}", founded)
    sort_year = int(match.group(0)) if match else 9999
    
    companies.append({
        "name": name,
        "loc": loc,
        "founded": founded,
        "sort_year": sort_year
    })

# Sort companies by founded year (oldest first)
companies.sort(key=lambda x: (x["sort_year"], x["name"]))

# Print table header
header_name = "Company Name"
header_loc = "Headquarters"
header_founded = "Founded"
print(f"{header_name:<45} | {header_loc:<30} | {header_founded}")
print("-" * 90)

for c in companies:
    name_str = c["name"]
    loc_str = c["loc"]
    found_str = c["founded"]
    print(f"{name_str:<45} | {loc_str:<30} | {found_str}")
'
