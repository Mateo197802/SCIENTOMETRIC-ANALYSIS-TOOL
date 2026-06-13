import pandas as pd
import pytest

from scripts.repair_missing_dois import (
    _atomic_write_outputs,
    merge_repair_records,
    sanitize_spurious_country_fallback,
)
from src.analysis.constants import EXPECTED_MASTER_COLUMNS
from src.modules.openalex import _affiliation_metadata


def _row(doi: str, name: str = "Example Author") -> dict[str, object]:
    row = {column: "No data" for column in EXPECTED_MASTER_COLUMNS}
    row.update({"DOI": doi, "AUTHOR_NAME": name, "PAPER_TITLE": f"Paper {doi}"})
    return row


def test_merge_repair_records_rejects_existing_doi():
    master = pd.DataFrame([_row("10.1/existing")])
    repair = pd.DataFrame([_row("10.1/existing", "Duplicate")])

    with pytest.raises(ValueError, match="already exist"):
        merge_repair_records(master, repair)


def test_merge_repair_records_preserves_schema_and_adds_missing_dois():
    master = pd.DataFrame([_row("10.1/existing")])
    repair = pd.DataFrame(
        [_row("10.1/missing-a"), _row("10.1/missing-b")]
    )

    merged = merge_repair_records(master, repair)

    assert list(merged.columns) == list(EXPECTED_MASTER_COLUMNS)
    assert set(merged["DOI"]) == {
        "10.1/existing",
        "10.1/missing-a",
        "10.1/missing-b",
    }


def test_sanitize_spurious_country_fallback_does_not_change_real_india_affiliation():
    data = pd.DataFrame(
        [
            {**_row("10.1/unknown"), "AFFILIATION_OA": "No data", "GEO_COUNTRY_OA": "IN"},
            {
                **_row("10.1/india"),
                "AFFILIATION_OA": "Indian Institute of Science",
                "GEO_COUNTRY_OA": "IN",
            },
        ]
    )

    cleaned = sanitize_spurious_country_fallback(data)

    assert cleaned.loc[0, "GEO_COUNTRY_OA"] == "UNKNOWN"
    assert cleaned.loc[1, "GEO_COUNTRY_OA"] == "IN"


def test_affiliation_metadata_uses_authorship_country_without_institution():
    affiliation, country = _affiliation_metadata(
        {"institutions": [], "countries": ["ZA"]}
    )

    assert affiliation == "No data"
    assert country == "ZA"


def test_affiliation_metadata_returns_unknown_without_evidence():
    affiliation, country = _affiliation_metadata(
        {"institutions": [], "countries": []}
    )

    assert affiliation == "No data"
    assert country == "UNKNOWN"


def test_atomic_writer_uses_repository_stable_serialization(tmp_path):
    data = pd.DataFrame([{"AUTHOR_NAME": "José", "DOI": "10.1/example"}])
    csv_path = tmp_path / "authors.csv"
    json_path = tmp_path / "authors.json"

    _atomic_write_outputs(data, csv_path, json_path)

    assert b"\r\n" not in csv_path.read_bytes()
    assert "\\u00e9" in json_path.read_text(encoding="utf-8")
