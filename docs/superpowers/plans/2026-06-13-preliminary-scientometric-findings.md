# Preliminary Scientometric Findings Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce an audited ML4Africa scientometric analysis package, repair the two omitted DOI records, reorganize figures, and draft evidence-based group and Leo Celi messages.

**Architecture:** Add a focused `src/analysis` package with pure metric functions and isolated rendering code. A repair script appends only verified missing DOI records to the master outputs, while `scripts/run_analysis.py` validates inputs, exports machine-readable summaries, renders briefing/manuscript/validation figures, and writes communication drafts.

**Tech Stack:** Python 3.12, pandas, NumPy, Matplotlib, Seaborn, pytest, existing pipeline modules, CSV/JSON.

---

### Task 1: Analysis Constants and Data Loading

**Files:**
- Create: `src/analysis/__init__.py`
- Create: `src/analysis/constants.py`
- Create: `src/analysis/loaders.py`
- Test: `tests/test_analysis_loaders.py`

- [ ] **Step 1: Write failing loader tests**

Create tests that assert:

```python
def test_load_master_outputs_requires_csv_json_parity(tmp_path):
    # CSV and JSON with different row counts must raise ValueError.

def test_reconcile_dois_reports_missing_values():
    # 1,158 input DOI values and 1,156 output DOI values return the exact two missing DOI values.
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_analysis_loaders.py -v
```

Expected: import failure because `src.analysis.loaders` does not exist.

- [ ] **Step 3: Implement constants and loaders**

Implement:

```python
AFRICAN_COUNTRY_CODES = frozenset({...})
MISSING_SENTINELS = frozenset({...})
EXPECTED_MASTER_COLUMNS = (...)

def normalize_doi(value: object) -> str: ...
def load_master_outputs(csv_path: Path, json_path: Path) -> pd.DataFrame: ...
def reconcile_dois(input_df: pd.DataFrame, master_df: pd.DataFrame) -> pd.DataFrame: ...
```

`load_master_outputs` must verify equal row counts, equal column sets, and all 35 required columns.

- [ ] **Step 4: Run loader tests**

Expected: all tests pass.

- [ ] **Step 5: Commit**

```powershell
git add src/analysis tests/test_analysis_loaders.py
git commit -m "feat: add audited scientometric data loading"
```

### Task 2: Pure Scientometric Metrics

**Files:**
- Create: `src/analysis/metrics.py`
- Test: `tests/test_analysis_metrics.py`

- [ ] **Step 1: Write failing metric tests**

Cover:

```python
def test_classify_affiliation_region():
    assert classify_affiliation_region("NG") == "Africa"
    assert classify_affiliation_region("US") == "Outside Africa"
    assert classify_affiliation_region("UNKNOWN") == "Unknown"

def test_collaboration_category():
    # Africa + US -> Mixed Africa + outside
    # NG + GH -> Africa-only known affiliations
    # US + GB -> No African affiliation detected

def test_fallback_authors_do_not_collapse():
    # Two PubMed fallback authors with different normalized names remain distinct.

def test_mixed_leadership_counts_papers():
    # Role percentages are paper-based, not row-based.
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_analysis_metrics.py -v
```

- [ ] **Step 3: Implement metric functions**

Implement:

```python
def add_analysis_columns(df: pd.DataFrame) -> pd.DataFrame: ...
def build_author_key(row: pd.Series) -> str: ...
def collaboration_summary(df: pd.DataFrame) -> pd.DataFrame: ...
def mixed_leadership_summary(df: pd.DataFrame) -> pd.DataFrame: ...
def impact_summary(df: pd.DataFrame) -> pd.DataFrame: ...
def profile_summary(df: pd.DataFrame) -> pd.DataFrame: ...
def country_summary(df: pd.DataFrame, min_papers: int = 5) -> pd.DataFrame: ...
def field_coverage(df: pd.DataFrame) -> pd.DataFrame: ...
def analysis_summary(input_df: pd.DataFrame, df: pd.DataFrame) -> dict: ...
```

Use DOI-level denominators for paper metrics and valid OpenAlex IDs plus normalized-name fallback for distinct-person estimates.

- [ ] **Step 4: Run metric tests**

Expected: all tests pass.

- [ ] **Step 5: Commit**

```powershell
git add src/analysis/metrics.py tests/test_analysis_metrics.py
git commit -m "feat: calculate reproducible scientometric metrics"
```

### Task 3: Repair Missing DOI Records

**Files:**
- Create: `scripts/repair_missing_dois.py`
- Modify: `data/output/csv/MASTER_AUTHOR_TABLE.csv`
- Modify: `data/output/json/MASTER_AUTHOR_TABLE.json`
- Test: `tests/test_repair_missing_dois.py`

- [ ] **Step 1: Write repair safety tests**

Assert that the repair merge:

```python
def test_merge_repair_records_rejects_existing_doi(): ...
def test_merge_repair_records_preserves_schema(): ...
def test_merge_repair_records_adds_both_missing_dois(): ...
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_repair_missing_dois.py -v
```

- [ ] **Step 3: Implement repair script**

The script will:

1. read input and master outputs;
2. identify missing DOI values;
3. call the existing OpenAlex, PubMed, Semantic Scholar, ORCID, compressor, and enrichment modules for only those DOI values;
4. merge records only when the DOI is absent;
5. preserve the established 35-column schema;
6. write CSV and JSON atomically after parity checks.

- [ ] **Step 4: Execute repair**

Run:

```powershell
.\.venv\Scripts\python.exe scripts/repair_missing_dois.py
```

Expected:

```text
Missing DOI values before repair: 2
Missing DOI values after repair: 0
```

- [ ] **Step 5: Verify output reconciliation**

Run loader tests plus an exact DOI reconciliation command. Expected: 1,158 input DOI values and 1,158 output DOI values.

- [ ] **Step 6: Commit**

```powershell
git add scripts/repair_missing_dois.py tests/test_repair_missing_dois.py data/output/csv/MASTER_AUTHOR_TABLE.csv data/output/json/MASTER_AUTHOR_TABLE.json
git commit -m "fix: reconcile omitted scientometric DOI records"
```

### Task 4: Figure Rendering and Output Tables

**Files:**
- Create: `src/analysis/figures.py`
- Create: `scripts/run_analysis.py`
- Replace: `scripts/analytics.py`
- Create: `data/analysis/analysis_summary.json`
- Create: `data/analysis/paper_collaboration_types.csv`
- Create: `data/analysis/mixed_leadership.csv`
- Create: `data/analysis/impact_summary.csv`
- Create: `data/analysis/profile_summary.csv`
- Create: `data/analysis/country_summary.csv`
- Create: `data/analysis/field_coverage.csv`
- Create: `data/analysis/doi_reconciliation.csv`
- Test: `tests/test_analysis_outputs.py`

- [ ] **Step 1: Write failing output tests**

Tests assert that the analysis runner produces all eight summary files and that percentages sum to 100 where required.

- [ ] **Step 2: Run tests and verify failure**

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_analysis_outputs.py -v
```

- [ ] **Step 3: Implement figure rendering**

Render:

```text
01_corpus_overview
02_collaboration_composition
03_mixed_collaboration_leadership
04_bibliometric_impact_gap
05_research_profile_composition
```

Use a restrained navy/teal/gold palette, explicit sample sizes, affiliation-based terminology, median/IQR annotations, and footnotes for inferred profile classifications.

- [ ] **Step 4: Implement analysis runner**

The runner writes all source tables before figures and outputs PNG briefing files plus PNG/SVG manuscript files.

- [ ] **Step 5: Run analysis**

Run:

```powershell
.\.venv\Scripts\python.exe scripts/run_analysis.py
```

- [ ] **Step 6: Run output tests**

Expected: all tests pass.

- [ ] **Step 7: Commit**

```powershell
git add src/analysis scripts/analytics.py scripts/run_analysis.py tests/test_analysis_outputs.py data/analysis assets/figures/briefing assets/figures/manuscript assets/figures/validation
git commit -m "feat: generate preliminary scientometric findings package"
```

### Task 5: Reorganize Legacy Figures

**Files:**
- Move: `assets/figures/*.png` to `assets/figures/archive/validation_legacy/`
- Move: `assets/figures/analytics/*.png` to `assets/figures/archive/analytics_legacy/`
- Create: `assets/figures/archive/README.md`
- Modify: `README.md`

- [ ] **Step 1: Record checksums of legacy files**

Verify and document exact duplicate pairs:

```text
01_accuracy_authors.png == accuracy_authors.png
02_accuracy_percentage.png == completeness_percentage.png
```

- [ ] **Step 2: Move legacy files**

Use PowerShell `Move-Item -LiteralPath` only after resolving and verifying all source and target paths remain within `assets/figures`.

- [ ] **Step 3: Write archive README**

Explain that legacy files are retained for provenance, that the radar is invalid for the completed run because it represents inactive sources, and that the five-paper validation sample is not a corpus-wide performance estimate.

- [ ] **Step 4: Update root README**

Replace the old three-figure description with the new directory map, exact corpus statistics, analysis command, and methodological caveats.

- [ ] **Step 5: Commit**

```powershell
git add README.md assets/figures
git commit -m "docs: reorganize scientometric figure assets"
```

### Task 6: Communication Drafts

**Files:**
- Create: `data/analysis/communications.md`

- [ ] **Step 1: Generate factual group message**

The message must contain:

```text
all 1,158 DOI values reconciled
final author-paper record count
two or three strongest descriptive findings
figures ready for discussion
```

- [ ] **Step 2: Generate private Leo message**

The message must:

```text
state exact completion status
ask to coordinate a meeting
name validation, interpretation, and manuscript planning as next steps
avoid causal or endorsement claims
```

- [ ] **Step 3: Cross-check every number**

Each numeric statement must appear in `analysis_summary.json` or one exported summary CSV.

- [ ] **Step 4: Commit**

```powershell
git add data/analysis/communications.md
git commit -m "docs: draft scientometric findings communications"
```

### Task 7: Final Verification

**Files:**
- Verify all modified and generated files.

- [ ] **Step 1: Run complete test suite**

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Expected: all tests pass.

- [ ] **Step 2: Run analysis from a clean output state**

Delete only generated `data/analysis`, `assets/figures/briefing`, `assets/figures/manuscript`, and `assets/figures/validation` contents after verifying target paths, rerun the analysis, and confirm deterministic summaries.

- [ ] **Step 3: Inspect every generated PNG**

Check dimensions, nonblank pixels, clipped labels, readable notes, and consistency with source tables.

- [ ] **Step 4: Validate Git diff**

Run:

```powershell
git diff --check
git status --short
```

- [ ] **Step 5: Commit final verification fixes**

```powershell
git add .
git commit -m "test: verify scientometric analysis package"
```
