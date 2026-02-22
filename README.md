# GEO Audit Tool for GymBeam Blog

## Overview

This project is a Python-based GEO (Generative Engine Optimization)
audit tool designed to analyze GymBeam blog articles and evaluate their
compliance with GEO optimization criteria.

The tool automatically:

-   Downloads blog articles
-   Extracts structured content
-   Evaluates articles using GEO criteria
-   Generates CSV and HTML reports
-   Provides recommendations for improvement

The goal is to assess how well articles are optimized for AI-driven
search engines such as ChatGPT, Perplexity, and Google SGE.

------------------------------------------------------------------------

## Project Structure

geo_audit/ 
├── main.py \# Main execution script\
├── analyzer.py \# Article analysis logic\
├── reporter.py \# CSV and HTML report generation\
├── to_json.py \# Article scraper and JSON generator\
│\
├── data/\
│ └── articles.json \# Stored article data\
│\
├── output/\
│ ├── report.csv\
│ └── report.html\
│\
└── README.md

------------------------------------------------------------------------

## How It Works

### Step 1: Download Articles

Run:

python to_json.py

This script:

-   Fetches GymBeam blog articles
-   Extracts:
    -   URL
    -   Title
    -   Meta description
    -   Article HTML
-   Saves them to:

data/articles.json

------------------------------------------------------------------------

### Step 2: Analyze Articles

Run:

python main.py

This script:

-   Loads articles from JSON
-   Analyzes each article using GEO criteria
-   Calculates a GEO score
-   Generates reports

Output files:

output/report.csv\
output/report.html

------------------------------------------------------------------------

## GEO Criteria Evaluated

Each article is evaluated using the following criteria:

-   direct_answer\
-   definition\
-   structured_headings\
-   contains_facts\
-   citation_sources\
-   faq_section\
-   contains_lists\
-   contains_tables\
-   adequate_length\
-   length_verify_md

Maximum score: 10

------------------------------------------------------------------------

## Output

### CSV Report

Structured table with results:

output/report.csv

Includes:

-   URL\
-   Title\
-   Score\
-   Individual criteria results\
-   Recommendations

------------------------------------------------------------------------

### HTML Report

Interactive report:

output/report.html

Features:

-   Color-coded scores\
-   Clickable article URLs\
-   Easy visualization

Score color system:

-   Green: 8--10 (Good GEO optimization)\
-   Orange: 5--7 (Needs improvement)\
-   Red: 0--4 (Poor optimization)

------------------------------------------------------------------------

## Error Handling

The tool safely handles:

-   Missing meta descriptions\
-   Missing article tags\
-   Missing headers\
-   Invalid HTML\
-   Missing tables or lists\
-   Missing JSON keys


------------------------------------------------------------------------

## Requirements

Install dependencies:

pip install beautifulsoup4

Python version:

Python 3.9+

------------------------------------------------------------------------

## Example Usage

python to_json.py\
python main.py

Output:

output/report.csv\
output/report.html

------------------------------------------------------------------------

## Purpose

This tool demonstrates:

-   Web scraping\
-   HTML parsing\
-   Error handling\
-   Automated content analysis\
-   Report generation\
-   GEO optimization evaluation

------------------------------------------------------------------------

## Author
Rastislav Pintér
Created as part of GymBeam GEO audit case study.
