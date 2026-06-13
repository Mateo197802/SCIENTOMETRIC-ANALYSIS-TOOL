# Legacy Figure Archive

These files are retained for provenance and must not be mixed with the current
scientometric findings in `briefing/` or `manuscript/`.

## `validation_legacy/`

The evaluator figures were produced from a five-paper manual checking sample.
They are useful for debugging the extraction pipeline but are not a
corpus-wide estimate of accuracy or completeness.

Two exact duplicate pairs are preserved:

- `01_accuracy_authors.png` equals `accuracy_authors.png`
  (`SHA256 e5d2f6a353523b86bad0718916e78626e1d9bf3abf8f34df5861a3ddcd6bd4d4`).
- `02_accuracy_percentage.png` equals `completeness_percentage.png`
  (`SHA256 e8993e26d6db8d6f94ff560fe0c6af712532fc33c6e5c1b728b05e062d4d5a92`).

`04_source_coverage_radar.png` is invalid for the completed run because it
visually reports strong coverage for Scopus and Google Scholar even though
those integrations were disabled.

## `analytics_legacy/`

These exploratory charts were superseded because they used author-paper rows
without adequate deduplication or DOI-level denominators. In particular,
`03_parachute_research_index.png` used authorship-position composition as a
proxy for extractive collaboration. That interpretation is not defensible
without additional qualitative and institutional evidence.
