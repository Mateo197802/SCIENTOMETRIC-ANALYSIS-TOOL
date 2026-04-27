# Scientometric Analysis Tool

An automated, multi-source scientometric data pipeline using LLMs and API orchestration to extract, disambiguate, and classify global research data. 

This tool eliminates the problem of author name collisions and fragmented profiles by utilizing an interconnected, multi-source approach: reading raw metadata from OpenAlex and PubMed, resolving missing identifiers using Scopus and Semantic Scholar, searching for public Google Scholar profiles, and using an LLM to accurately infer demographics and scientific expertise.

## 🚀 Architecture Overview

The pipeline strictly takes a curated CSV list of DOIs to prevent false positives and processes each paper through a sequence of extraction nodes:

1. **OpenAlex Node**: Acts as the foundation. Extracts paper metadata, open access status, author lists, raw affiliations, and lifetime topics.
2. **PubMed Node**: Validates medical papers, extracts strict MeSH terms, and searches for "ghost authors" missing from OpenAlex.
3. **Scopus Node**: Uses the institutional IP/API to extract deep metrics: Official H-Index, lifetime citations, document count, and Seniority (years active).
4. **Semantic Scholar Node**: Extracts influential citations and provides a fallback ID and H-Index to contrast with Scopus.
5. **Google Scholar Node**: Extracts the author's public interests/topics using SerpApi. Features a fallback mechanism that injects OpenAlex Concepts if the author has no public profile.
6. **ORCID Node**: Queries the ORCID API using extracted IDs to capture precise, granular department and current employment data.
7. **Enrichment Node**: 
   - Uses `genderize.io` to automatically infer the author's gender.
   - Uses **Azure OpenAI (GPT-4o)** with `temperature=0.0` to process the entire profile and deterministically classify the author's primary role (e.g., `CLINICAL`, `COMPUTER_SCIENCE`, `HYBRID_MED_TECH`).

## 📁 Repository Structure

```text
SCIENTOMETRIC-ANALYSIS-TOOL/
├── src/                      # Source code
│   ├── main.py               # Main orchestration script
│   ├── config.py             # Configuration and keys loader
│   ├── enrichment.py         # LLM logic and gender classification
│   └── modules/              # Individual API extractors
├── scripts/                  
│   └── evaluator.py          # Script to generate evaluation graphs and metrics
├── data/
│   ├── input/                # Place your input_dois.csv here
│   └── output/               # Generates MASTER_AUTHOR_TABLE.csv
├── assets/
│   └── figures/              # Heatmaps, Radars, and Output Graphs
├── .gitignore
├── requirements.txt
└── README.md
```

## 🛠️ Usage

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys:**
   Create a `.env` file inside `src/` (use `.env_sample` as a template) and add your keys for Azure OpenAI, SerpApi, PubMed, and Scopus.

3. **Run the Extraction:**
   Place your DOIs in `data/input/input_dois.csv` containing at least a `DOI` column.
   ```bash
   python src/main.py
   ```
   The final dense dataset will be saved to `data/output/MASTER_AUTHOR_TABLE.csv`.

4. **Generate Evaluation Reports:**
   To benchmark the extraction fidelity against raw OpenAlex data and generate data completeness heatmaps:
   ```bash
   python scripts/evaluator.py
   ```
   Graphs will be saved to `assets/figures/`.

## 📊 Final Output Columns
The `MASTER_AUTHOR_TABLE.csv` provides a complete radiography of each researcher:
- `AUTHOR_NAME`, `ORCID`, `HINDEX_SC`, `CITATIONS_SC`, `SENIORITY_SC`
- `AFFILIATION_OA`, `GEO_COUNTRY_OA`, `ORCID_EMPLOYMENT`
- `KEYWORDS_OA`, `MESH_PM`, `INTERESTS_GS`, `SUBJECT_AREAS_SC`
- `GENDER`, `PROFILE_CLASSIFICATION` (LLM Output)
