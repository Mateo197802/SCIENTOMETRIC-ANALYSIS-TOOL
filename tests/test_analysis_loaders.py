import json

import pandas as pd
import pytest

from src.analysis.constants import EXPECTED_MASTER_COLUMNS
from src.analysis.loaders import load_master_outputs, reconcile_dois


def _master_row(doi: str) -> dict[str, object]:
    row = {column: "No data" for column in EXPECTED_MASTER_COLUMNS}
    row.update(
        {
            "PAPER_TITLE": f"Paper {doi}",
            "DOI": doi,
            "AUTHOR_NAME": "Example Author",
        }
    )
    return row


def test_load_master_outputs_requires_csv_json_row_parity(tmp_path):
    csv_path = tmp_path / "master.csv"
    json_path = tmp_path / "master.json"

    pd.DataFrame([_master_row("10.1/a")]).to_csv(csv_path, index=False)
    json_path.write_text(
        json.dumps([_master_row("10.1/a"), _master_row("10.1/b")]),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="row count"):
        load_master_outputs(csv_path, json_path)


def test_load_master_outputs_requires_expected_schema(tmp_path):
    csv_path = tmp_path / "master.csv"
    json_path = tmp_path / "master.json"
    incomplete = {"DOI": "10.1/a", "AUTHOR_NAME": "Example Author"}

    pd.DataFrame([incomplete]).to_csv(csv_path, index=False)
    json_path.write_text(json.dumps([incomplete]), encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        load_master_outputs(csv_path, json_path)


def test_reconcile_dois_reports_exact_missing_values():
    input_df = pd.DataFrame(
        {
            "DOI": [
                "https://doi.org/10.1038/s41467-025-64391-1",
                "10.1111/exsy.13298",
                "10.1000/present",
            ]
        }
    )
    master_df = pd.DataFrame([_master_row("10.1000/present")])

    reconciliation = reconcile_dois(input_df, master_df)

    assert reconciliation.to_dict("records") == [
        {"DOI": "10.1000/present", "STATUS": "present"},
        {"DOI": "10.1038/s41467-025-64391-1", "STATUS": "missing"},
        {"DOI": "10.1111/exsy.13298", "STATUS": "missing"},
    ]
