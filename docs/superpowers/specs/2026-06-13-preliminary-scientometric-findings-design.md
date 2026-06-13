# Preliminary Scientometric Findings Design

## Objective

Convert the completed ML4Africa pipeline output into a defensible preliminary
analysis package for:

1. a brief WhatsApp update to the project group;
2. a private message to Leo Celi requesting a next-steps meeting;
3. high-impact preliminary figures for discussion and later manuscript work;
4. a clean separation between scientific findings and pipeline validation.

## Audited Dataset State

- Input: 1,158 unique DOI values.
- Output: 1,156 DOI values with author records.
- Missing from the output:
  - `10.1038/s41467-025-64391-1`
  - `10.1111/exsy.13298`
- Both missing DOI values currently resolve in OpenAlex, so they are classified
  as transient pipeline omissions rather than invalid identifiers.
- Output size: 7,337 author-paper records and 35 columns.
- CSV and JSON outputs contain the same 7,337 records and schema.
- The output contains 5,657 distinct valid OpenAlex author IDs.
- Author-paper records must not be described as unique researchers.

The two omitted DOI values will be repaired before the final figures and
messages are produced. Until then, communications must say that all 1,158 DOI
values were submitted and 1,156 produced records.

## Analytical Unit and Interpretation

The principal unit is the paper, identified by DOI. Author-paper rows are used
to calculate representation and authorship roles. Distinct researchers are
estimated only with valid OpenAlex author IDs, with normalized author names as
a documented fallback for records that came only from PubMed or Semantic
Scholar.

African affiliation is defined from `GEO_COUNTRY_OA` using an explicit ISO
country-code set. This measures affiliation at publication time, not
nationality, ethnicity, residence, or origin.

The analysis will use descriptive language. It will not label a paper as
"parachute research" from authorship position alone. Mixed collaborations with
low African representation or leadership are signals requiring further
investigation, not proof of extractive practice.

Gender findings are exploratory because `GENDER` is name-based inference.
Profile findings are exploratory because `PROFILE_CLASSIFICATION` is
LLM-generated. Both require clear figure notes and cannot be presented as
self-identified attributes.

## Preliminary Finding Set

After repairing the missing DOI values, the analysis will recompute and report:

1. corpus size and metadata coverage;
2. paper collaboration composition:
   - African-affiliation only;
   - mixed African and outside-African affiliations;
   - no African affiliation detected;
3. African-affiliated representation among author positions in mixed papers;
4. first, last, and corresponding authorship distribution in mixed papers;
5. bibliometric impact distributions for African and outside-African
   affiliations, using medians and interquartile ranges rather than means;
6. research-profile composition by affiliation region;
7. country-level participation for countries with sufficient paper counts;
8. exploratory gender distribution by authorship role.

Current figures are provisional. For example, the unrepaired output shows an
African-affiliated median H-index of 5 versus 12 outside Africa, but this value
will be regenerated after the two missing papers are inserted.

## Visual Package

### Briefing

`assets/figures/briefing/` will contain five presentation-ready PNG files:

1. `01_corpus_overview.png`
   - KPI-style summary of input DOI values, DOI values with output, author-paper
     records, distinct OpenAlex author IDs, and field coverage.
2. `02_collaboration_composition.png`
   - Paper counts and percentages for African-only, mixed, and no-African-
     affiliation categories.
3. `03_mixed_collaboration_leadership.png`
   - African versus outside-African first, last, and corresponding authorship
     in mixed collaborations.
4. `04_bibliometric_impact_gap.png`
   - H-index distributions with median and IQR annotations, using a scale that
     does not allow extreme outliers to conceal the central distribution.
5. `05_research_profile_composition.png`
   - Normalized profile composition by affiliation region with classification
     caveats.

### Manuscript

`assets/figures/manuscript/` will contain the same analytical figures in PNG
and SVG formats, with restrained styling, complete labels, sample sizes, and
methodological notes.

### Validation

`assets/figures/validation/` will contain only pipeline-quality figures and a
DOI processing reconciliation figure. Validation results must not be mixed
with substantive scientometric findings.

### Archive

`assets/figures/archive/` will retain superseded files rather than deleting
them. Exact duplicates and invalid or misleading figures, including the source
coverage radar that reports inactive sources as highly complete, will be moved
here with an archive README.

## Analysis Architecture

The existing `scripts/analytics.py` will be replaced by a small analytical
package:

- `src/analysis/constants.py`: country groups, missing-value sentinels, labels,
  and colors.
- `src/analysis/loaders.py`: schema validation and CSV/JSON reconciliation.
- `src/analysis/metrics.py`: pure functions for paper, author-role, profile,
  gender, impact, and coverage metrics.
- `src/analysis/figures.py`: figure rendering only.
- `scripts/run_analysis.py`: command-line orchestration and output manifest.

Machine-readable summaries will be written to `data/analysis/`:

- `analysis_summary.json`
- `paper_collaboration_types.csv`
- `country_summary.csv`
- `field_coverage.csv`
- `doi_reconciliation.csv`

The raw input and existing master outputs will not be overwritten by analysis
code. Repairing the two DOI values will use the established pipeline modules,
then create a reconciled master output only after record and schema checks pass.

## Verification

Automated tests will cover:

- Africa-region classification;
- missing-value handling;
- paper collaboration categorization;
- first, last, and corresponding-author calculations;
- unique-author counting without collapsing fallback records;
- CSV/JSON parity;
- DOI reconciliation;
- deterministic summary generation.

Final verification will require:

- 1,158 input DOI values reconciled;
- CSV and JSON row/schema parity;
- no blank or clipped figures;
- all percentages traceable to exported summary tables;
- captions that distinguish affiliation from nationality;
- no use of the invalid legacy radar or the five-paper validation sample as a
  corpus-wide performance claim.

## Communication Outputs

The group message will be brief, factual, and framed as preliminary. It will
report the completed corpus, the major descriptive signals, and that a visual
analysis package is ready for discussion.

The private message to Leo will state the exact processing status, mention that
the complete analysis package is being consolidated, and request a meeting to
agree on validation, interpretation, and manuscript next steps. It will not
claim institutional endorsement or causal conclusions.
