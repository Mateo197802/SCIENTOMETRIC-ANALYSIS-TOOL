"""Build figures for the validation-manuscript Google Doc draft."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "assets" / "figures" / "validation_manuscript"

NAVY = "#102A43"
TEAL = "#0F8B8D"
GOLD = "#E9B44C"
BLUE = "#4C78A8"
SLATE = "#627D98"
LIGHT = "#EAF0F6"
PALE = "#F7F9FC"
GREEN = "#1B998B"
RED = "#C84C4C"


def _configure() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.edgecolor": "#BCCCDC",
            "axes.linewidth": 0.8,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "svg.hashsalt": "validation-manuscript",
        }
    )


def _box(axis, xy, width, height, title, body, color=NAVY, face=PALE):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.018,rounding_size=0.035",
        linewidth=1.8,
        edgecolor=color,
        facecolor=face,
    )
    axis.add_patch(patch)
    axis.text(
        x + width / 2,
        y + height * 0.79,
        title,
        ha="center",
        va="center",
        fontsize=12.2,
        fontweight="bold",
        color=color,
        linespacing=1.08,
    )
    axis.text(
        x + width / 2,
        y + height * 0.29,
        body,
        ha="center",
        va="center",
        fontsize=9.8,
        color=NAVY,
        linespacing=1.18,
    )


def _arrow(axis, start, end, color=NAVY):
    axis.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=1.7,
            color=color,
            shrinkA=4,
            shrinkB=4,
        )
    )


def _save(fig, name: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    png = OUTPUT_DIR / f"{name}.png"
    svg = OUTPUT_DIR / f"{name}.svg"
    fig.savefig(png, dpi=260, bbox_inches="tight")
    fig.savefig(svg, bbox_inches="tight", metadata={"Date": None})
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    plt.close(fig)


def build_validation_workflow() -> None:
    fig, axis = plt.subplots(figsize=(13.8, 7.5))
    axis.set_axis_off()
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.text(
        0.03,
        0.95,
        "Validation-first scientometric workflow",
        fontsize=23,
        fontweight="bold",
        color=NAVY,
        ha="left",
    )
    axis.text(
        0.03,
        0.895,
        "The tool is evaluated by reproducing published benchmark results, not by treating one stress-test corpus as the main claim.",
        fontsize=12.5,
        color=SLATE,
        ha="left",
    )
    boxes = [
        ((0.04, 0.59), "Benchmark\nselection", "Published studies\nreproducible query\nand filters", TEAL),
        ((0.29, 0.59), "Corpus\nreconstruction", "Search/API retrieval\nDOI-first\nnormalization", NAVY),
        ((0.54, 0.59), "Metadata\nenrichment", "OpenAlex | PubMed\nSemantic Scholar\nORCID | Genderize", BLUE),
        ((0.79, 0.59), "Author-paper\nmaster table", "35-field table\nCSV/JSON parity\nDOI reconciliation", GOLD),
        ((0.17, 0.24), "Benchmark\ncomparison", "Counts, affiliations\nauthorship roles\ncitations", NAVY),
        ((0.50, 0.24), "Mismatch\nledger", "Coverage, access\ndeduplication\ndisambiguation", RED),
        ((0.77, 0.24), "Validation\ndecision", "Comparable results\nor explained\ndivergence", GREEN),
    ]
    for xy, title, body, color in boxes:
        _box(axis, xy, 0.18, 0.21, title, body, color=color)
    _arrow(axis, (0.22, 0.695), (0.29, 0.695))
    _arrow(axis, (0.47, 0.695), (0.54, 0.695))
    _arrow(axis, (0.72, 0.695), (0.79, 0.695))
    _arrow(axis, (0.87, 0.59), (0.30, 0.45), color=SLATE)
    _arrow(axis, (0.35, 0.345), (0.50, 0.345))
    _arrow(axis, (0.68, 0.345), (0.77, 0.345))
    _save(fig, "figure_1_validation_workflow")


def build_benchmark_matrix() -> None:
    fig, axis = plt.subplots(figsize=(13.8, 7.2))
    axis.set_axis_off()
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.text(
        0.03,
        0.94,
        "Candidate benchmarks and validation endpoints",
        fontsize=23,
        fontweight="bold",
        color=NAVY,
    )
    axis.text(
        0.03,
        0.885,
        "Benchmarks were selected because they report corpus construction, time range, filters, final count, and bibliometric outputs.",
        fontsize=12.5,
        color=SLATE,
    )
    rows = [
        ("Yan & Wang\n2023", "2,217", "Academic publishing\nWoS, 1970-2020", "Countries\nInstitutions\nAuthors\nCited papers"),
        ("Baminiwatta &\nSolangaarachchi\n2021", "16,581", "Mindfulness\nWoS, 1966-2021", "Country collaboration\nCo-authorship\nCitation bursts"),
        ("Basilio et al.\n2022", "23,494", "MCDA methods\nWoS + Scopus,\n1977-2022", "Authors\nCountries\nInstitutions\nCitation patterns"),
    ]
    x_positions = [0.04, 0.22, 0.38, 0.63]
    widths = [0.16, 0.12, 0.22, 0.30]
    headers = ["Benchmark", "Published\ncount", "Corpus definition", "Comparison endpoints"]
    y_top = 0.735
    row_h = 0.19
    for x, width, header in zip(x_positions, widths, headers):
        _box(axis, (x, y_top), width, 0.095, header, "", color=NAVY, face=LIGHT)
    for row_index, row in enumerate(rows):
        y = y_top - (row_index + 1) * row_h
        for col_index, value in enumerate(row):
            x = x_positions[col_index]
            width = widths[col_index]
            face = "#FFFFFF" if row_index % 2 == 0 else PALE
            color = [TEAL, GOLD, BLUE, NAVY][col_index]
            patch = FancyBboxPatch(
                (x, y),
                width,
                row_h * 0.82,
                boxstyle="round,pad=0.012,rounding_size=0.02",
                linewidth=1.2,
                edgecolor="#D7E2EC",
                facecolor=face,
            )
            axis.add_patch(patch)
            axis.text(
                x + width / 2,
                y + row_h * 0.41,
                value,
                ha="center",
                va="center",
                fontsize=11.5 if col_index != 1 else 16,
                fontweight="bold" if col_index <= 1 else "normal",
                color=color if col_index == 1 else NAVY,
                linespacing=1.22,
            )
    _save(fig, "figure_2_benchmark_matrix")


def build_second_run_expansion() -> None:
    fig, axis = plt.subplots(figsize=(13.8, 7.2))
    axis.set_axis_off()
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.text(
        0.03,
        0.94,
        "Current evidence base and second-run expansion",
        fontsize=23,
        fontweight="bold",
        color=NAVY,
    )
    axis.text(
        0.03,
        0.885,
        "Preliminary results are intentionally limited until Scopus and Google Scholar/SerpAPI enrichment are rerun or ruled out.",
        fontsize=12.5,
        color=SLATE,
    )
    _box(axis, (0.06, 0.56), 0.25, 0.24, "Completed\ncore run", "OpenAlex\nPubMed\nSemantic Scholar\nORCID\nGenderize\nAzure OpenAI", TEAL)
    _box(axis, (0.38, 0.56), 0.25, 0.24, "Validated\noutputs", "DOI reconciliation\nCSV/JSON parity\nAuthor-paper table\nCoverage summaries", NAVY)
    _box(axis, (0.70, 0.56), 0.23, 0.24, "Preliminary\nreporting", "Stress-test corpus\nBenchmark candidates\nMethods draft\nNo final claims", GOLD)
    _arrow(axis, (0.31, 0.68), (0.38, 0.68))
    _arrow(axis, (0.63, 0.68), (0.70, 0.68))
    _box(axis, (0.16, 0.23), 0.27, 0.22, "Second-run\nmetadata", "Scopus identifiers\naffiliation history\ncitation metadata\nGoogle Scholar checks", BLUE)
    _box(axis, (0.57, 0.23), 0.27, 0.22, "Final validation\nlayer", "Benchmark comparison\nrank overlap\nmismatch ledger\nmanual audit sample", GREEN)
    _arrow(axis, (0.44, 0.34), (0.57, 0.34), color=SLATE)
    _arrow(axis, (0.81, 0.56), (0.71, 0.45), color=SLATE)
    _save(fig, "figure_3_second_run_expansion")


def main() -> None:
    _configure()
    build_validation_workflow()
    build_benchmark_matrix()
    build_second_run_expansion()
    print(f"Validation manuscript figures written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
