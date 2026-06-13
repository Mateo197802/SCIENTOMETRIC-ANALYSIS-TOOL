"""Repair DOI omissions in the master outputs without reprocessing the corpus."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from io import StringIO
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from analysis.constants import EXPECTED_MASTER_COLUMNS, MISSING_SENTINELS
from analysis.loaders import load_master_outputs, normalize_doi, reconcile_dois
from config import load_config
from modules.enrichment import process_gender_and_llm
from modules.google_scholar import process_google_scholar
from modules.openalex import process_openalex
from modules.orcid import process_orcid
from modules.pubmed import process_pubmed
from modules.scopus import process_scopus
from modules.semantic_scholar import process_semantic_scholar
from utils.id_compressor import compress_authors


def _ensure_master_schema(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for column in EXPECTED_MASTER_COLUMNS:
        if column not in result.columns:
            result[column] = "No data"
    return result.loc[:, EXPECTED_MASTER_COLUMNS]


def merge_repair_records(
    master_df: pd.DataFrame, repair_df: pd.DataFrame
) -> pd.DataFrame:
    """Append absent DOI records while rejecting accidental duplicate repairs."""
    master = _ensure_master_schema(master_df)
    repair = _ensure_master_schema(repair_df)
    existing = {normalize_doi(value) for value in master["DOI"]}
    repair_dois = {normalize_doi(value) for value in repair["DOI"]}
    overlap = sorted(existing & repair_dois)
    if overlap:
        raise ValueError(f"Repair DOI values already exist in master output: {overlap}")
    return pd.concat([master, repair], ignore_index=True).loc[
        :, EXPECTED_MASTER_COLUMNS
    ]


def sanitize_spurious_country_fallback(df: pd.DataFrame) -> pd.DataFrame:
    """Remove historical India defaults where no affiliation evidence exists."""
    result = df.copy()
    affiliation = result["AFFILIATION_OA"].fillna("").astype(str).str.strip().str.upper()
    country = result["GEO_COUNTRY_OA"].fillna("").astype(str).str.strip().str.upper()
    missing_affiliation = affiliation.isin(MISSING_SENTINELS)
    result.loc[missing_affiliation & country.eq("IN"), "GEO_COUNTRY_OA"] = "UNKNOWN"
    return result


def _sanitize_record_country(record: dict[str, Any]) -> dict[str, Any]:
    result = dict(record)
    affiliation = str(result.get("AFFILIATION_OA") or "").strip().upper()
    country = str(result.get("GEO_COUNTRY_OA") or "").strip().upper()
    if affiliation in MISSING_SENTINELS and country == "IN":
        result["GEO_COUNTRY_OA"] = "UNKNOWN"
    return result


def process_missing_doi(doi: str, config: dict[str, object]) -> list[dict]:
    """Run the established extraction chain for one omitted DOI."""
    authors = process_openalex(doi, config)
    if not authors:
        raise RuntimeError(f"OpenAlex returned no author records for {doi}")
    authors = process_pubmed(doi, authors, config)
    authors = process_scopus(doi, authors, config)
    authors = process_semantic_scholar(doi, authors, config)
    authors = process_google_scholar(authors, config)
    authors = compress_authors(authors)
    authors = process_orcid(authors, config)
    return process_gender_and_llm(authors, config)


def _json_compatible(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _json_compatible(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_compatible(item) for item in value]
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def _schema_record(record: dict[str, Any], missing: Any) -> dict[str, Any]:
    return {
        column: _json_compatible(record.get(column, missing))
        for column in EXPECTED_MASTER_COLUMNS
    }


def _serialize_json_records(records: list[dict[str, Any]]) -> str:
    chunks = []
    for record in records:
        text = json.dumps(
            _json_compatible(record),
            ensure_ascii=True,
            indent=4,
            separators=(",", ":"),
        ).replace("/", "\\/")
        chunks.append("\n".join(f"    {line}" for line in text.splitlines()))
    return "[\n" + ",\n".join(chunks) + "\n]"


def _atomic_write_record_outputs(
    csv_records: list[dict[str, Any]],
    json_records: list[dict[str, Any]],
    csv_path: Path,
    json_path: Path,
) -> None:
    csv_tmp = csv_path.with_suffix(csv_path.suffix + ".tmp")
    json_tmp = json_path.with_suffix(json_path.suffix + ".tmp")
    with csv_tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=EXPECTED_MASTER_COLUMNS,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(csv_records)
    json_tmp.write_text(
        _serialize_json_records(json_records),
        encoding="utf-8",
        newline="\n",
    )
    os.replace(csv_tmp, csv_path)
    os.replace(json_tmp, json_path)


def _atomic_write_outputs(
    df: pd.DataFrame, csv_path: Path, json_path: Path
) -> None:
    records = df.to_dict(orient="records")
    csv_records = [_schema_record(record, "") for record in records]
    json_records = [_schema_record(record, None) for record in records]
    _atomic_write_record_outputs(csv_records, json_records, csv_path, json_path)


def _read_raw_records(
    csv_path: Path, json_path: Path
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    csv_records = list(
        csv.DictReader(StringIO(csv_path.read_text(encoding="utf-8")))
    )
    json_records = json.loads(json_path.read_text(encoding="utf-8"))
    if len(csv_records) != len(json_records):
        raise ValueError("CSV and JSON raw record counts differ")
    return csv_records, json_records


def repair_outputs(
    input_path: Path,
    csv_path: Path,
    json_path: Path,
    env_file: Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Repair all missing input DOI values and return output plus reconciliation."""
    if env_file:
        load_dotenv(env_file, override=True)
    config = load_config()
    config["scopusActive"] = False
    config["scholarActive"] = False

    input_df = pd.read_csv(input_path)
    master_df = load_master_outputs(csv_path, json_path)
    csv_records, json_records = _read_raw_records(csv_path, json_path)
    before = reconcile_dois(input_df, master_df)
    missing = before.loc[before["STATUS"].eq("missing"), "DOI"].tolist()
    print(f"Missing DOI values before repair: {len(missing)}")

    repair_records = []
    for doi in missing:
        print(f"Repairing {doi}")
        repair_records.extend(process_missing_doi(doi, config))

    repaired = master_df
    if repair_records:
        repaired = merge_repair_records(master_df, pd.DataFrame(repair_records))
    repaired = sanitize_spurious_country_fallback(repaired)
    repaired = _ensure_master_schema(repaired)

    after = reconcile_dois(input_df, repaired)
    remaining = int(after["STATUS"].eq("missing").sum())
    if remaining:
        raise RuntimeError(f"Repair incomplete: {remaining} DOI values remain missing")

    csv_output = [_sanitize_record_country(record) for record in csv_records]
    json_output = [_sanitize_record_country(record) for record in json_records]
    csv_output.extend(
        _schema_record(record, "") for record in repair_records
    )
    json_output.extend(
        _schema_record(record, None) for record in repair_records
    )
    _atomic_write_record_outputs(csv_output, json_output, csv_path, json_path)
    validated = load_master_outputs(csv_path, json_path)
    if len(validated) != len(repaired):
        raise RuntimeError("Atomic output validation changed the record count")

    print(f"Missing DOI values after repair: {remaining}")
    print(f"Master author-paper records after repair: {len(repaired)}")
    return repaired, after


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=BASE_DIR / "data" / "input" / "input_dois.csv",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=BASE_DIR / "data" / "output" / "csv" / "MASTER_AUTHOR_TABLE.csv",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=BASE_DIR / "data" / "output" / "json" / "MASTER_AUTHOR_TABLE.json",
    )
    parser.add_argument("--env-file", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repair_outputs(args.input, args.csv, args.json, args.env_file)


if __name__ == "__main__":
    main()
