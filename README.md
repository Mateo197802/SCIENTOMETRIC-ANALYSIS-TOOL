# Scientometric Analysis Tool

A modular, multi-source scientometric data pipeline for large-scale author profiling and bibliometric analysis. The system extracts, disambiguates, enriches, and classifies research author metadata from academic publications using API orchestration and large language models (LLMs).

Developed as part of a research initiative at the **Massachusetts Institute of Technology (MIT)**, this tool supports studies on global research equity, authorship dynamics, and scientometric disparities in biomedical and computational sciences.

---

## Overview

Given a curated list of DOIs, the pipeline extracts comprehensive metadata for every author across multiple academic databases, resolves identity ambiguities through fuzzy matching, enriches profiles with employment and demographic data, and applies deterministic LLM classification to categorize each researcher by discipline and role.

The output is a single, unified dataset (`MASTER_AUTHOR_TABLE`) containing 35 structured columns per author record, suitable for downstream statistical analysis, visualization, and publication.

---

## Architecture

The pipeline processes each DOI sequentially through a chain of extraction nodes, with automatic checkpointing after every DOI to enable fault-tolerant resumption.

```
INPUT                        EXTRACTION NODES                              OUTPUT
+-----------------+    +------------------------------------------+    +---------------------+
| input_dois.csv  | -> | OpenAlex -> PubMed -> Semantic Scholar   | -> | MASTER_AUTHOR_TABLE |
| (DOI list)      |    | -> ORCID -> Genderize -> Azure GPT-4o   |    | (.csv + .json)      |
+-----------------+    +------------------------------------------+    +---------------------+
```

### Extraction Nodes

| Node | Source | Data Extracted |
|------|--------|----------------|
| **OpenAlex** | OpenAlex API | Paper title, year, open access status, funding sources, author names, positions, affiliations, country, H-index, citations, i10-index, topics, keywords |
| **PubMed** | NCBI E-utilities | PMID, MeSH terms, funding agencies, author names, institutional affiliations |
| **Semantic Scholar** | S2 API | Influential citation count, citation contexts, author IDs, ORCID, H-index, total citations |
| **ORCID** | ORCID Public API | Current employment (institution, department, city, country) |
| **Genderize** | Genderize.io | Gender inference from first name (5-key round-robin rotation) |
| **Azure GPT-4o** | Azure OpenAI | Deterministic profile classification (e.g., CLINICAL, COMPUTER_SCIENCE, HYBRID_MED_TECH) |

### Deactivated Nodes

| Node | Reason |
|------|--------|
| **Scopus** | Requires institutional IP with valid API key; returns HTTP 401 without verified access |
| **Google Scholar** | SerpAPI integration available but disabled for current run |

### Fault Tolerance

- A checkpoint file (`pipeline_checkpoint.json`) is written after each successfully processed DOI
- If the pipeline is interrupted (network failure, system restart, API timeout), re-running `main.py` automatically resumes from the last checkpoint
- Upon successful completion, the checkpoint file is removed

---

## Repository Structure

```
SCIENTOMETRIC-ANALYSIS-TOOL/
├── src/
│   ├── main.py                    # Pipeline orchestrator with checkpoint logic
│   ├── config.py                  # Environment variable loader (.env parsing)
│   └── modules/
│       ├── openalex.py            # OpenAlex API extraction
│       ├── pubmed.py              # PubMed / NCBI E-utilities extraction
│       ├── semantic_scholar.py    # Semantic Scholar API extraction
│       ├── scopus.py              # Scopus API extraction (deactivated)
│       ├── google_scholar.py      # Google Scholar via SerpAPI (deactivated)
│       ├── orcid.py               # ORCID employment data extraction
│       └── enrichment.py          # Gender inference + LLM profile classification
├── scripts/
│   ├── analytics.py               # Generates publication-quality analytical figures
│   └── evaluator.py               # Validates extraction accuracy against OpenAlex web data
├── data/
│   ├── input/
│   │   └── input_dois.csv         # Input: one DOI per row
│   └── output/
│       ├── csv/
│       │   └── MASTER_AUTHOR_TABLE.csv    # Primary output
│       └── json/
│           └── MASTER_AUTHOR_TABLE.json   # JSON mirror of the primary output
├── assets/
│   └── figures/
│       ├── analytics/             # Analytical figures (H-index disparity, profiles, parachute index)
│       └── *.png                  # Evaluation figures (accuracy, completeness, coverage)
├── .env                           # API keys and configuration (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Output Schema

The `MASTER_AUTHOR_TABLE` contains 35 columns per author record:

### Paper Metadata
| Column | Source | Description |
|--------|--------|-------------|
| `PAPER_TITLE` | OpenAlex | Title of the publication |
| `DOI` | Input | Digital Object Identifier |
| `YEAR` | OpenAlex | Publication year |
| `OPEN_ACCESS_OA` | OpenAlex | Open access status and type |
| `FUNDING_OA` | OpenAlex | Funding sources (parsed from `funders` field) |

### Author Identity and Affiliation
| Column | Source | Description |
|--------|--------|-------------|
| `AUTHOR_NAME` | OpenAlex | Author display name |
| `AUTHOR_POS_OA` | OpenAlex | Authorship position (first, middle, last) |
| `IS_CORRESPONDING_OA` | OpenAlex | Corresponding author flag |
| `AFFILIATION_OA` | OpenAlex | Primary institutional affiliation |
| `GEO_COUNTRY_OA` | OpenAlex | Country of affiliation (ISO code) |
| `AUTHOR_ID_OA` | OpenAlex | OpenAlex author identifier |
| `ORCID` | OpenAlex/S2 | Consolidated ORCID identifier |

### Bibliometric Indicators
| Column | Source | Description |
|--------|--------|-------------|
| `WORKS_COUNT_OA` | OpenAlex | Total publications by author |
| `CITATIONS_OA` | OpenAlex | Lifetime citation count |
| `HINDEX_OA` | OpenAlex | H-index |
| `I10INDEX_OA` | OpenAlex | i10-index |
| `2YR_MEAN_OA` | OpenAlex | Two-year mean citedness |

### Topic and Keyword Classification
| Column | Source | Description |
|--------|--------|-------------|
| `TOPICS_OA` | OpenAlex | Research topics |
| `PRIMARY_TOPIC_OA` | OpenAlex | Primary research topic |
| `KEYWORDS_OA` | OpenAlex | Author keywords |

### PubMed Data
| Column | Source | Description |
|--------|--------|-------------|
| `PMID_PM` | PubMed | PubMed identifier |
| `MESH_PM` | PubMed | MeSH subject headings |
| `FUNDING_PM` | PubMed | Funding information from PubMed |
| `AUTHOR_NAME_PM` | PubMed | Author name as indexed in PubMed |
| `AFFILIATION_PM` | PubMed | Affiliation as indexed in PubMed |

### Semantic Scholar Data
| Column | Source | Description |
|--------|--------|-------------|
| `INFLUENTIAL_CITATIONS_SS` | S2 | Influential citation count |
| `CITATION_CONTEXTS_SS` | S2 | Citation context snippets |
| `AUTHOR_ID_SS` | S2 | Semantic Scholar author identifier |
| `AUTHOR_NAME_SS` | S2 | Author name in Semantic Scholar |
| `ORCID_SS` | S2 | ORCID from Semantic Scholar |
| `HINDEX_SS` | S2 | H-index from Semantic Scholar |
| `CITATIONS_SS` | S2 | Citation count from Semantic Scholar |

### Enrichment Data
| Column | Source | Description |
|--------|--------|-------------|
| `ORCID_EMPLOYMENT` | ORCID API | Current employment (institution, department, location) |
| `GENDER` | Genderize.io | Inferred gender |
| `PROFILE_CLASSIFICATION` | Azure GPT-4o | Deterministic role classification |

---

## Installation and Usage

### Prerequisites

- Python 3.12 or higher
- API access credentials (see Configuration section below)

### Setup

```bash
# Clone the repository
git clone https://github.com/Mateo197802/SCIENTOMETRIC-ANALYSIS-TOOL.git
cd SCIENTOMETRIC-ANALYSIS-TOOL

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt
pip install matplotlib seaborn   # Required for analytics and evaluation scripts
```

### Configuration

Create a `.env` file in the project root with the following variables:

```env
# OpenAlex (Polite Pool - use institutional email)
OPENALEX_KEY=your_email@institution.edu
OPENALEX_DELAY=1.0
OPENALEX_ACTIVE=true

# PubMed / NCBI
PUBMED_KEY=your_ncbi_api_key
PUBMED_DELAY=0.5
PUBMED_ACTIVE=true

# Semantic Scholar
SEMANTIC_KEY=
SEMANTIC_DELAY=1.0
SEMANTIC_ACTIVE=true

# Scopus (requires institutional IP)
SCOPUS_KEY=your_scopus_key
SCOPUS_DELAY=1.0
SCOPUS_ACTIVE=false

# Google Scholar (SerpAPI)
SCHOLAR_KEY=your_serpapi_key
SCHOLAR_DELAY=1.0
SCHOLAR_ACTIVE=false

# Azure OpenAI (GPT-4o)
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/

# Genderize.io (up to 5 keys for round-robin rotation)
GENDERIZE_KEY_1=your_key_1
GENDERIZE_KEY_2=your_key_2
GENDERIZE_KEY_3=your_key_3
GENDERIZE_KEY_4=your_key_4
GENDERIZE_KEY_5=your_key_5
```

### Running the Pipeline

```bash
# Place your DOIs in data/input/input_dois.csv (one DOI per row, header: DOI)
python src/main.py
```

The pipeline outputs:
- `data/output/csv/MASTER_AUTHOR_TABLE.csv` -- Primary structured output
- `data/output/json/MASTER_AUTHOR_TABLE.json` -- JSON mirror

### Generating Analytical Figures

```bash
python scripts/analytics.py
```

Produces three publication-quality figures in `assets/figures/analytics/`:
1. **Global H-Index Disparity** -- Boxplot of H-index distribution by country (top 25 by author count)
2. **Clinical vs. Technical Impact** -- Violin plot of H-index by LLM-classified research profile
3. **Parachute Research Index** -- Stacked bar chart of authorship position hierarchy by country

### Running the Evaluator

```bash
python scripts/evaluator.py
```

Benchmarks extraction accuracy against raw OpenAlex web data and generates completeness heatmaps and coverage radar charts in `assets/figures/`.

---

## Current Dataset Statistics

| Metric | Value |
|--------|-------|
| DOIs processed | 1,156 |
| Author records | 7,337 |
| Output columns | 35 |
| Active API sources | 4 (OpenAlex, PubMed, Semantic Scholar, ORCID) |
| Enrichment sources | 2 (Genderize.io, Azure GPT-4o) |

---

## License

This project is developed for academic research purposes at the Massachusetts Institute of Technology.

---

## Acknowledgments

- [OpenAlex](https://openalex.org/) for open bibliometric data
- [PubMed / NCBI](https://pubmed.ncbi.nlm.nih.gov/) for biomedical literature metadata
- [Semantic Scholar](https://www.semanticscholar.org/) for citation analysis
- [ORCID](https://orcid.org/) for researcher identity resolution
- [Genderize.io](https://genderize.io/) for name-based gender inference
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service) for deterministic profile classification
