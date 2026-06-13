"""Generate the audited preliminary scientometric analysis package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.analysis.figures import render_all_figures
from src.analysis.loaders import load_master_outputs, reconcile_dois
from src.analysis.metrics import (
    add_analysis_columns,
    analysis_summary,
    collaboration_summary,
    country_summary,
    field_coverage,
    gender_role_summary,
    impact_observations,
    impact_summary,
    mixed_leadership_summary,
    paper_collaboration_types,
    profile_summary,
)


def _write_csv(data: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(
        path,
        index=False,
        lineterminator="\n",
        float_format="%.1f",
    )


def run_analysis(
    input_path: Path,
    csv_path: Path,
    json_path: Path,
    data_dir: Path,
    figure_root: Path,
) -> dict[str, object]:
    """Validate the corpus, export source tables, and render all figures."""
    input_df = pd.read_csv(input_path)
    master = load_master_outputs(csv_path, json_path)
    data = add_analysis_columns(master)
    reconciliation = reconcile_dois(input_df, master)
    missing_count = int(reconciliation["STATUS"].eq("missing").sum())
    if missing_count:
        raise RuntimeError(
            f"Analysis requires complete DOI reconciliation; {missing_count} remain"
        )

    paper_types = paper_collaboration_types(data)
    collaboration = collaboration_summary(data)
    leadership = mixed_leadership_summary(data)
    observations = impact_observations(data)
    impact = impact_summary(data)
    profiles = profile_summary(data)
    countries = country_summary(data)
    coverage = field_coverage(data)
    gender_roles = gender_role_summary(data)
    summary = analysis_summary(input_df, data)
    summary["doi_reconciliation"] = {
        "present": int(reconciliation["STATUS"].eq("present").sum()),
        "missing": missing_count,
    }
    summary["mixed_collaboration_leadership"] = leadership.to_dict("records")

    outputs = {
        "paper_collaboration_types.csv": paper_types,
        "collaboration_summary.csv": collaboration,
        "mixed_leadership.csv": leadership,
        "impact_observations.csv": observations,
        "impact_summary.csv": impact,
        "profile_summary.csv": profiles,
        "country_summary.csv": countries,
        "field_coverage.csv": coverage,
        "gender_role_summary.csv": gender_roles,
        "doi_reconciliation.csv": reconciliation,
    }
    for filename, table in outputs.items():
        _write_csv(table, data_dir / filename)

    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "analysis_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    render_all_figures(
        summary=summary,
        collaboration=collaboration,
        leadership=leadership,
        observations=observations,
        impact=impact,
        profiles=profiles,
        coverage=coverage,
        reconciliation=reconciliation,
        figure_root=figure_root,
    )
    return summary


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
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=BASE_DIR / "data" / "analysis",
    )
    parser.add_argument(
        "--figure-root",
        type=Path,
        default=BASE_DIR / "assets" / "figures",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_analysis(
        input_path=args.input,
        csv_path=args.csv,
        json_path=args.json,
        data_dir=args.data_dir,
        figure_root=args.figure_root,
    )
    print(
        "Analysis complete: "
        f"{summary['output_dois']:,} DOI values, "
        f"{summary['author_paper_records']:,} author-paper records"
    )


if __name__ == "__main__":
    main()
