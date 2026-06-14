"""Build deterministic tables and figures used by the manuscript."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

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
SOURCE_FIGURE_DIR = BASE_DIR / "assets" / "figures" / "manuscript"
FIGURE_DIR = BASE_DIR / "manuscript" / "figures"

NAVY = "#17324D"
TEAL = "#0B7A75"
LIGHT_TEAL = "#DDF3F0"
LIGHT_NAVY = "#E6EEF5"
NEUTRAL = "#EEF1F4"
DARK_GRAY = "#344054"
MID_GRAY = "#667085"
WHITE = "#FFFFFF"


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


def _draw_pipeline(output_dir: Path) -> None:
    fig, axis = plt.subplots(figsize=(16, 10), dpi=200)
    fig.patch.set_facecolor(WHITE)
    axis.set_xlim(0, 16)
    axis.set_ylim(0, 10)
    axis.axis("off")

    axis.text(
        0.8,
        9.55,
        "Scientometric Analysis Tool: reproducible author-level workflow",
        color=NAVY,
        fontsize=24,
        fontweight="bold",
        va="top",
    )
    axis.text(
        0.8,
        9.05,
        "Closed-corpus ingestion, identity reconciliation, enrichment, validation, and analysis",
        color=MID_GRAY,
        fontsize=13,
        va="top",
    )

    stages = [
        (
            0.8,
            7.35,
            4.4,
            1.05,
            "ML4Africa closed DOI corpus\nn = 1,158",
            LIGHT_NAVY,
            NAVY,
        ),
        (
            5.8,
            7.35,
            4.4,
            1.05,
            "Metadata retrieval\nOpenAlex | PubMed |\nSemantic Scholar",
            NEUTRAL,
            DARK_GRAY,
        ),
        (
            10.8,
            7.35,
            4.4,
            1.05,
            "Identifier reconciliation\nand within-paper consolidation",
            NEUTRAL,
            DARK_GRAY,
        ),
        (
            10.8,
            5.55,
            4.4,
            1.05,
            "Supplementary enrichment\nORCID | Genderize |\nAzure OpenAI",
            NEUTRAL,
            DARK_GRAY,
        ),
        (
            5.8,
            5.55,
            4.4,
            1.05,
            "35-field author-paper table\n7,361 records\n5,675 distinct OpenAlex IDs",
            LIGHT_TEAL,
            TEAL,
        ),
        (
            0.8,
            5.55,
            4.4,
            1.05,
            "Validation layer\nCSV/JSON parity\nComplete DOI reconciliation",
            NEUTRAL,
            DARK_GRAY,
        ),
    ]

    for x, y, width, height, text, face, edge in stages:
        patch = FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.04,rounding_size=0.09",
            facecolor=face,
            edgecolor=edge,
            linewidth=2.0,
        )
        axis.add_patch(patch)
        axis.text(
            x + width / 2,
            y + height / 2,
            text,
            ha="center",
            va="center",
            color=edge,
            fontsize=11.5,
            fontweight="bold",
            linespacing=1.25,
        )

    arrows = [
        ((5.2, 7.88), (5.75, 7.88)),
        ((10.2, 7.88), (10.75, 7.88)),
        ((13.0, 7.32), (13.0, 6.65)),
        ((10.75, 6.08), (10.25, 6.08)),
        ((5.75, 6.08), (5.25, 6.08)),
    ]
    for start, end in arrows:
        axis.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=18,
                color=MID_GRAY,
                linewidth=2.0,
            )
        )

    output_boxes = [
        (0.8, 2.75, 4.4, 1.35, "Collaboration\ncomposition", LIGHT_TEAL, TEAL),
        (
            5.8,
            2.75,
            4.4,
            1.35,
            "First, last, and corresponding\nauthor leadership",
            LIGHT_TEAL,
            TEAL,
        ),
        (
            10.8,
            2.75,
            4.4,
            1.35,
            "Regional and country-level\nbibliometric impact",
            LIGHT_NAVY,
            NAVY,
        ),
    ]
    axis.text(
        0.8,
        4.62,
        "Primary analytical outputs",
        color=NAVY,
        fontsize=16,
        fontweight="bold",
    )
    for x, y, width, height, text, face, edge in output_boxes:
        patch = FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.04,rounding_size=0.09",
            facecolor=face,
            edgecolor=edge,
            linewidth=2.0,
        )
        axis.add_patch(patch)
        axis.text(
            x + width / 2,
            y + height / 2,
            text,
            ha="center",
            va="center",
            color=edge,
            fontsize=13,
            fontweight="bold",
        )
        axis.add_patch(
            FancyArrowPatch(
                (3.0 if x == 0.8 else 8.0 if x == 5.8 else 13.0, 5.5),
                (x + width / 2, 4.15),
                arrowstyle="-|>",
                mutation_scale=18,
                color=MID_GRAY,
                linewidth=1.8,
                connectionstyle="arc3,rad=0",
            )
        )

    note = FancyBboxPatch(
        (0.8, 0.65),
        14.4,
        1.15,
        boxstyle="round,pad=0.05,rounding_size=0.08",
        facecolor="#FAFAFA",
        edgecolor="#D0D5DD",
        linewidth=1.4,
    )
    axis.add_patch(note)
    axis.text(
        1.1,
        1.42,
        "Executed run:",
        color=DARK_GRAY,
        fontsize=12,
        fontweight="bold",
        va="center",
    )
    axis.text(
        2.85,
        1.42,
        "OpenAlex, PubMed, Semantic Scholar, ORCID, Genderize, and Azure OpenAI",
        color=DARK_GRAY,
        fontsize=11.5,
        va="center",
    )
    axis.text(
        1.1,
        0.98,
        "Implemented but disabled:",
        color=MID_GRAY,
        fontsize=12,
        fontweight="bold",
        va="center",
    )
    axis.text(
        4.65,
        0.98,
        "Scopus and Google Scholar integrations were not used in the completed corpus run.",
        color=MID_GRAY,
        fontsize=11.5,
        va="center",
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output_dir / "figure_1_pipeline.png",
        dpi=200,
        facecolor=WHITE,
        bbox_inches="tight",
        pad_inches=0.15,
    )
    fig.savefig(
        output_dir / "figure_1_pipeline.svg",
        format="svg",
        facecolor=WHITE,
        bbox_inches="tight",
        pad_inches=0.15,
        metadata={"Date": None},
    )
    plt.close(fig)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def _fit_image(image: Image.Image, width: int, height: int) -> Image.Image:
    ratio = min(width / image.width, height / image.height)
    size = (int(image.width * ratio), int(image.height * ratio))
    return image.resize(size, Image.Resampling.LANCZOS)


def _stack_panels(
    sources: list[Path],
    destination: Path,
    panel_labels: list[str],
) -> None:
    canvas_width = 3000
    outer_margin = 100
    panel_gap = 90
    label_height = 90
    usable_width = canvas_width - (2 * outer_margin)
    panels: list[Image.Image] = []
    for source in sources:
        with Image.open(source) as image:
            panel = image.convert("RGB")
            panel = _fit_image(panel, usable_width, 1600)
            panels.append(panel)

    canvas_height = (
        2 * outer_margin
        + sum(panel.height + label_height for panel in panels)
        + panel_gap * (len(panels) - 1)
    )
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)
    font = _font(68, bold=True)
    y = outer_margin
    for label, panel in zip(panel_labels, panels, strict=True):
        draw.text((outer_margin, y), label, fill=NAVY, font=font)
        y += label_height
        x = (canvas_width - panel.width) // 2
        canvas.paste(panel, (x, y))
        y += panel.height + panel_gap
    canvas.save(destination, format="PNG", optimize=True)


def _copy_figure(source: Path, destination: Path) -> None:
    with Image.open(source) as image:
        image.convert("RGB").save(destination, format="PNG", optimize=True)


def build_figures(output_dir: Path = FIGURE_DIR) -> list[Path]:
    """Build original and composite figures from committed project outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    _draw_pipeline(output_dir)
    _stack_panels(
        [
            SOURCE_FIGURE_DIR / "01_corpus_overview.png",
            SOURCE_FIGURE_DIR / "02_collaboration_composition.png",
        ],
        output_dir / "figure_2_corpus_collaboration.png",
        ["A", "B"],
    )
    _stack_panels(
        [
            SOURCE_FIGURE_DIR / "03_mixed_collaboration_leadership.png",
            SOURCE_FIGURE_DIR / "07_mixed_collaboration_country_leadership.png",
        ],
        output_dir / "figure_3_mixed_leadership.png",
        ["A", "B"],
    )
    _copy_figure(
        SOURCE_FIGURE_DIR / "04_bibliometric_impact_gap.png",
        output_dir / "figure_4_regional_hindex.png",
    )
    _copy_figure(
        SOURCE_FIGURE_DIR / "06_country_hindex_distribution.png",
        output_dir / "figure_5_country_hindex.png",
    )
    return sorted(output_dir.glob("figure_*"))


def main() -> None:
    tables = build_tables()
    figures = build_figures()
    print(
        "Manuscript tables built: "
        + ", ".join(f"{name} ({len(table)} rows)" for name, table in tables.items())
    )
    print("Manuscript figures built: " + ", ".join(path.name for path in figures))


if __name__ == "__main__":
    main()
