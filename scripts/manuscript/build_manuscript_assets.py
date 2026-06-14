"""Build deterministic tables and figures used by the manuscript."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.analysis.loaders import load_master_outputs, reconcile_dois
from src.analysis.manuscript_metrics import (
    build_collaboration_leadership_table,
    build_corpus_table,
    build_impact_table,
    corpus_characteristics,
    publication_year_summary,
)
from src.analysis.metrics import (
    add_analysis_columns,
    collaboration_summary,
    field_coverage,
    impact_summary,
    mixed_leadership_summary,
)

INPUT_PATH = BASE_DIR / "data" / "input" / "input_dois.csv"
MASTER_CSV = BASE_DIR / "data" / "output" / "csv" / "MASTER_AUTHOR_TABLE.csv"
MASTER_JSON = (
    BASE_DIR / "data" / "output" / "json" / "MASTER_AUTHOR_TABLE.json"
)
TABLE_DIR = BASE_DIR / "manuscript" / "tables"


def _write_csv(table: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(
        path,
        index=False,
        lineterminator="\n",
        float_format="%.1f",
    )


def build_tables() -> dict[str, pd.DataFrame]:
    """Build the manuscript tables from validated repository outputs."""
    input_df = pd.read_csv(INPUT_PATH)
    master = load_master_outputs(MASTER_CSV, MASTER_JSON)
    reconciliation = reconcile_dois(input_df, master)
    if reconciliation["STATUS"].eq("missing").any():
        raise RuntimeError("Manuscript assets require complete DOI reconciliation")

    data = add_analysis_columns(master)
    characteristics = corpus_characteristics(input_df, data)
    coverage = field_coverage(data)
    collaboration = collaboration_summary(data)
    leadership = mixed_leadership_summary(data)
    impact = impact_summary(data)

    tables = {
        "table_1_corpus_characteristics.csv": build_corpus_table(
            characteristics, coverage
        ),
        "table_2_collaboration_leadership.csv": (
            build_collaboration_leadership_table(
                collaboration,
                leadership,
                total_papers=int(data["DOI_NORMALIZED"].nunique()),
            )
        ),
        "table_3_bibliometric_impact.csv": build_impact_table(impact),
        "supplementary_publication_years.csv": publication_year_summary(data),
    }
    for filename, table in tables.items():
        _write_csv(table, TABLE_DIR / filename)
    return tables


def main() -> None:
    tables = build_tables()
    print(
        "Manuscript tables built: "
        + ", ".join(f"{name} ({len(table)} rows)" for name, table in tables.items())
    )


if __name__ == "__main__":
    main()
