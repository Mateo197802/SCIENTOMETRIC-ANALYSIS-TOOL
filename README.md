# Scientometric Analysis Tool

A DOI-driven pipeline for reproducible author-level scientometric profiling,
metadata enrichment, and validation against published bibliometric studies.

## Current Direction

The manuscript strategy has shifted from reporting a new standalone analysis of
a single research corpus to validating the tool itself. The central claim is:

> A closed-corpus, author-level scientometric workflow can reproduce the
> document counts, affiliation patterns, authorship-position signals, country
> distributions, and bibliometric indicators reported in peer-reviewed
> scientometric studies when the same corpus-construction rules are supplied.

The previous ML4Africa DOI corpus is retained only as an internal stress-test
and case-study reference for pipeline scale, reconciliation, and figure design.
It is not the central publication claim.

## Validation Benchmarks

The first validation set uses published studies with reproducible corpus
construction, time windows, inclusion filters, and reported bibliometric
outputs.

| Benchmark | Corpus strategy | Time range | Final count | Validation targets |
|---|---|---:|---:|---|
| Yan & Wang, 2023, SAGE Open, DOI `10.1177/21582440231158562` | Web of Science query for academic-publishing terms | 1970-2020 | 2,217 documents | institutions, countries, productive authors, cited articles |
| Basilio et al., 2022, Electronics, DOI `10.3390/electronics11111720` | WoS + Scopus Boolean query for MCDA methods | 1977-Apr 2022 | 23,494 analyzed records | authors, countries, institutions, citation patterns |
| Baminiwatta & Solangaarachchi, 2021, Mindfulness, DOI `10.1007/s12671-021-01681-x` | WoS topic query for mindfulness | 1966-2021 | 16,581 publications | country collaboration, co-authorship, citation bursts |

Mejia et al. 2021, DOI `10.3389/frma.2021.742311`, is used as
methodological support for bibliometric topic and citation-network analysis, not
as a direct replication target.

## Pipeline

The primary workflow processes a closed DOI list through OpenAlex, PubMed,
Semantic Scholar, ORCID, Genderize, and deterministic LLM-based profile
classification. Scopus and Google Scholar/SerpAPI modules exist for richer
metadata validation and should be enabled only when access is confirmed.

```text
benchmark corpus definition
    -> DOI/query-derived input table
    -> OpenAlex
    -> PubMed
    -> Semantic Scholar
    -> ORCID
    -> Genderize
    -> profile classification
    -> MASTER_AUTHOR_TABLE.csv + MASTER_AUTHOR_TABLE.json
    -> benchmark comparison tables
```

The master table contains paper metadata, authorship position, corresponding
author status, publication-time affiliation, country code, bibliometric
indicators, topics, PubMed metadata, Semantic Scholar metadata, ORCID
employment, name-based gender inference, and inferred research profile.

## Analysis Package

Run the audited analysis package from the repository root:

```powershell
.\.venv\Scripts\python.exe scripts\run_analysis.py
```

The command:

1. validates CSV/JSON row and schema parity;
2. requires complete input/output DOI reconciliation;
3. exports source tables to `data/analysis/`;
4. generates briefing PNG files;
5. generates neutral analysis PNG and SVG files;
6. generates a separate DOI validation figure.

Key machine-readable outputs:

```text
data/analysis/
  analysis_summary.json
  collaboration_summary.csv
  paper_collaboration_types.csv
  mixed_leadership.csv
  impact_observations.csv
  impact_summary.csv
  profile_summary.csv
  country_summary.csv
  country_impact_summary.csv
  mixed_country_leadership.csv
  gender_role_summary.csv
  field_coverage.csv
  doi_reconciliation.csv
```

## Figure Structure

```text
assets/figures/
  briefing/       # Presentation-ready PNG figures
  analysis/       # High-resolution PNG and SVG figures
  validation/     # Pipeline validation only
  archive/
```

## Validation Outputs To Build Next

For each benchmark study, the validation layer should report:

1. source corpus definition, search query, time range, and filters;
2. reproduced document count and DOI/resolution losses;
3. country and institutional distributions compared with the source paper;
4. authorship-position and corresponding-author patterns where available;
5. citation and author-impact indicators from available APIs;
6. mismatch log explaining database coverage, API access, and deduplication
   differences.

## Methodological Boundaries

- Affiliation country is publication-time affiliation, not nationality,
  ethnicity, residence, or origin.
- Collaboration and leadership percentages use DOI-level denominators unless a
  table explicitly states author-level denominators.
- Distinct-person estimates use valid OpenAlex author IDs, with normalized
  names only for documented fallback records.
- Impact comparisons are descriptive and API-dependent; they do not establish
  causal effects.
- `GENDER` is inferred from names and is not self-identified gender.
- `PROFILE_CLASSIFICATION` is LLM-inferred and requires manual validation.
- Authorship position alone is not evidence of extractive or parachute
  research.

## Repository Map

```text
SCIENTOMETRIC-ANALYSIS-TOOL/
  src/
    main.py
    analysis/
      constants.py
      loaders.py
      metrics.py
      figures.py
    modules/
  scripts/
    run_analysis.py
    repair_missing_dois.py
    analytics.py
    evaluator.py
  docs/
    validation/
  data/
    input/
    output/
    analysis/
  assets/
    figures/
  tests/
  requirements.txt
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a local `.env` file for API credentials. It is intentionally excluded
from version control.

Run the extraction pipeline:

```powershell
.\.venv\Scripts\python.exe src\main.py
```

Run tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Data Sources

- [OpenAlex](https://openalex.org/)
- [PubMed / NCBI](https://pubmed.ncbi.nlm.nih.gov/)
- [Semantic Scholar](https://www.semanticscholar.org/)
- [ORCID](https://orcid.org/)
- [Genderize.io](https://genderize.io/)
- Azure OpenAI Service
- Optional validation expansions: Scopus API and Google Scholar via SerpAPI

This repository supports reproducible scientometric validation for global
research collaboration and biomedical data-science studies.
