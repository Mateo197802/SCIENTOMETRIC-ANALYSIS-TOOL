"""Validated loading and DOI reconciliation for analysis inputs."""

from pathlib import Path

import pandas as pd

from .constants import EXPECTED_MASTER_COLUMNS


def normalize_doi(value: object) -> str:
    """Return a lower-case DOI without URL prefixes or surrounding whitespace."""
    normalized = str(value).strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix) :]
    return normalized


def load_master_outputs(csv_path: Path, json_path: Path) -> pd.DataFrame:
    """Load matching master CSV/JSON files and validate their shared schema."""
    csv_df = pd.read_csv(csv_path)
    json_df = pd.read_json(json_path)

    if len(csv_df) != len(json_df):
        raise ValueError(
            "CSV and JSON row count mismatch: "
            f"{len(csv_df)} CSV rows versus {len(json_df)} JSON rows"
        )

    csv_columns = set(csv_df.columns)
    json_columns = set(json_df.columns)
    if csv_columns != json_columns:
        raise ValueError("CSV and JSON column sets do not match")

    missing = sorted(set(EXPECTED_MASTER_COLUMNS) - csv_columns)
    if missing:
        raise ValueError(f"Master outputs are missing required columns: {missing}")

    return csv_df.loc[:, EXPECTED_MASTER_COLUMNS].copy()


def reconcile_dois(input_df: pd.DataFrame, master_df: pd.DataFrame) -> pd.DataFrame:
    """Return one sorted row per input DOI with present or missing output status."""
    if "DOI" not in input_df.columns or "DOI" not in master_df.columns:
        raise ValueError("Both input and master data must contain a DOI column")

    input_dois = {normalize_doi(value) for value in input_df["DOI"].dropna()}
    output_dois = {normalize_doi(value) for value in master_df["DOI"].dropna()}

    records = [
        {"DOI": doi, "STATUS": "present" if doi in output_dois else "missing"}
        for doi in sorted(input_dois)
    ]
    return pd.DataFrame(records, columns=["DOI", "STATUS"])
