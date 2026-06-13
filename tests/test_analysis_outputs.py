import json

import pandas as pd

from scripts.run_analysis import run_analysis
from src.analysis.constants import EXPECTED_MASTER_COLUMNS


def _row(
    doi: str,
    name: str,
    country: str,
    position: str,
    author_id: str,
    corresponding: bool = False,
    profile: str = "COMPUTER_SCIENCE | Unknown",
    hindex: int = 5,
) -> dict[str, object]:
    row = {column: "No data" for column in EXPECTED_MASTER_COLUMNS}
    row.update(
        {
            "PAPER_TITLE": f"Paper {doi}",
            "DOI": doi,
            "YEAR": 2025,
            "AUTHOR_NAME": name,
            "AUTHOR_ID_OA": author_id,
            "GEO_COUNTRY_OA": country,
            "AUTHOR_POS_OA": position,
            "IS_CORRESPONDING_OA": corresponding,
            "AFFILIATION_OA": f"Institution {country}",
            "PROFILE_CLASSIFICATION": profile,
            "GENDER": "Unknown",
            "HINDEX_OA": hindex,
            "CITATIONS_OA": hindex * 10,
            "WORKS_COUNT_OA": hindex * 2,
        }
    )
    return row


def test_run_analysis_writes_tables_and_figures(tmp_path):
    records = [
        _row("10.1/mixed", "Ada", "NG", "first", "A1", True),
        _row(
            "10.1/mixed",
            "Chris",
            "US",
            "last",
            "A2",
            profile="CLINICAL_MEDICINE | Unknown",
            hindex=20,
        ),
        _row("10.1/africa", "Bola", "GH", "first", "A3"),
        _row("10.1/africa", "Dayo", "NG", "last", "A4"),
        _row("10.1/outside", "Eve", "US", "first", "A5"),
        _row("10.1/outside", "Fay", "GB", "last", "A6"),
    ]
    input_path = tmp_path / "input.csv"
    csv_path = tmp_path / "master.csv"
    json_path = tmp_path / "master.json"
    data_dir = tmp_path / "analysis"
    figure_root = tmp_path / "figures"

    pd.DataFrame({"DOI": ["10.1/mixed", "10.1/africa", "10.1/outside"]}).to_csv(
        input_path, index=False
    )
    master = pd.DataFrame(records, columns=EXPECTED_MASTER_COLUMNS)
    master.to_csv(csv_path, index=False)
    master.to_json(json_path, orient="records", indent=4)

    summary = run_analysis(
        input_path=input_path,
        csv_path=csv_path,
        json_path=json_path,
        data_dir=data_dir,
        figure_root=figure_root,
    )

    expected_tables = {
        "analysis_summary.json",
        "paper_collaboration_types.csv",
        "mixed_leadership.csv",
        "impact_summary.csv",
        "profile_summary.csv",
        "country_summary.csv",
        "field_coverage.csv",
        "doi_reconciliation.csv",
    }
    assert expected_tables.issubset({path.name for path in data_dir.iterdir()})

    collaboration = pd.read_csv(data_dir / "paper_collaboration_types.csv")
    assert collaboration["DOI"].nunique() == 3
    leadership = pd.read_csv(data_dir / "mixed_leadership.csv")
    assert leadership.groupby("ROLE")["PERCENT"].sum().round(8).eq(100.0).all()

    stored_summary = json.loads(
        (data_dir / "analysis_summary.json").read_text(encoding="utf-8")
    )
    assert stored_summary == summary
    assert summary["input_dois"] == summary["output_dois"] == 3

    figure_names = {
        "01_corpus_overview",
        "02_collaboration_composition",
        "03_mixed_collaboration_leadership",
        "04_bibliometric_impact_gap",
        "05_research_profile_composition",
    }
    for name in figure_names:
        assert (figure_root / "briefing" / f"{name}.png").stat().st_size > 0
        assert (figure_root / "manuscript" / f"{name}.png").stat().st_size > 0
        assert (figure_root / "manuscript" / f"{name}.svg").stat().st_size > 0

    assert (
        figure_root / "validation" / "01_doi_reconciliation.png"
    ).stat().st_size > 0
