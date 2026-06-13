# Country Impact and Mixed-Collaboration Leadership Figures

## Objective

Replace the analytical value of two archived legacy charts with two defensible,
publication-ready figures:

1. country-level OpenAlex H-index distributions;
2. African-country leadership participation in mixed Africa-outside
   collaborations.

The new figures extend the active package as figures `06` and `07`. They do not
restore or overwrite the archived files.

## Figure 06: Country-Level Bibliometric Impact

### Analytical Unit

The unit is one distinct author-country observation:

- identify a person with the established `AUTHOR_KEY`;
- retain one observation per `AUTHOR_KEY` and affiliation country;
- use the maximum available `HINDEX_OA` when repeated rows exist;
- exclude unknown affiliation countries and missing H-index values.

An author affiliated with countries in both regions may contribute one
observation to each country. This is intentional and must be stated in the
figure note.

### Country Selection

Select countries independently within each affiliation region:

- the eight African countries with the largest number of distinct
  author-country observations;
- the eight outside-African countries with the largest number of distinct
  author-country observations;
- require at least 20 observations per country;
- rank countries for inclusion by sample size, not by H-index.

Within the rendered panels, order selected countries by median H-index for
readability.

### Visual Design

Use a two-panel horizontal forest plot:

- African affiliations in teal;
- outside-African affiliations in navy;
- point: median OpenAlex H-index;
- line: interquartile range;
- label: ISO country code and `N`;
- shared x-axis;
- explicit note that the country is publication-time affiliation, not origin or
  nationality.

The title will be:

`OpenAlex H-index distribution by affiliation country`

The output base name will be:

`06_country_hindex_distribution`

### Source Table

Write `data/analysis/country_impact_summary.csv` with:

- `COUNTRY`
- `AFFILIATION_REGION`
- `AUTHORS`
- `HINDEX_MEDIAN`
- `HINDEX_Q1`
- `HINDEX_Q3`
- `SELECTED_FOR_FIGURE`

## Figure 07: African-Country Leadership in Mixed Collaborations

### Analytical Unit

Start with the 499 papers classified as `Mixed Africa + outside`. For each
African affiliation country:

- denominator: distinct mixed-collaboration DOI values where that country has
  at least one affiliated author;
- first-author numerator: distinct denominator papers with at least one
  country-affiliated first author;
- last-author numerator: distinct denominator papers with at least one
  country-affiliated last author;
- corresponding-author numerator: distinct denominator papers with at least
  one country-affiliated corresponding author.

The three percentages are independent and are not expected to sum to 100%.

### Country Selection

Include:

- the ten African countries with the largest mixed-paper denominators;
- minimum denominator of 10 mixed papers;
- order rows by denominator descending.

Selection is based on participation volume, not leadership percentage.

### Visual Design

Use a heatmap:

- rows: African affiliation countries;
- columns: first, last, and corresponding authorship;
- cell color: percentage of that country's mixed papers with the role;
- cell annotation: percentage;
- row label: ISO country code and `N` mixed papers;
- consistent 0-100% color scale;
- include a note that multiple countries or authors may hold a role on the
  same paper.

The title will be:

`African-country leadership participation in mixed collaborations`

The output base name will be:

`07_mixed_collaboration_country_leadership`

The chart must not use the terms `parachute research`, `country of origin`, or
`extractive collaboration`.

### Source Table

Write `data/analysis/mixed_country_leadership.csv` with:

- `COUNTRY`
- `MIXED_PAPERS`
- `FIRST_AUTHOR_PAPERS`
- `FIRST_AUTHOR_PERCENT`
- `LAST_AUTHOR_PAPERS`
- `LAST_AUTHOR_PERCENT`
- `CORRESPONDING_AUTHOR_PAPERS`
- `CORRESPONDING_AUTHOR_PERCENT`
- `SELECTED_FOR_FIGURE`

## Output Integration

Generate:

- briefing PNG files in `assets/figures/briefing/`;
- manuscript PNG and deterministic SVG files in
  `assets/figures/manuscript/`;
- both new source CSV tables in `data/analysis/`.

The existing figures `01` through `05`, validation output, archived legacy
files, and communication drafts remain unchanged.

Update `README.md` so the active package lists seven analytical figures.

## Architecture

Extend the existing analysis modules without introducing a second analytical
path:

- `src/analysis/metrics.py` calculates the two source tables;
- `src/analysis/figures.py` renders only from calculated tables;
- `scripts/run_analysis.py` exports the tables and passes them to the renderer;
- `tests/test_analysis_metrics.py` verifies denominators, deduplication, and
  country selection;
- `tests/test_analysis_outputs.py` verifies the two new CSV, PNG, and SVG
  artifacts and deterministic SVG output.

No new runtime dependency is required.

## Verification Criteria

The implementation is complete when:

- H-index rows are deduplicated by author and country;
- country selection uses observation count rather than outcome values;
- the leadership table uses DOI-level country-specific denominators;
- role percentages are independently calculated and bounded from 0 to 100;
- exactly eight countries per region appear in figure 06 when sufficient data
  exist;
- exactly ten African countries appear in figure 07 when sufficient data
  exist;
- all source values are traceable to exported CSV files;
- PNG files are legible and nonblank;
- SVG files are deterministic and contain no timestamp metadata;
- the complete test suite passes.
