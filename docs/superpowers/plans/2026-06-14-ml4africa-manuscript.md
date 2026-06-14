# ML4Africa Scientometric Manuscript Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce, validate, and upload a complete journal-neutral Word manuscript titled *Geographic Patterns of Scientific Leadership and Bibliometric Impact in the ML4Africa Research Corpus*.

**Architecture:** Extend the audited analysis package with manuscript-specific summary tables and an original pipeline figure, then build a source-backed academic manuscript from Markdown and structured citation files. A deterministic Python builder will generate the `.docx`; LibreOffice/PDF rendering and page-image inspection will validate layout before Browser uploads the final file to Word Online.

**Tech Stack:** Python 3.12, pandas, matplotlib, python-docx, pypdf/pdfplumber, Crossref/PubMed/publisher records, Microsoft Word `.docx`, LibreOffice or Word PDF rendering, Browser plugin, Git.

---

## File Structure

```text
manuscript/
  README.md
  evidence/
    evidence_matrix.csv
    search_log.md
  references/
    references.bib
    references_vancouver.md
  text/
    manuscript.md
    supplement.md
  tables/
    table_1_corpus_characteristics.csv
    table_2_collaboration_leadership.csv
    table_3_bibliometric_impact.csv
    supplementary_variable_dictionary.csv
    supplementary_country_participation.csv
    supplementary_country_leadership.csv
  figures/
    figure_1_pipeline.png
    figure_1_pipeline.svg
    figure_2_corpus_collaboration.png
    figure_3_mixed_leadership.png
    figure_4_regional_hindex.png
    figure_5_country_hindex.png
scripts/manuscript/
  build_manuscript_assets.py
  build_manuscript_docx.py
  validate_manuscript.py
src/analysis/
  manuscript_metrics.py
tests/
  test_manuscript_metrics.py
  test_manuscript_outputs.py
output/doc/
  ML4Africa_scientometric_manuscript.docx
output/pdf/
  ML4Africa_scientometric_manuscript.pdf
```

`manuscript/text/` is the human-readable source of record. Numerical tables are
generated from committed analysis outputs. The Word builder consumes the text,
tables, references, and original figure assets without recomputing scientific
results.

### Task 1: Freeze Manuscript-Specific Metrics

**Files:**
- Create: `src/analysis/manuscript_metrics.py`
- Create: `tests/test_manuscript_metrics.py`
- Create: `scripts/manuscript/build_manuscript_assets.py`
- Create: `manuscript/tables/table_1_corpus_characteristics.csv`
- Create: `manuscript/tables/table_2_collaboration_leadership.csv`
- Create: `manuscript/tables/table_3_bibliometric_impact.csv`

- [ ] **Step 1: Write failing tests for publication years and table traceability**

```python
import pandas as pd

from src.analysis.manuscript_metrics import (
    corpus_characteristics,
    publication_year_summary,
)


def test_publication_year_summary_uses_distinct_dois():
    data = pd.DataFrame(
        {
            "DOI_NORMALIZED": ["a", "a", "b", "c"],
            "YEAR": [2020, 2020, 2021, 2021],
        }
    )
    result = publication_year_summary(data)
    assert result.to_dict("records") == [
        {"YEAR": 2020, "PAPERS": 1},
        {"YEAR": 2021, "PAPERS": 2},
    ]


def test_corpus_characteristics_reports_units_without_conflation():
    input_df = pd.DataFrame({"DOI": ["a", "b"]})
    data = pd.DataFrame(
        {
            "DOI_NORMALIZED": ["a", "a", "b"],
            "AUTHOR_ID_OA": ["A1", "A2", "A1"],
            "AUTHOR_KEY": ["oa:A1", "oa:A2", "oa:A1"],
            "AFFILIATION_REGION": ["Africa", "Outside Africa", "Africa"],
        }
    )
    result = corpus_characteristics(input_df, data)
    values = dict(zip(result["METRIC"], result["VALUE"]))
    assert values["Input DOI values"] == 2
    assert values["Author-paper records"] == 3
    assert values["Distinct OpenAlex author IDs"] == 2
```

- [ ] **Step 2: Run the tests and verify the expected import failure**

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_manuscript_metrics.py -v
```

Expected: collection fails because `src.analysis.manuscript_metrics` does not
exist.

- [ ] **Step 3: Implement the manuscript metrics**

```python
"""Manuscript-specific tables derived from audited analysis data."""

from __future__ import annotations

import pandas as pd

from .metrics import is_missing


def publication_year_summary(df: pd.DataFrame) -> pd.DataFrame:
    papers = (
        df.loc[:, ["DOI_NORMALIZED", "YEAR"]]
        .drop_duplicates("DOI_NORMALIZED")
        .assign(YEAR=lambda value: pd.to_numeric(value["YEAR"], errors="coerce"))
        .dropna(subset=["YEAR"])
    )
    papers["YEAR"] = papers["YEAR"].astype(int)
    return (
        papers.groupby("YEAR")
        .size()
        .rename("PAPERS")
        .reset_index()
        .sort_values("YEAR")
    )


def corpus_characteristics(
    input_df: pd.DataFrame, df: pd.DataFrame
) -> pd.DataFrame:
    author_ids = df["AUTHOR_ID_OA"].astype(str).str.strip()
    valid = author_ids[
        ~df["AUTHOR_ID_OA"].map(is_missing)
        & ~author_ids.str.upper().isin(
            {"PUBMED_FALLBACK", "SEMANTIC_FALLBACK"}
        )
    ]
    rows = [
        ("Input DOI values", int(input_df["DOI"].nunique())),
        ("Output DOI values", int(df["DOI_NORMALIZED"].nunique())),
        ("Author-paper records", int(len(df))),
        ("Distinct OpenAlex author IDs", int(valid.nunique())),
        ("Observed minimum publication year", int(df["YEAR"].min())),
        ("Observed maximum publication year", int(df["YEAR"].max())),
    ]
    return pd.DataFrame(rows, columns=["METRIC", "VALUE"])
```

- [ ] **Step 4: Add a deterministic asset builder**

Create `scripts/manuscript/build_manuscript_assets.py` with repository-root
path resolution, validated master-data loading, calls to existing analysis
functions, and CSV writes using:

```python
table.to_csv(
    output_path,
    index=False,
    lineterminator="\n",
    float_format="%.1f",
)
```

Build:

- Table 1 from `corpus_characteristics`, selected field-coverage rows, and
  publication-year summary metadata.
- Table 2 from `collaboration_summary.csv` and `mixed_leadership.csv`.
- Table 3 from `impact_summary.csv`.

- [ ] **Step 5: Run focused and full tests**

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_manuscript_metrics.py -v
.\.venv\Scripts\python.exe -m pytest -v
```

Expected: manuscript tests pass and the existing 25 tests remain green.

- [ ] **Step 6: Generate and inspect manuscript tables**

Run:

```powershell
.\.venv\Scripts\python.exe scripts\manuscript\build_manuscript_assets.py
```

Expected: the three main table CSV files are created with `1,158`, `7,361`,
`5,675`, publication years `1974-2025`, and the committed leadership/impact
values.

- [ ] **Step 7: Commit the metric layer**

```powershell
git add src/analysis/manuscript_metrics.py tests/test_manuscript_metrics.py scripts/manuscript/build_manuscript_assets.py manuscript/tables
git commit -m "feat: generate manuscript summary tables"
```

### Task 2: Build the Literature Evidence Base

**Files:**
- Create: `manuscript/evidence/evidence_matrix.csv`
- Create: `manuscript/evidence/search_log.md`
- Create: `manuscript/references/references.bib`
- Create: `manuscript/references/references_vancouver.md`

- [ ] **Step 1: Define the evidence matrix schema**

Create a UTF-8 CSV with these columns:

```text
CITATION_KEY,TITLE,YEAR,JOURNAL,DOI_OR_URL,EVIDENCE_TYPE,
MANUSCRIPT_SECTION,CLAIM_SUPPORTED,POPULATION_OR_SCOPE,
DESIGN,KEY_FINDING,LIMITATION,VERIFICATION_SOURCE,VERIFIED_DATE
```

- [ ] **Step 2: Execute focused literature searches**

Search primary and methodological literature in these lanes:

1. African participation and leadership in global-health authorship.
2. First, last, and corresponding authorship as leadership indicators.
3. Geographic and citation inequities in biomedical research.
4. AI/ML for health research capacity and representation in Africa.
5. Bibliometric data-source methods: OpenAlex, PubMed, Semantic Scholar, ORCID.
6. Name-based gender inference validity and limitations.
7. Reporting guidance for bibliometric and observational research.

Use primary papers and official documentation. Record the exact query, source,
date, inclusion rationale, and excluded near-duplicates in `search_log.md`.

- [ ] **Step 3: Verify every retained reference**

For each retained citation, confirm title, authors, year, journal, volume,
pages/article number, and DOI against at least one authoritative record:

- publisher landing page;
- PubMed;
- Crossref;
- official database documentation.

Do not retain citations that cannot be resolved reliably.

- [ ] **Step 4: Populate the evidence matrix**

Every contextual claim planned for the Introduction or Discussion must have a
row. `CLAIM_SUPPORTED` must be a bounded paraphrase, not a copied abstract
sentence. Record design and scope limitations so association is not converted
into causation.

- [ ] **Step 5: Build Vancouver references**

Create `references.bib` as structured reference storage and
`references_vancouver.md` as the exact numbered rendering used by the Word
builder. Include live `https://doi.org/...` links when available.

- [ ] **Step 6: Validate the bibliography**

Run a script or structured check that asserts:

```python
assert evidence["CITATION_KEY"].is_unique
assert evidence["DOI_OR_URL"].str.startswith(("https://", "http://")).all()
assert evidence["VERIFICATION_SOURCE"].ne("").all()
assert evidence["VERIFIED_DATE"].ne("").all()
```

- [ ] **Step 7: Commit the evidence base**

```powershell
git add manuscript/evidence manuscript/references
git commit -m "docs: build ML4Africa manuscript evidence base"
```

### Task 3: Create the Original Pipeline Figure and Composite Figures

**Files:**
- Modify: `scripts/manuscript/build_manuscript_assets.py`
- Create: `manuscript/figures/figure_1_pipeline.png`
- Create: `manuscript/figures/figure_1_pipeline.svg`
- Create: `manuscript/figures/figure_2_corpus_collaboration.png`
- Create: `manuscript/figures/figure_3_mixed_leadership.png`
- Create: `manuscript/figures/figure_4_regional_hindex.png`
- Create: `manuscript/figures/figure_5_country_hindex.png`
- Create: `tests/test_manuscript_outputs.py`

- [ ] **Step 1: Write failing output tests**

```python
from pathlib import Path
from PIL import Image


def test_manuscript_figures_exist_and_are_readable(tmp_path):
    expected = [
        "figure_1_pipeline.png",
        "figure_2_corpus_collaboration.png",
        "figure_3_mixed_leadership.png",
        "figure_4_regional_hindex.png",
        "figure_5_country_hindex.png",
    ]
    for filename in expected:
        path = tmp_path / filename
        assert path.exists()
        with Image.open(path) as image:
            assert image.width >= 1600
            assert image.height >= 900
```

- [ ] **Step 2: Run the output test and verify failure**

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_manuscript_outputs.py -v
```

Expected: failure because the manuscript figures have not been generated.

- [ ] **Step 3: Implement Figure 1**

Render an original vector workflow diagram with these labeled stages:

```text
ML4Africa closed DOI corpus (n=1,158)
    |
OpenAlex -> PubMed -> Semantic Scholar
    |
Identifier reconciliation and within-paper consolidation
    |
ORCID + Genderize + Azure OpenAI enrichment
    |
35-field author-paper table
(7,361 records; 5,675 distinct OpenAlex author IDs)
    |
CSV/JSON parity + complete DOI reconciliation
    |
Collaboration | Leadership | Bibliometric impact
```

Mark Scopus and Google Scholar in a side note as implemented but disabled for
the completed run. Use teal for African-affiliation analysis, navy for
outside-African analysis, and neutral gray for validation stages.

- [ ] **Step 4: Build composite Figures 2-5**

Reuse the committed manuscript PNGs as source panels:

- Figure 2: `01_corpus_overview.png` + `02_collaboration_composition.png`.
- Figure 3: `03_mixed_collaboration_leadership.png` +
  `07_mixed_collaboration_country_leadership.png`.
- Figure 4: `04_bibliometric_impact_gap.png`.
- Figure 5: `06_country_hindex_distribution.png`.

Do not copy figures from external papers. Add panel labels only where a
composite contains multiple panels.

- [ ] **Step 5: Render and test figures**

Run:

```powershell
.\.venv\Scripts\python.exe scripts\manuscript\build_manuscript_assets.py
.\.venv\Scripts\python.exe -m pytest tests\test_manuscript_outputs.py -v
```

Expected: all figure files exist, SVG output has no timestamp metadata, and
PNG dimensions satisfy the test.

- [ ] **Step 6: Visually inspect all five figures**

Use image inspection at original resolution. Confirm:

- no clipped labels;
- readable legends and denominators;
- consistent title capitalization;
- no unsupported terms such as `parachute research`;
- no source-image scaling artifacts.

- [ ] **Step 7: Commit the figure package**

```powershell
git add scripts/manuscript/build_manuscript_assets.py tests/test_manuscript_outputs.py manuscript/figures
git commit -m "feat: create ML4Africa manuscript figures"
```

### Task 4: Write the Main Manuscript Source

**Files:**
- Create: `manuscript/text/manuscript.md`
- Create: `manuscript/README.md`

- [ ] **Step 1: Write the title page and structured abstract**

Use the approved title and headings:

```markdown
# Geographic Patterns of Scientific Leadership and Bibliometric Impact in the ML4Africa Research Corpus

## Abstract
### Background
### Methods
### Results
### Conclusions
```

Include only audited values. Keep the abstract near 300 words and distinguish
papers, author-paper records, and distinct authors.

- [ ] **Step 2: Write the Introduction**

Use 5-7 paragraphs:

1. ML4H opportunity and local scientific capacity.
2. Global concentration of resources and bibliometric visibility.
3. Authorship leadership as an imperfect proxy.
4. Evidence specific to African research partnerships.
5. Gap in author-level mapping for the ML4Africa corpus.
6. Study objective and research questions.

Every external factual claim receives a numbered citation from the evidence
matrix.

- [ ] **Step 3: Write the complete Methods**

Include all approved subsections:

```markdown
## Methods
### Study design
### Corpus and unit of analysis
### Scientometric Analysis Tool
### Data-source APIs and extracted variables
### Author reconciliation and deduplication
### Geographic classification
### Collaboration and leadership outcomes
### Bibliometric outcomes
### Supplementary automated classifications
### Data validation and reproducibility
### Statistical analysis
### Ethics
```

State that Scopus and Google Scholar were disabled. Report the Genderize
threshold `>=0.80`, Azure OpenAI temperature `0`, and the precise identity-key
logic. Explain that the first OpenAlex institution/country evidence was used.

- [ ] **Step 4: Write Results from machine-readable tables**

Use the fixed order:

1. Corpus characteristics.
2. Collaboration composition.
3. Mixed-collaboration leadership.
4. Country leadership.
5. Regional impact.
6. Country impact.

Required values include:

- 1,158 DOI values;
- 7,361 author-paper records;
- 5,675 distinct OpenAlex author IDs;
- 533 Africa-only papers;
- 499 mixed papers;
- 93 with no African affiliation detected;
- 33 unknown-only papers;
- first authorship: 40.9% Africa-only and 54.3% outside-Africa-only;
- last authorship: 49.9% Africa-only and 46.5% outside-Africa-only;
- corresponding authorship: 37.9% Africa-only, 51.9%
  outside-Africa-only, and 6.8% both regions;
- median H-index 5 for African and 13 for outside-African affiliation strata.

- [ ] **Step 5: Write Discussion and Conclusion**

Structure:

```markdown
## Discussion
### Principal findings
### Interpretation in relation to prior literature
### Implications for ML4Africa
### Strengths and limitations
### Future research

## Conclusions
```

Do not label papers or countries as extractive. Discuss authorship patterns as
signals requiring contextual interpretation. Explain that bibliometric
differences can reflect career stage, field, database coverage, language,
resources, and citation-network effects.

- [ ] **Step 6: Add end matter**

Include explicit fields for team confirmation:

```markdown
## Author contributions
[Editorial completion required: confirm author list and CRediT roles.]

## Funding
[Editorial completion required: confirm project funding.]

## Competing interests
[Editorial completion required: collect declarations from all authors.]
```

Data/code availability must point to the GitHub repository without promising
release of data that the team has not authorized.

- [ ] **Step 7: Add figure legends and table callouts**

Every figure legend defines the unit, denominator, abbreviations, and geographic
meaning. Insert figure/table callouts after first mention in the working draft.

- [ ] **Step 8: Run manuscript text validation**

Search for prohibited or unresolved language:

```powershell
rg -n "TBD|TODO|all African|systematic review|nationality|country of origin|parachute research index|caused by|proves that" manuscript\text\manuscript.md
```

Expected: only approved editorial-completion markers and a cautious literature
discussion of terminology, if retained.

- [ ] **Step 9: Commit the main manuscript**

```powershell
git add manuscript/text/manuscript.md manuscript/README.md
git commit -m "docs: draft ML4Africa scientometric manuscript"
```

### Task 5: Write the Supplement and Variable Dictionary

**Files:**
- Create: `manuscript/text/supplement.md`
- Create: `manuscript/tables/supplementary_variable_dictionary.csv`
- Create: `manuscript/tables/supplementary_country_participation.csv`
- Create: `manuscript/tables/supplementary_country_leadership.csv`

- [ ] **Step 1: Generate the 35-field variable dictionary**

For every output column record:

```text
VARIABLE,SOURCE,LEVEL,DEFINITION,TYPE,MISSING_SENTINELS,
PRIMARY_OR_SUPPLEMENTARY,ANALYTICAL_USE,LIMITATION
```

Verify exactly 35 master-table rows.

- [ ] **Step 2: Export full country tables**

Copy deterministic source data from:

- `data/analysis/country_summary.csv`;
- `data/analysis/mixed_country_leadership.csv`;
- `data/analysis/country_impact_summary.csv`.

Do not truncate the supplement to only figure-selected countries.

- [ ] **Step 3: Write supplementary methods**

Document:

- Genderize country-conditioned first-name inference and threshold;
- cache behavior;
- consortium/institutional-name exclusion regex;
- Azure OpenAI taxonomy and temperature;
- missing-value handling;
- field coverage;
- DOI reconciliation;
- software environment and test suite.

- [ ] **Step 4: Write supplementary results**

Report name-inferred gender and LLM-profile summaries as exploratory. Use the
terms `name-inferred` and `LLM-inferred` in every heading and legend.

- [ ] **Step 5: Validate supplementary boundaries**

Run:

```powershell
rg -n "self-identified|validated gender|biological sex|ground truth|expert-validated" manuscript\text\supplement.md
```

Expected: no unsupported validation claims.

- [ ] **Step 6: Commit the supplement**

```powershell
git add manuscript/text/supplement.md manuscript/tables
git commit -m "docs: add ML4Africa manuscript supplement"
```

### Task 6: Build the Word Manuscript

**Files:**
- Create: `scripts/manuscript/build_manuscript_docx.py`
- Create: `output/doc/ML4Africa_scientometric_manuscript.docx`
- Modify: `requirements.txt`

- [ ] **Step 1: Add document dependencies**

Append:

```text
python-docx>=1.2.0
pypdf>=6.0.0
pdfplumber>=0.11.0
```

- [ ] **Step 2: Implement document styles**

In `build_manuscript_docx.py`, configure:

- US Letter;
- 1-inch margins;
- Times New Roman 11 pt body;
- Arial 14/12 pt headings;
- 1.15 line spacing;
- 6 pt paragraph spacing;
- page-number footer;
- clickable DOI/GitHub hyperlinks;
- editable Word tables;
- image width constrained to the text area;
- page breaks before References and Supplement.

- [ ] **Step 3: Parse manuscript structure**

Implement explicit Markdown parsing for:

- headings;
- paragraphs;
- numbered references;
- figure placeholders;
- table placeholders;
- editorial completion notices.

Reject unknown placeholder syntax with a `ValueError` rather than silently
omitting content.

- [ ] **Step 4: Insert figures and tables**

Map:

```python
FIGURES = {
    "Figure 1": "manuscript/figures/figure_1_pipeline.png",
    "Figure 2": "manuscript/figures/figure_2_corpus_collaboration.png",
    "Figure 3": "manuscript/figures/figure_3_mixed_leadership.png",
    "Figure 4": "manuscript/figures/figure_4_regional_hindex.png",
    "Figure 5": "manuscript/figures/figure_5_country_hindex.png",
}
```

Load the three main CSV tables into editable Word tables with repeated header
rows.

- [ ] **Step 5: Generate the `.docx`**

Run:

```powershell
.\.venv\Scripts\python.exe scripts\manuscript\build_manuscript_docx.py
```

Expected: `output/doc/ML4Africa_scientometric_manuscript.docx`.

- [ ] **Step 6: Inspect the document structurally**

Use `python-docx` to assert:

```python
assert approved_title in document.paragraphs[0].text
assert len(document.inline_shapes) == 5
assert len(document.tables) >= 3
assert "References" in paragraph_text
assert "Supplementary Material" in paragraph_text
```

- [ ] **Step 7: Commit the Word builder and document**

```powershell
git add requirements.txt scripts/manuscript/build_manuscript_docx.py output/doc/ML4Africa_scientometric_manuscript.docx
git commit -m "feat: build ML4Africa Word manuscript"
```

### Task 7: Validate Scientific and Numerical Consistency

**Files:**
- Create: `scripts/manuscript/validate_manuscript.py`

- [ ] **Step 1: Implement source-to-text assertions**

Load committed CSV/JSON values and assert their formatted forms appear in
`manuscript.md`. Check all primary abstract and Results values.

- [ ] **Step 2: Implement terminology checks**

Fail on:

```python
PROHIBITED = [
    "all African machine learning for health research",
    "systematic review of the ML4Africa corpus",
    "country of origin",
    "nationality was defined",
    "parachute research index",
]
```

Allow `parachute research` only in a citation-supported discussion sentence
that states authorship alone is insufficient for classification.

- [ ] **Step 3: Implement citation checks**

Assert:

- citations are sequential;
- every citation number has a reference;
- every reference is cited;
- every external Introduction/Discussion paragraph contains at least one
  citation where it makes factual literature claims;
- no raw tool tokens or source placeholders remain.

- [ ] **Step 4: Run the validator**

Run:

```powershell
.\.venv\Scripts\python.exe scripts\manuscript\validate_manuscript.py
```

Expected: `Manuscript validation passed`.

- [ ] **Step 5: Run all tests**

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
git diff --check
```

Expected: all tests pass and no whitespace errors.

- [ ] **Step 6: Commit validation**

```powershell
git add scripts/manuscript/validate_manuscript.py
git commit -m "test: validate manuscript scientific consistency"
```

### Task 8: Render and Visually Review Every Page

**Files:**
- Create: `output/pdf/ML4Africa_scientometric_manuscript.pdf`
- Temporary: `tmp/docs/manuscript_pages/*.png`

- [ ] **Step 1: Detect the available renderer**

Check for Microsoft Word automation, LibreOffice `soffice`, or the bundled DOCX
render helper. Prefer LibreOffice headless conversion when available.

- [ ] **Step 2: Convert DOCX to PDF**

Run the available equivalent of:

```powershell
soffice --headless --convert-to pdf --outdir output\pdf output\doc\ML4Africa_scientometric_manuscript.docx
```

Expected: a readable PDF with nonzero page count.

- [ ] **Step 3: Render PDF pages to PNG**

Use Poppler or `pypdfium2` to create one PNG per page under
`tmp/docs/manuscript_pages/`.

- [ ] **Step 4: Inspect every page**

Check at 100% scale:

- title and author-completion field;
- abstract fit and section hierarchy;
- table width and repeated headers;
- figure resolution and legends;
- page breaks;
- reference hanging indents and hyperlinks;
- no orphan headings;
- no clipped or overlapping text;
- supplement numbering.

- [ ] **Step 5: Correct and rerender**

Modify only `build_manuscript_docx.py` or source Markdown, regenerate the DOCX,
and repeat PDF/PNG inspection until zero defects remain.

- [ ] **Step 6: Validate PDF text**

Extract PDF text and confirm the approved title, `References`, final reference,
and final supplement heading are present.

- [ ] **Step 7: Commit the validated render**

```powershell
git add output/doc/ML4Africa_scientometric_manuscript.docx output/pdf/ML4Africa_scientometric_manuscript.pdf
git commit -m "docs: publish validated ML4Africa manuscript"
```

### Task 9: Upload to Word Online

**Files:**
- Upload source: `output/doc/ML4Africa_scientometric_manuscript.docx`
- Destination: user-provided Yachay Tech SharePoint Word URL.

- [ ] **Step 1: Open the shared Word Online link**

Use Browser and verify:

- Yachay Tech authentication is active;
- the shared file is accessible;
- whether the link targets an existing manuscript or an empty document.

- [ ] **Step 2: Choose the non-destructive upload path**

If the target is an empty/template document, use Word Online's replace/upload
workflow. If it contains unrelated content, upload the final DOCX as a separate
file in the same SharePoint location and open it. Do not delete existing files
or alter sharing permissions.

- [ ] **Step 3: Confirm before upload if the UI creates an external side effect**

At action time, identify the exact file, destination account/site, and whether
the operation replaces an existing file. The user's request authorizes upload
to the supplied location, but any ambiguous replacement must be resolved
before committing the destructive variant.

- [ ] **Step 4: Upload the final DOCX**

Upload only:

```text
output/doc/ML4Africa_scientometric_manuscript.docx
```

- [ ] **Step 5: Verify Word Online rendering**

Confirm the authoritative signals:

- approved title is visible;
- the document reaches the Supplementary Material section;
- figures and tables load;
- Word reports a saved/synchronized state;
- no conversion or upload error is shown.

- [ ] **Step 6: Record the final Word Online URL**

Add the verified link to `manuscript/README.md` under `Online working copy`.
Do not store authentication tokens or private session data.

- [ ] **Step 7: Commit the delivery record**

```powershell
git add manuscript/README.md
git commit -m "docs: record Word Online manuscript delivery"
```

### Task 10: Final Repository Verification and GitHub Synchronization

**Files:**
- Verify all files created in Tasks 1-9.

- [ ] **Step 1: Run final tests and validation**

```powershell
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe scripts\manuscript\validate_manuscript.py
git diff --check
git status --short
```

Expected: all tests and validation pass; only intentional tracked outputs are
present.

- [ ] **Step 2: Confirm artifact checksums**

```powershell
Get-FileHash output\doc\ML4Africa_scientometric_manuscript.docx -Algorithm SHA256
Get-FileHash output\pdf\ML4Africa_scientometric_manuscript.pdf -Algorithm SHA256
```

Record hashes in `manuscript/README.md`.

- [ ] **Step 3: Push `master`**

```powershell
git push origin master
```

- [ ] **Step 4: Verify local/remote parity**

```powershell
git rev-parse master
git ls-remote origin refs/heads/master
```

Expected: identical commit hashes.

- [ ] **Step 5: Report final delivery**

Report:

- local Word path;
- local PDF path;
- Word Online URL;
- test count;
- validation result;
- final commit hash;
- any editorial completion fields still requiring consortium input.
