# ML4Africa Scientometric Manuscript

This directory contains the source-backed, journal-neutral manuscript:

**Geographic Patterns of Scientific Leadership and Bibliometric Impact in the ML4Africa Research Corpus**

## Source of record

- Main text: `manuscript/text/manuscript.md`
- Supplement: `manuscript/text/supplement.md`
- Evidence matrix: `manuscript/evidence/evidence_matrix.csv`
- Verified references: `manuscript/references/references_vancouver.md`
- Machine-readable tables: `manuscript/tables/`
- Original and project-derived figures: `manuscript/figures/`

## Rebuild

```powershell
python scripts/manuscript/build_manuscript_assets.py
python scripts/manuscript/build_manuscript_docx.py
python scripts/manuscript/validate_manuscript.py
```

## Interpretive boundaries

- The 1,158 DOI values form a closed corpus supplied by the ML4Africa team.
- Geographic categories denote publication-time affiliation evidence, not nationality or origin.
- First, last, and corresponding authorship are descriptive leadership signals, not complete contribution measures.
- H-index, citations, and works counts are dynamic database-recorded indicators and are not direct measures of research quality.
- Name-inferred gender and LLM-inferred profile classifications are exploratory supplementary outputs.

## Editorial completion required

- Confirm the final author list, order, degrees, and affiliations.
- Confirm the corresponding author.
- Assign CRediT roles.
- Confirm funding and grant numbers.
- Collect competing-interest declarations.
- Confirm named acknowledgements.

## Online working copy

[To be recorded after verified SharePoint upload.]

## Validated artifacts

- Word SHA256: `455D5DE2ECFBD79436EE1CC1D09F1A1404C60986DC7A9C7E99B941873421C768`
- PDF SHA256: `8A5653DD7750F9DD03A229A5EC2F29A2D3A4C1FF98B5C2956387C065A4339373`
- Automated verification: 36 tests passed.
- Scientific consistency validator: passed.
- Visual review: 27 PDF pages inspected.
