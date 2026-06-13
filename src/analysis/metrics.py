"""Pure metric calculations for the scientometric analysis."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable

import numpy as np
import pandas as pd

from .constants import AFRICAN_COUNTRY_CODES, MISSING_SENTINELS
from .loaders import normalize_doi

COLLABORATION_ORDER = (
    "Africa-only known affiliations",
    "Mixed Africa + outside",
    "No African affiliation detected",
    "Unknown affiliations only",
)
LEADERSHIP_REGION_ORDER = (
    "Africa only",
    "Outside Africa only",
    "Both regions",
    "Unknown only",
)
ROLE_ORDER = ("First author", "Last author", "Corresponding author")


def _normalized_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def is_missing(value: object) -> bool:
    """Return whether a value is absent or is an established pipeline sentinel."""
    normalized = _normalized_text(value).upper()
    return not normalized or normalized in MISSING_SENTINELS


def classify_affiliation_region(country_code: object) -> str:
    """Classify an affiliation country code without inferring nationality."""
    code = _normalized_text(country_code).upper()
    if not code or code in MISSING_SENTINELS:
        return "Unknown"
    if code in AFRICAN_COUNTRY_CODES:
        return "Africa"
    return "Outside Africa"


def normalize_person_name(value: object) -> str:
    """Normalize a display name for fallback identity keys."""
    text = unicodedata.normalize("NFD", _normalized_text(value))
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return re.sub(r"[^a-z]", "", text.lower())


def build_author_key(row: pd.Series) -> str:
    """Build an identity key without collapsing all source-fallback authors."""
    author_id = _normalized_text(row.get("AUTHOR_ID_OA"))
    invalid_ids = MISSING_SENTINELS | {"PUBMED_FALLBACK", "SEMANTIC_FALLBACK"}
    if author_id and author_id.upper() not in invalid_ids:
        return f"oa:{author_id}"

    normalized_name = normalize_person_name(row.get("AUTHOR_NAME"))
    return f"name:{normalized_name}"


def _to_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return _normalized_text(value).lower() in {"true", "1", "yes"}


def add_analysis_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with normalized fields used by all downstream metrics."""
    result = df.copy()
    result["DOI_NORMALIZED"] = result["DOI"].map(normalize_doi)
    result["AFFILIATION_COUNTRY"] = (
        result["GEO_COUNTRY_OA"].fillna("").astype(str).str.strip().str.upper()
    )
    result["AFFILIATION_REGION"] = result["GEO_COUNTRY_OA"].map(
        classify_affiliation_region
    )
    result["AUTHOR_POSITION"] = (
        result["AUTHOR_POS_OA"].fillna("Unknown").astype(str).str.strip().str.lower()
    )
    result["IS_CORRESPONDING"] = result["IS_CORRESPONDING_OA"].map(_to_bool)
    result["BASE_PROFILE"] = (
        result["PROFILE_CLASSIFICATION"]
        .fillna("UNKNOWN")
        .astype(str)
        .str.split(" | ", regex=False)
        .str[0]
        .str.strip()
        .replace("", "UNKNOWN")
    )
    result["GENDER_INFERRED"] = (
        result["GENDER"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.title()
        .replace("", "Unknown")
    )
    result["AUTHOR_KEY"] = result.apply(build_author_key, axis=1)
    for column in ("HINDEX_OA", "CITATIONS_OA", "WORKS_COUNT_OA"):
        result[column] = pd.to_numeric(result[column], errors="coerce")
    return result


def _paper_collaboration_category(regions: Iterable[str]) -> str:
    known = {region for region in regions if region != "Unknown"}
    if known == {"Africa"}:
        return "Africa-only known affiliations"
    if known == {"Outside Africa"}:
        return "No African affiliation detected"
    if known == {"Africa", "Outside Africa"}:
        return "Mixed Africa + outside"
    return "Unknown affiliations only"


def _rounded_percentages(counts: list[int]) -> list[float]:
    total = sum(counts)
    if total == 0:
        return [0.0] * len(counts)
    percentages = [round(count / total * 100, 1) for count in counts]
    if sum(percentages) != 100.0:
        largest_index = max(range(len(counts)), key=counts.__getitem__)
        other_total = sum(
            percent
            for index, percent in enumerate(percentages)
            if index != largest_index
        )
        percentages[largest_index] = 100.0 - other_total
    return percentages


def paper_collaboration_types(df: pd.DataFrame) -> pd.DataFrame:
    """Classify each paper from the known affiliation regions of its authors."""
    records = []
    for doi, group in df.groupby("DOI_NORMALIZED", sort=True):
        records.append(
            {
                "DOI": doi,
                "CATEGORY": _paper_collaboration_category(
                    group["AFFILIATION_REGION"]
                ),
                "AUTHOR_PAPER_RECORDS": int(len(group)),
                "KNOWN_AFFILIATION_RECORDS": int(
                    group["AFFILIATION_REGION"].ne("Unknown").sum()
                ),
            }
        )
    return pd.DataFrame(records)


def collaboration_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize mutually exclusive paper collaboration categories."""
    papers = paper_collaboration_types(df)
    observed = papers["CATEGORY"].value_counts()
    categories = [category for category in COLLABORATION_ORDER if category in observed]
    counts = [int(observed[category]) for category in categories]
    return pd.DataFrame(
        {
            "CATEGORY": categories,
            "PAPERS": counts,
            "PERCENT": _rounded_percentages(counts),
        }
    )


def _leadership_region(regions: Iterable[str]) -> str:
    known = {region for region in regions if region != "Unknown"}
    if known == {"Africa"}:
        return "Africa only"
    if known == {"Outside Africa"}:
        return "Outside Africa only"
    if known == {"Africa", "Outside Africa"}:
        return "Both regions"
    return "Unknown only"


def mixed_leadership_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Classify leadership affiliation region for every mixed-collaboration paper."""
    paper_types = paper_collaboration_types(df)
    mixed_dois = set(
        paper_types.loc[
            paper_types["CATEGORY"].eq("Mixed Africa + outside"), "DOI"
        ]
    )
    mixed = df[df["DOI_NORMALIZED"].isin(mixed_dois)]
    role_masks = {
        "First author": mixed["AUTHOR_POSITION"].eq("first"),
        "Last author": mixed["AUTHOR_POSITION"].eq("last"),
        "Corresponding author": mixed["IS_CORRESPONDING"],
    }

    records = []
    for role in ROLE_ORDER:
        role_rows = mixed[role_masks[role]]
        by_paper = {
            doi: _leadership_region(
                role_rows.loc[
                    role_rows["DOI_NORMALIZED"].eq(doi), "AFFILIATION_REGION"
                ]
            )
            for doi in sorted(mixed_dois)
        }
        counts = [
            sum(region == category for region in by_paper.values())
            for category in LEADERSHIP_REGION_ORDER
        ]
        percentages = _rounded_percentages(counts)
        records.extend(
            {
                "ROLE": role,
                "LEADERSHIP_REGION": category,
                "PAPERS": count,
                "PERCENT": percent,
                "MIXED_PAPERS": len(mixed_dois),
            }
            for category, count, percent in zip(
                LEADERSHIP_REGION_ORDER, counts, percentages
            )
        )
    return pd.DataFrame(records)


def impact_observations(df: pd.DataFrame) -> pd.DataFrame:
    """Create one bibliometric observation per author and affiliation region."""
    known = df[df["AFFILIATION_REGION"].ne("Unknown")].copy()
    return (
        known.sort_values("HINDEX_OA", ascending=False)
        .drop_duplicates(["AUTHOR_KEY", "AFFILIATION_REGION"])
        .loc[
            :,
            [
                "AUTHOR_KEY",
                "AFFILIATION_REGION",
                "HINDEX_OA",
                "CITATIONS_OA",
                "WORKS_COUNT_OA",
            ],
        ]
    )


def impact_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return robust impact statistics by affiliation region."""
    observations = impact_observations(df)
    records = []
    for region, group in observations.groupby("AFFILIATION_REGION", sort=False):
        hindex = group["HINDEX_OA"].dropna()
        citations = group["CITATIONS_OA"].dropna()
        works = group["WORKS_COUNT_OA"].dropna()
        records.append(
            {
                "AFFILIATION_REGION": region,
                "AUTHORS": int(len(group)),
                "HINDEX_MEDIAN": float(hindex.median()),
                "HINDEX_Q1": float(hindex.quantile(0.25)),
                "HINDEX_Q3": float(hindex.quantile(0.75)),
                "CITATIONS_MEDIAN": float(citations.median()),
                "WORKS_MEDIAN": float(works.median()),
            }
        )
    return pd.DataFrame(records)


def _mode_or_unknown(series: pd.Series) -> str:
    values = series.dropna().astype(str)
    return values.mode().iloc[0] if not values.empty else "UNKNOWN"


def profile_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize LLM-inferred profile composition by affiliation region."""
    known = df[df["AFFILIATION_REGION"].ne("Unknown")]
    people = known.groupby(
        ["AUTHOR_KEY", "AFFILIATION_REGION"], as_index=False
    ).agg(BASE_PROFILE=("BASE_PROFILE", _mode_or_unknown))
    counts = (
        people.groupby(["AFFILIATION_REGION", "BASE_PROFILE"])
        .size()
        .rename("AUTHORS")
        .reset_index()
    )
    records = []
    for region, group in counts.groupby("AFFILIATION_REGION", sort=False):
        group = group.sort_values("BASE_PROFILE")
        percentages = _rounded_percentages(group["AUTHORS"].astype(int).tolist())
        for (_, row), percent in zip(group.iterrows(), percentages):
            records.append(
                {
                    "AFFILIATION_REGION": region,
                    "BASE_PROFILE": row["BASE_PROFILE"],
                    "AUTHORS": int(row["AUTHORS"]),
                    "PERCENT": percent,
                }
            )
    return pd.DataFrame(records)


def gender_role_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize name-inferred gender for major authorship roles."""
    records = []
    for region in ("Africa", "Outside Africa"):
        regional = df[df["AFFILIATION_REGION"].eq(region)]
        role_masks = {
            "All author-paper records": pd.Series(True, index=regional.index),
            "First author": regional["AUTHOR_POSITION"].eq("first"),
            "Last author": regional["AUTHOR_POSITION"].eq("last"),
            "Corresponding author": regional["IS_CORRESPONDING"],
        }
        for role, mask in role_masks.items():
            role_rows = regional[mask]
            known = role_rows[
                role_rows["GENDER_INFERRED"].isin(["Female", "Male"])
            ]
            records.append(
                {
                    "AFFILIATION_REGION": region,
                    "ROLE": role,
                    "KNOWN_GENDER_RECORDS": int(len(known)),
                    "FEMALE_RECORDS": int(known["GENDER_INFERRED"].eq("Female").sum()),
                    "FEMALE_PERCENT": round(
                        known["GENDER_INFERRED"].eq("Female").mean() * 100, 1
                    )
                    if len(known)
                    else np.nan,
                }
            )
    return pd.DataFrame(records)


def country_summary(df: pd.DataFrame, min_papers: int = 5) -> pd.DataFrame:
    """Return country participation and leadership counts."""
    known = df[df["AFFILIATION_REGION"].ne("Unknown")]
    records = []
    for country, group in known.groupby("AFFILIATION_COUNTRY"):
        papers = group["DOI_NORMALIZED"].nunique()
        if papers < min_papers:
            continue
        records.append(
            {
                "COUNTRY": country,
                "REGION": classify_affiliation_region(country),
                "PAPERS": int(papers),
                "AUTHOR_PAPER_RECORDS": int(len(group)),
                "DISTINCT_AUTHOR_KEYS": int(group["AUTHOR_KEY"].nunique()),
                "FIRST_AUTHOR_PAPERS": int(
                    group.loc[
                        group["AUTHOR_POSITION"].eq("first"), "DOI_NORMALIZED"
                    ].nunique()
                ),
                "LAST_AUTHOR_PAPERS": int(
                    group.loc[
                        group["AUTHOR_POSITION"].eq("last"), "DOI_NORMALIZED"
                    ].nunique()
                ),
                "CORRESPONDING_AUTHOR_PAPERS": int(
                    group.loc[group["IS_CORRESPONDING"], "DOI_NORMALIZED"].nunique()
                ),
            }
        )
    columns = [
        "COUNTRY",
        "REGION",
        "PAPERS",
        "AUTHOR_PAPER_RECORDS",
        "DISTINCT_AUTHOR_KEYS",
        "FIRST_AUTHOR_PAPERS",
        "LAST_AUTHOR_PAPERS",
        "CORRESPONDING_AUTHOR_PAPERS",
    ]
    if not records:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(records, columns=columns).sort_values(
        ["PAPERS", "AUTHOR_PAPER_RECORDS"], ascending=False
    )


def field_coverage(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate populated-record coverage for every source field."""
    derived_columns = {
        "DOI_NORMALIZED",
        "AFFILIATION_COUNTRY",
        "AFFILIATION_REGION",
        "AUTHOR_POSITION",
        "IS_CORRESPONDING",
        "BASE_PROFILE",
        "GENDER_INFERRED",
        "AUTHOR_KEY",
    }
    records = []
    for column in df.columns:
        if column in derived_columns:
            continue
        populated = ~df[column].map(is_missing)
        records.append(
            {
                "FIELD": column,
                "POPULATED_RECORDS": int(populated.sum()),
                "TOTAL_RECORDS": int(len(df)),
                "COVERAGE_PERCENT": round(populated.mean() * 100, 1),
            }
        )
    return pd.DataFrame(records)


def analysis_summary(input_df: pd.DataFrame, df: pd.DataFrame) -> dict[str, object]:
    """Build the compact JSON-compatible summary used in communications."""
    collaboration = collaboration_summary(df)
    impact = impact_summary(df)
    author_ids = df["AUTHOR_ID_OA"].astype(str).str.strip()
    valid_oa_ids = author_ids[
        ~df["AUTHOR_ID_OA"].map(is_missing)
        & ~author_ids.str.upper().isin({"PUBMED_FALLBACK", "SEMANTIC_FALLBACK"})
    ]
    return {
        "input_dois": int(input_df["DOI"].map(normalize_doi).nunique()),
        "output_dois": int(df["DOI_NORMALIZED"].nunique()),
        "author_paper_records": int(len(df)),
        "distinct_openalex_author_ids": int(valid_oa_ids.nunique()),
        "collaboration_composition": collaboration.to_dict("records"),
        "impact_by_affiliation_region": impact.to_dict("records"),
    }
