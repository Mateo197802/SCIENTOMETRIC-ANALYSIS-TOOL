# Architecture and Modules Overview

This tool replicates the logical data extraction sequence from the original V19 n8n visual workflows. Instead of visual nodes, the pipeline is divided into distinct Python scripts (`modules/`) orchestrated sequentially by `main.py`.

## Orchestrator (`main.py`)

This is the heart of the tool. It reads the input DOIs from your CSV, sets up the iteration logic, and sequentially calls each API module. Once all modules add their respective deep metrics and new rows, it ensures the final `MASTER_AUTHOR_TABLE.csv` rigidly adheres to the exact 42 expected output columns.

## Configuration (`config.py`)

Acts as a dynamic parameters file, translating the constants in the `.env` folder into active Python parameters (API Keys and API execution delays to prevent rate-limiting bans).

## 1. OpenAlex Module (`modules/openalex.py`)

**Role:** Foundational layer.
It makes the initial request using the DOI to retrieve paper metadata (Title, Year, Funding) and lists all authors. For every author found, it spins up an internal sub-request to the OpenAlex Authors Endpoint to fetch their deep metrics (`WORKS_COUNT`, `HINDEX`, `I10_INDEX`, `2YR_MEAN_CITEDNESS`).

## 2. PubMed Module (`modules/pubmed.py`)

**Role:** The Ghost-Author Catcher.
Queries NCBI/PubMed E-utilities. It extracts the `MESH_PM` Medical Headings and the exact `PMID_PM`. Fundamentally, it checks if any authors are listed in PubMed that were *not* registered in OpenAlex. If found, it creates "Ghost" fallback rows for those authors.

## 3. Scopus Module (`modules/scopus.py`)

**Role:** Academic Pedigree.
Matches authors found previously against Elsevier’s Scopus database, recovering granular academic data points like `SUBJECT_AREAS` and `CITATIONS`. It inherently features logic to calculate an author's `SENIORITY_SC` based on the delta between the current year and the year of their first publication.

## 4. Semantic Scholar Module (`modules/semantic_scholar.py`)

**Role:** Influence metrics.
Cross-references the paper and authors in Semantic Scholar strictly to recover the highly valuable `INFLUENTIAL_CITATIONS_SS` metric and other alternative impact factor metrics.

## 5. Google Scholar Module (`modules/google_scholar.py`)

**Role:** Broad Interest Extraction.
Uses SerpApi to search the raw text string of the author's Name + their abbreviated Affiliation to pull their `INTERESTS_GS` (Google Scholar Labels), applying intelligent internal caching to prevent duplicate API calls on co-authors.

## 6. Author Compressor utility (`utils/id_compressor.py`)

**Role:** Deduplication node.
A crucial step mapping back and normalizing names. It scrubs weird accents (NFD normalization), trims formatting, and collapses duplicate ghost rows into single super-rows by injecting the best ID hits from across the APIs.

## 7. ORCID Module (`modules/orcid.py`)

**Role:** Concrete Affiliations.
Searches the raw ORCID API for deeper historic employment tracks to provide concrete institutional boundaries in the `ORCID_EMPLOYMENT` field.

## 8. Enrichment Module (`modules/enrichment.py`)

**Role:** The Categorization Engine.
First, predicting Gender relying on high confidence thresholds ($>80\%$) mapped to the `genderize.io` API. Second, simulating the exact n8n LLM Prompt. It constructs a context window incorporating all collected Affiliations, Lifetime Scopus/Scholar interests, and MeSH headings to query Azure OpenAI's GPT-4, forcing a strict structural output to assign the author into one defining Domain (e.g., `BIOINFORMATICS`, `CLINICAL`, etc.).
