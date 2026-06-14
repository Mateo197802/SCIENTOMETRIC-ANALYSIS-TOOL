"""Manuscript-specific tables derived from audited analysis data."""

from __future__ import annotations

import pandas as pd

from .metrics import is_missing


def publication_year_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Count distinct DOI values by valid publication year."""
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
        .reset_index(drop=True)
    )


def corpus_characteristics(
    input_df: pd.DataFrame, df: pd.DataFrame
) -> pd.DataFrame:
    """Summarize corpus units without conflating records and researchers."""
    author_ids = df["AUTHOR_ID_OA"].astype(str).str.strip()
    valid = author_ids[
        ~df["AUTHOR_ID_OA"].map(is_missing)
        & ~author_ids.str.upper().isin(
            {"PUBMED_FALLBACK", "SEMANTIC_FALLBACK"}
        )
    ]
    years = pd.to_numeric(df["YEAR"], errors="coerce").dropna()
    rows = [
        ("Input DOI values", int(input_df["DOI"].nunique())),
        ("Output DOI values", int(df["DOI_NORMALIZED"].nunique())),
        ("Author-paper records", int(len(df))),
        ("Distinct OpenAlex author IDs", int(valid.nunique())),
        ("Observed minimum publication year", int(years.min())),
        ("Observed maximum publication year", int(years.max())),
    ]
    return pd.DataFrame(rows, columns=["METRIC", "VALUE"])


def build_corpus_table(
    characteristics: pd.DataFrame, coverage: pd.DataFrame
) -> pd.DataFrame:
    """Combine corpus units and selected metadata-coverage measures."""
    records = [
        {
            "SECTION": "Corpus",
            "MEASURE": row.METRIC,
            "VALUE": int(row.VALUE),
            "DENOMINATOR": pd.NA,
            "PERCENT": pd.NA,
        }
        for row in characteristics.itertuples(index=False)
    ]
    coverage_labels = {
        "PAPER_TITLE": "Paper title populated",
        "YEAR": "Publication year populated",
        "AUTHOR_POS_OA": "Authorship position populated",
        "AFFILIATION_OA": "Affiliation populated",
        "GEO_COUNTRY_OA": "Affiliation country populated",
        "AUTHOR_ID_OA": "OpenAlex author ID populated",
        "ORCID": "ORCID populated",
        "GENDER": "Name-inferred gender populated",
        "PROFILE_CLASSIFICATION": "LLM profile classification populated",
    }
    selected = coverage[coverage["FIELD"].isin(coverage_labels)]
    for row in selected.itertuples(index=False):
        records.append(
            {
                "SECTION": "Metadata coverage",
                "MEASURE": coverage_labels[row.FIELD],
                "VALUE": int(row.POPULATED_RECORDS),
                "DENOMINATOR": int(row.TOTAL_RECORDS),
                "PERCENT": float(row.COVERAGE_PERCENT),
            }
        )
    return pd.DataFrame(
        records,
        columns=["SECTION", "MEASURE", "VALUE", "DENOMINATOR", "PERCENT"],
    )


def build_collaboration_leadership_table(
    collaboration: pd.DataFrame,
    leadership: pd.DataFrame,
    total_papers: int,
) -> pd.DataFrame:
    """Combine DOI-level collaboration and leadership outcomes."""
    records = [
        {
            "OUTCOME": "Collaboration composition",
            "ROLE": "All papers",
            "CATEGORY": row.CATEGORY,
            "PAPERS": int(row.PAPERS),
            "DENOMINATOR": int(total_papers),
            "PERCENT": float(row.PERCENT),
        }
        for row in collaboration.itertuples(index=False)
    ]
    records.extend(
        {
            "OUTCOME": "Leadership in mixed collaborations",
            "ROLE": row.ROLE,
            "CATEGORY": row.LEADERSHIP_REGION,
            "PAPERS": int(row.PAPERS),
            "DENOMINATOR": int(row.MIXED_PAPERS),
            "PERCENT": float(row.PERCENT),
        }
        for row in leadership.itertuples(index=False)
    )
    return pd.DataFrame(records)


def build_impact_table(impact: pd.DataFrame) -> pd.DataFrame:
    """Format regional OpenAlex impact summaries for the manuscript."""
    records = []
    for row in impact.itertuples(index=False):
        records.append(
            {
                "AFFILIATION_REGION": row.AFFILIATION_REGION,
                "AUTHORS": int(row.AUTHORS),
                "HINDEX_MEDIAN": float(row.HINDEX_MEDIAN),
                "HINDEX_IQR": f"{row.HINDEX_Q1:.1f}-{row.HINDEX_Q3:.1f}",
                "CITATIONS_MEDIAN": float(row.CITATIONS_MEDIAN),
                "WORKS_MEDIAN": float(row.WORKS_MEDIAN),
            }
        )
    return pd.DataFrame(records)
