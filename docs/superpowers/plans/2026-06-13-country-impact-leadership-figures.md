# Country Impact and Leadership Figures Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two audited country-level figures that replace the analytical purpose of the archived H-index and “parachute research” charts.

**Architecture:** Extend the existing pure-metrics and rendering pipeline. `metrics.py` will produce complete source tables and deterministic figure-selection flags; `figures.py` will render only selected rows; `run_analysis.py` will export both source tables and generate briefing/manuscript artifacts.

**Tech Stack:** Python 3.12, pandas, NumPy, Matplotlib, pytest.

---

### Task 1: Country Impact Metrics

**Files:**
- Modify: `src/analysis/metrics.py`
- Modify: `tests/test_analysis_metrics.py`

- [ ] **Step 1: Write failing tests**

Add tests for:

```python
def test_country_impact_summary_deduplicates_author_country_observations():
    # Repeated papers for the same author-country contribute one observation.
    # The retained H-index is the maximum available value.

def test_country_impact_summary_selects_by_sample_size_within_region():
    # Select the requested top N independently for Africa and outside Africa.
    # A country with a higher median but fewer eligible authors is not selected.
```

- [ ] **Step 2: Verify red**

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_analysis_metrics.py -k country_impact -v
```

Expected: import failure because `country_impact_summary` does not exist.

- [ ] **Step 3: Implement the metric**

Add:

```python
def country_impact_summary(
    df: pd.DataFrame,
    countries_per_region: int = 8,
    min_authors: int = 20,
) -> pd.DataFrame:
    """Summarize deduplicated author-country H-index distributions."""
```

The function must:

1. exclude unknown countries and missing H-index values;
2. deduplicate by `AUTHOR_KEY` and `AFFILIATION_COUNTRY`;
3. aggregate `AUTHORS`, median, Q1, and Q3;
4. mark top countries by `AUTHORS` within each region;
5. return all eligible countries plus `SELECTED_FOR_FIGURE`.

- [ ] **Step 4: Verify green**

Run the two country-impact tests and then all metric tests.

- [ ] **Step 5: Commit**

```powershell
git add src/analysis/metrics.py tests/test_analysis_metrics.py
git commit -m "feat: calculate country-level bibliometric impact"
```

### Task 2: Mixed-Country Leadership Metrics

**Files:**
- Modify: `src/analysis/metrics.py`
- Modify: `tests/test_analysis_metrics.py`

- [ ] **Step 1: Write failing tests**

Add:

```python
def test_mixed_country_leadership_uses_country_specific_doi_denominators():
    # Percentages use distinct mixed papers where the country participates.

def test_mixed_country_leadership_selects_by_mixed_paper_volume():
    # Select top countries by MIXED_PAPERS, not by leadership percentage.
```

- [ ] **Step 2: Verify red**

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_analysis_metrics.py -k mixed_country -v
```

Expected: import failure because `mixed_country_leadership_summary` does not
exist.

- [ ] **Step 3: Implement the metric**

Add:

```python
def mixed_country_leadership_summary(
    df: pd.DataFrame,
    country_limit: int = 10,
    min_mixed_papers: int = 10,
) -> pd.DataFrame:
    """Calculate African-country role participation in mixed papers."""
```

Calculate distinct DOI counts for first, last, and corresponding authorship,
independent percentages, and deterministic `SELECTED_FOR_FIGURE` flags.

- [ ] **Step 4: Verify green**

Run both new tests and the complete metric suite.

- [ ] **Step 5: Commit**

```powershell
git add src/analysis/metrics.py tests/test_analysis_metrics.py
git commit -m "feat: calculate country leadership in mixed collaborations"
```

### Task 3: Render Figures 06 and 07

**Files:**
- Modify: `src/analysis/figures.py`
- Modify: `scripts/run_analysis.py`
- Modify: `tests/test_analysis_outputs.py`

- [ ] **Step 1: Extend the failing output test**

Require:

```text
data/analysis/country_impact_summary.csv
data/analysis/mixed_country_leadership.csv
assets/figures/briefing/06_country_hindex_distribution.png
assets/figures/briefing/07_mixed_collaboration_country_leadership.png
assets/figures/manuscript/06_country_hindex_distribution.png
assets/figures/manuscript/06_country_hindex_distribution.svg
assets/figures/manuscript/07_mixed_collaboration_country_leadership.png
assets/figures/manuscript/07_mixed_collaboration_country_leadership.svg
```

Also include both SVG files in the existing byte-determinism check.

- [ ] **Step 2: Verify red**

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_analysis_outputs.py -v
```

Expected: failure because the new tables and figures are absent.

- [ ] **Step 3: Implement rendering**

Add:

```python
def render_country_hindex_distribution(...): ...
def render_mixed_country_leadership(...): ...
```

Figure 06 is a two-panel forest plot with shared x-axis. Figure 07 is a
0–100% annotated heatmap. Both use `_save` for PNG/SVG output.

- [ ] **Step 4: Integrate runner**

Calculate both tables, export them, and pass them into
`render_all_figures`.

- [ ] **Step 5: Verify green**

Run output tests and then the complete suite.

- [ ] **Step 6: Commit**

```powershell
git add src/analysis/figures.py scripts/run_analysis.py tests/test_analysis_outputs.py
git commit -m "feat: render country impact and leadership figures"
```

### Task 4: Generate and Review Real Outputs

**Files:**
- Create: `data/analysis/country_impact_summary.csv`
- Create: `data/analysis/mixed_country_leadership.csv`
- Create: `assets/figures/briefing/06_country_hindex_distribution.png`
- Create: `assets/figures/briefing/07_mixed_collaboration_country_leadership.png`
- Create: `assets/figures/manuscript/06_country_hindex_distribution.png`
- Create: `assets/figures/manuscript/06_country_hindex_distribution.svg`
- Create: `assets/figures/manuscript/07_mixed_collaboration_country_leadership.png`
- Create: `assets/figures/manuscript/07_mixed_collaboration_country_leadership.svg`
- Modify: `README.md`

- [ ] **Step 1: Run the full analysis**

```powershell
.\.venv\Scripts\python.exe scripts\run_analysis.py
```

- [ ] **Step 2: Validate source tables**

Confirm:

- figure 06 selects 8 African and 8 outside-African countries;
- figure 07 selects 10 African countries;
- all role percentages are between 0 and 100;
- selection order is driven by sample size.

- [ ] **Step 3: Inspect both briefing PNG files**

Check dimensions, nonblank pixels, labels, color scale, footnotes, and absence
of prohibited terminology.

- [ ] **Step 4: Update README**

List seven active analytical figures and add both new source tables.

- [ ] **Step 5: Run final verification**

```powershell
.\.venv\Scripts\python.exe -m pytest -v
git diff --check
git status --short
```

- [ ] **Step 6: Commit**

```powershell
git add README.md data/analysis assets/figures/briefing assets/figures/manuscript
git commit -m "docs: publish country-level scientometric figures"
```
