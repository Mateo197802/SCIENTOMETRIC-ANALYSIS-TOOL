# A1 n8n Architecture and Node Operations Overview

The Scientometric Analysis Tool V1 operates recursively via a structured data flowchart using interconnected API nodes within the n8n engine. Instead of discrete python files, the workflow relies on visual webhooks and internal programmatic logic (commonly Javascript inside `Code Nodes`) to sequence and aggregate the data.

## 1. Orchestrator Flow

The `Search CSV Folder` node continuously iterates down the input `.csv` reading raw DOIs. A central `Switch Node` reads the database targets assigned from the `DeepSearch.xlsx` file and routes the API traffic into specific database channels.

## 2. Core Operational Architecture

### A. The "Lukas Technique" Code Node (Author Unrolling)

A pivotal functional block right after the primary OpenAlex hit. This **Code Node** forcibly unrolls the multi-layered JSON response extracted from the bibliographic database. Rather than keeping 1 row per publication with nested authors, the code runs a strict loop to expand `1 Document` into `N Author Entities`, embedding metrics like the `First/Middle/Last` rotational position. This relational flattening permits cross-referencing against Google Scholar and ORCID APIs downstream.

### B. Ghost-Author Injection (PubMed Branch)

Following the initial OpenAlex metadata extraction, the pipeline triggers the specific E-utilities PubMed API. Using internal logic checks, it matches the currently listed researchers against those found in PubMed for the same article. Authors listed in PubMed but entirely missing from OpenAlex are appended back into the workflow stream as synthesized "Ghost Authors" preventing fatal structural data drop-offs. Data parameters obtained include precise `PMID_PM`, `MESH_PM` headers, and raw `FUNDING_PM`.

### C. The Scopus and Semantic Scholar Integrations

The workflow diverges into two sequential `HTTP Request` nodes hitting the Elsevier Scopus Graph and the Semantic Scholar Graph API.

* **Scopus:** Cross-references names against Author Profiles extracting deeper quantitative records, primarily generating values for `HINDEX_SC`, total `CITATIONS_SC` count, and academic categorical `SUBJECT_AREAS_SC`. It calculates categorical `SENIORITY_SC` by dynamically subtracting the current year from the date of the author's first publication entry natively in n8n.
* **Semantic Scholar:** Queries for qualitative indicators—specifically the `INFLUENTIAL_CITATIONS_SS` volume count, highlighting profound impact.

### D. Central Global Caching Logic

To sustain operational speed and strictly avoid burning commercial API rate limits (e.g., Azure OpenAI and SerpAPI endpoints), a bespoke **Global Cache Node** operates functionally upstream from the gender inference and Google Scholar nodes.

* **Mechanism:** Every time a unique researcher Name is encountered, it is cached into a persistent array block. If the name recurs (e.g., repeating co-authors across multiple papers), n8n bypasses the HTTP Request node entirely and dynamically injects the saved values to the row output payload, creating rapid, hyper-efficient scraping.

## 3. The Profiling and Fallback Loop Enrichment Engine

### A. Gender Inference (Genderize.io + Regex Filter)

The author’s first name undergoes parsing across the `genderize.io` integration. To conserve downstream LLM queries, n8n relies on a probability cutoff (`>0.80`).
If the predicted gender breaches this rigorous confidence interval, the pipeline bypasses directly to final output.

### B. The Fallback Web-Scraper Node (Regex Pronouns Validation)

When predictions flag authors as `Unknown` or under `<0.8` probability, the n8n pipeline redirects traffic into a targeted **Fallback Loop**. It triggers a Google Search for their public academic profile and uses robust Regular Expression (`Regex`) functions to perform term-frequency ratio calculations on pronouns (`she/her` vs `he/him`). E.g., If a scraped academic bio contains >90% 'she/her', n8n forcefully encodes the probability vector as 'Female'.

### C. Azure OpenAI Profiling Node

For profound scientific background extraction, the pipeline consolidates exactly all parsed arrays across OpenAlex Keywords, Scopus Subjects, Scholar Interests, and ORCID Departments into a tight System Prompt passed into an **Azure OpenAI Node**. Constraining output formats, the GPT engine strictly categorizes the researcher according to fundamental taxonomy segments (e.g. `CLINICAL`, `BIOINFORMATICS`, `BASIC_LIFE_SCIENCES`).

All parsed entities and metrics aggregate dynamically via simple `Set` nodes prior to sequential uploading into a monolithic `MASTER_AUTHOR_TABLE.csv` file structure on Google Drive.
