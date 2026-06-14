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

- SharePoint Word document: [Document 1.docx](https://yachaytecheduec-my.sharepoint.com/:w:/g/personal/isaac_gavilanes_yachaytech_edu_ec/IQAFGcgvbx2sRrCU2eU-G8twAcUS48ke__qhpcVP54cteWc?e=eR2jFJ)
- Upload verified on 2026-06-14: title, references, 11 tables, and 5 figures are present.
- Downloaded working-copy SHA256: `BE8BA5B81BEA956250147F84BFB103FE3FD32C2E0400E2036C78C57A51FFDDE5`.
- The anonymous edit permission does not allow renaming the SharePoint file; the owner must rename `Document 1.docx` from an authenticated session.

## Validated artifacts

- Word SHA256: `D549E9320FB0A187A01AC9304E3D8FD62371B39CBF95D851066BEB63379C67C3`
- PDF SHA256: `AF49E5266EED7391F28313E809C7B326514E7305F202A7DEA8C5332D002A8AF3`
- Automated verification: 36 tests passed.
- Scientific consistency validator: passed.
- Visual review: 27 PDF pages inspected.
