# Scientometric Analysis Tool

A DOI-driven pipeline for author-level scientometric profiling and analysis of
research collaboration, leadership, bibliometric impact, and disciplinary
composition.

The current ML4Africa corpus is fully reconciled:

| Metric | Final value |
|---|---:|
| Unique input DOI values | 1,158 |
| DOI values present in final output | 1,158 |
| Author-paper records | 7,361 |
| Distinct valid OpenAlex author IDs | 5,675 |
| Output columns | 35 |

Author-paper records are not unique researchers.

## Pipeline

The primary workflow processes a closed DOI list through OpenAlex, PubMed,
Semantic Scholar, ORCID, Genderize, and deterministic LLM-based profile
classification. Scopus and Google Scholar integrations exist but were disabled
for the completed run.

```text
input_dois.csv
    -> OpenAlex
    -> PubMed
    -> Semantic Scholar
    -> ORCID
    -> Genderize
    -> profile classification
    -> MASTER_AUTHOR_TABLE.csv + MASTER_AUTHOR_TABLE.json
```

The master table contains paper metadata, authorship position, corresponding
author status, publication-time affiliation, country code, bibliometric
indicators, topics, PubMed metadata, Semantic Scholar metadata, ORCID
employment, name-based gender inference, and inferred research profile.

## Analysis Package

Run the complete audited analysis from the repository root:

```powershell
.\.venv\Scripts\python.exe scripts\run_analysis.py
```

The command:

1. validates CSV/JSON row and schema parity;
2. requires complete input/output DOI reconciliation;
3. exports source tables to `data/analysis/`;
4. generates briefing PNG files;
5. generates manuscript PNG and SVG files;
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
  gender_role_summary.csv
  field_coverage.csv
  doi_reconciliation.csv
```

## Figure Structure

```text
assets/figures/
  briefing/       # Five presentation-ready PNG figures
  manuscript/     # Matching high-resolution PNG and SVG figures
  validation/     # Pipeline validation only
  archive/
    analytics_legacy/
    validation_legacy/
```

The five current analytical figures are:

1. corpus overview and metadata coverage;
2. DOI-level collaboration composition;
3. leadership affiliation in mixed collaborations;
4. OpenAlex H-index distributions by affiliation region;
5. inferred research-profile composition by affiliation region.

## Methodological Boundaries

- African affiliation is based on publication-time affiliation country. It is
  not nationality, ethnicity, residence, or origin.
- Collaboration and leadership percentages use DOI-level denominators.
- Distinct-person estimates use valid OpenAlex author IDs, with normalized
  names only for documented fallback records.
- The impact comparison is descriptive. It does not establish a causal effect
  of geography or affiliation.
- `GENDER` is inferred from names and is not self-identified gender.
- `PROFILE_CLASSIFICATION` is LLM-inferred and requires manual validation.
- Authorship position alone is not evidence of "parachute research."
- Legacy evaluator charts based on five manually checked papers are retained
  for provenance but are not corpus-wide accuracy estimates.

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

This repository supports academic research on global research collaboration
and equity in biomedical and computational science.
