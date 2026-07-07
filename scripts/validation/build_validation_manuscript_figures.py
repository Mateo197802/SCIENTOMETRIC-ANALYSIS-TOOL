"""Build editorial figures for the validation-manuscript Google Doc draft."""

from __future__ import annotations

from pathlib import Path
from textwrap import fill

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "assets" / "figures" / "validation_manuscript"

INK = "#102A43"
MUTED = "#627D98"
GRID = "#D7E2EC"
PANEL = "#FFFFFF"
SURFACE = "#FCFCFD"
PALE = "#F7F9FC"

TEAL = "#0F8B8D"
BLUE = "#4C78A8"
GOLD = "#E9B44C"
GREEN = "#1B998B"
RED = "#C84C4C"
GRAY = "#7A828F"


def _configure() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "figure.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "axes.edgecolor": GRID,
            "axes.linewidth": 0.8,
            "svg.hashsalt": "validation-manuscript-v2",
        }
    )


def _canvas(width: float = 16, height: float = 8.4):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig, ax


def _title(ax, title: str, subtitle: str) -> None:
    ax.text(0.035, 0.955, title, ha="left", va="top", fontsize=25, fontweight="bold", color=INK)
    ax.text(0.035, 0.895, subtitle, ha="left", va="top", fontsize=13.2, color=MUTED)


def _box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    body: str,
    *,
    edge: str = INK,
    face: str = PALE,
    title_size: float = 12.6,
    body_size: float = 9.8,
    title_y: float = 0.75,
    body_y: float = 0.34,
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.026",
        linewidth=2.0,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h * title_y,
        title,
        ha="center",
        va="center",
        fontsize=title_size,
        fontweight="bold",
        color=edge,
        linespacing=1.02,
    )
    if body:
        ax.text(
            x + w / 2,
            y + h * body_y,
            body,
            ha="center",
            va="center",
            fontsize=body_size,
            color=INK,
            linespacing=1.18,
        )


def _kpi_card(ax, x: float, y: float, w: float, h: float, value: str, label: str, *, edge: str) -> None:
    _box(ax, x, y, w, h, value, label, edge=edge, face=PANEL, title_size=21, body_size=10.2, title_y=0.62, body_y=0.25)


def _poly_arrow(ax, points: list[tuple[float, float]], *, color: str = INK, lw: float = 2.2) -> None:
    """Draw an orthogonal connector. Every segment must be horizontal or vertical."""
    if len(points) < 2:
        raise ValueError("An arrow needs at least two points.")
    for (x0, y0), (x1, y1) in zip(points[:-2], points[1:-1]):
        if x0 != x1 and y0 != y1:
            raise ValueError(f"Non-orthogonal segment: {(x0, y0)} -> {(x1, y1)}")
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=lw, solid_capstyle="round")
    start = points[-2]
    end = points[-1]
    if start[0] != end[0] and start[1] != end[1]:
        raise ValueError(f"Non-orthogonal arrowhead segment: {start} -> {end}")
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=20,
            linewidth=lw,
            color=color,
            shrinkA=2,
            shrinkB=5,
        )
    )


def _cell(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    *,
    face: str = PANEL,
    edge: str = GRID,
    color: str = INK,
    weight: str = "normal",
    size: float = 9.6,
    wrap: int = 25,
) -> None:
    ax.add_patch(Rectangle((x, y), w, h, linewidth=1.1, edgecolor=edge, facecolor=face))
    ax.text(
        x + w / 2,
        y + h / 2,
        fill(text, width=wrap, break_long_words=False),
        ha="center",
        va="center",
        fontsize=size,
        fontweight=weight,
        color=color,
        linespacing=1.16,
    )


def _save(fig, name: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    png = OUTPUT_DIR / f"{name}.png"
    svg = OUTPUT_DIR / f"{name}.svg"
    fig.savefig(png, dpi=240)
    fig.savefig(svg, metadata={"Date": None})
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    plt.close(fig)


def build_validation_workflow() -> None:
    fig, ax = _canvas(16, 8.4)
    _title(
        ax,
        "Validation-first scientometric workflow",
        "Orthogonal pipeline from published benchmarks to auditable validation decisions.",
    )

    top_y = 0.625
    bottom_y = 0.245
    top_h = 0.205
    bottom_h = 0.205
    w = 0.18
    gap = 0.062
    top_x = [0.04, 0.04 + w + gap, 0.04 + 2 * (w + gap), 0.04 + 3 * (w + gap)]
    bottom_x = [0.17, 0.41, 0.65]

    _box(ax, top_x[0], top_y, w, top_h, "Benchmark\nselection", "Published studies\nquery, time span,\nfilters, outputs", edge=TEAL)
    _box(ax, top_x[1], top_y, w, top_h, "Corpus\nreconstruction", "Search/API retrieval\nrecord screening\nDOI-first table", edge=INK)
    _box(ax, top_x[2], top_y, w, top_h, "Metadata\nenrichment", "OpenAlex | PubMed\nSemantic Scholar\nORCID | Genderize", edge=BLUE)
    _box(ax, top_x[3], top_y, w, top_h, "Author-paper\nmaster table", "35-field table\nCSV/JSON parity\nDOI reconciliation", edge=GOLD)

    _box(ax, bottom_x[0], bottom_y, 0.19, bottom_h, "Benchmark\ncomparison", "Counts and shares\nrank overlap\nauthorship roles\ncitation indicators", edge=INK)
    _box(ax, bottom_x[1], bottom_y, 0.19, bottom_h, "Mismatch\nledger", "Coverage gaps\nsource drift\ndeduplication\ndisambiguation", edge=RED)
    _box(ax, bottom_x[2], bottom_y, 0.19, bottom_h, "Validation\ndecision", "Comparable result\nor documented\nsource-specific\nexplanation", edge=GREEN)

    y_mid = top_y + top_h / 2
    _poly_arrow(ax, [(top_x[0] + w, y_mid), (top_x[1], y_mid)])
    _poly_arrow(ax, [(top_x[1] + w, y_mid), (top_x[2], y_mid)])
    _poly_arrow(ax, [(top_x[2] + w, y_mid), (top_x[3], y_mid)])

    # Deliberate orthogonal route from the master table to the comparison stage.
    table_center_x = top_x[3] + w / 2
    comparison_center_x = bottom_x[0] + 0.19 / 2
    lane_y = 0.515
    _poly_arrow(
        ax,
        [
            (table_center_x, top_y),
            (table_center_x, lane_y),
            (comparison_center_x, lane_y),
            (comparison_center_x, bottom_y + bottom_h),
        ],
        color=GRAY,
    )
    _poly_arrow(ax, [(bottom_x[0] + 0.19, bottom_y + bottom_h / 2), (bottom_x[1], bottom_y + bottom_h / 2)])
    _poly_arrow(ax, [(bottom_x[1] + 0.19, bottom_y + bottom_h / 2), (bottom_x[2], bottom_y + bottom_h / 2)])

    ax.text(0.035, 0.12, "Design principle: every disagreement is retained as a traceable source, access, or normalization issue.", fontsize=11.5, color=MUTED)
    _save(fig, "figure_1_validation_workflow")


def build_benchmark_matrix() -> None:
    fig, ax = _canvas(16, 8.0)
    _title(
        ax,
        "Benchmark studies and reproducible validation targets",
        "Each benchmark contributes an external denominator plus specific outputs that the tool must reproduce or explain.",
    )

    columns = [
        ("Benchmark", 0.145, 16),
        ("Reported denominator", 0.155, 17),
        ("Source and span", 0.205, 23),
        ("Reconstructable outputs", 0.245, 25),
        ("Validation role / blocker", 0.215, 23),
    ]
    x0 = 0.035
    y_header = 0.755
    header_h = 0.105
    row_h = 0.175
    xs = [x0]
    for _, width, _ in columns[:-1]:
        xs.append(xs[-1] + width)

    for (label, width, wrap), x in zip(columns, xs):
        _cell(ax, x, y_header, width, header_h, label, face="#EAF0F6", edge=INK, weight="bold", size=11.3, wrap=wrap)

    rows = [
        (
            "Yan & Wang 2023",
            "n = 2,217 documents",
            "Web of Science; academic publishing; 1970-2020",
            "Countries, institutions, productive authors, highly cited papers",
            "Recommended first run: moderate corpus and closest endpoint match",
        ),
        (
            "Baminiwatta & Solangaarachchi 2021",
            "n = 16,581 publications",
            "Web of Science; mindfulness research; 1966-2021",
            "Country collaboration, co-authorship structure, citation bursts",
            "Scale and collaboration-network stress test",
        ),
        (
            "Basilio et al. 2022",
            "35,643 retrieved; 23,494 analyzed",
            "Web of Science plus Scopus; MCDA methods; 1977-Apr 2022",
            "Authors, countries, institutions, citation and topic patterns",
            "Multi-source benchmark; Scopus access is material",
        ),
    ]

    for r, row in enumerate(rows):
        y = y_header - (r + 1) * row_h
        face = PANEL if r % 2 == 0 else PALE
        for c, (text, x) in enumerate(zip(row, xs)):
            width = columns[c][1]
            wrap = columns[c][2]
            color = INK
            weight = "normal"
            size = 9.8
            if c == 0:
                weight = "bold"
            if c == 1:
                color = GOLD
                weight = "bold"
                size = 12.8
            _cell(ax, x, y, width, row_h, text, face=face, edge=GRID, color=color, weight=weight, size=size, wrap=wrap)

    note = (
        "Comparison metrics: document-count agreement, DOI loss log, top-country and top-institution rank overlap, "
        "author overlap where reported, and citation-source mismatch categories."
    )
    ax.text(0.035, 0.105, fill(note, width=128), fontsize=10.8, color=MUTED, linespacing=1.15)
    _save(fig, "figure_2_benchmark_matrix")


def build_second_run_expansion() -> None:
    fig, ax = _canvas(16, 8.4)
    _title(
        ax,
        "Evidence boundary before final benchmark claims",
        "Current outputs support methods and feasibility; final validation requires benchmark reruns and second-source enrichment.",
    )

    top_y = 0.59
    lower_y = 0.235
    w = 0.25
    h = 0.225
    _box(ax, 0.06, top_y, w, h, "Completed\ncore run", "OpenAlex\nPubMed\nSemantic Scholar\nORCID\nGenderize\nAzure OpenAI", edge=TEAL, body_size=9.4)
    _box(ax, 0.375, top_y, w, h, "Validated\noutputs", "DOI reconciliation\nCSV/JSON parity\nAuthor-paper table\nCoverage summaries", edge=INK)
    _box(ax, 0.69, top_y, w, h, "Preliminary\nreporting", "Stress-test corpus\nBenchmark candidates\nMethods draft\nNo final claims", edge=GOLD)
    _poly_arrow(ax, [(0.06 + w, top_y + h / 2), (0.375, top_y + h / 2)])
    _poly_arrow(ax, [(0.375 + w, top_y + h / 2), (0.69, top_y + h / 2)])

    _box(ax, 0.375, lower_y, w, h, "Second-run\nmetadata", "Scopus IDs\naffiliation history\ncitation metadata\nGoogle Scholar checks", edge=BLUE)
    _box(ax, 0.69, lower_y, w, h, "Final validation\nlayer", "Benchmark comparison\nrank overlap\nmismatch ledger\nmanual audit sample", edge=GREEN)
    _poly_arrow(ax, [(0.375 + w, lower_y + h / 2), (0.69, lower_y + h / 2)], color=GRAY)
    _poly_arrow(ax, [(0.69 + w / 2, top_y), (0.69 + w / 2, lower_y + h)], color=GRAY)

    ax.text(0.06, 0.13, "Interpretation rule: preliminary engineering outputs can be reported now; external validity claims wait for benchmark reproduction.", fontsize=11.5, color=MUTED)
    _save(fig, "figure_3_second_run_expansion")


def build_preliminary_results_summary() -> None:
    fig, ax = _canvas(16, 8.4)
    _title(
        ax,
        "Preliminary stress-test output inventory",
        "The completed closed-corpus run demonstrates engineering feasibility, not external scientific validation.",
    )

    cards = [
        ("1,158", "input DOI values", TEAL),
        ("7,361", "author-paper records", BLUE),
        ("5,675", "distinct valid\nOpenAlex author IDs", GOLD),
        ("35", "output fields", GREEN),
    ]
    x = 0.06
    for value, label, color in cards:
        _kpi_card(ax, x, 0.62, 0.20, 0.18, value, label, edge=color)
        x += 0.235

    _box(
        ax,
        0.08,
        0.28,
        0.38,
        0.22,
        "What the current run supports",
        "DOI ingestion at corpus scale\nMulti-source metadata retrieval\nAuthor-paper unrolling\nCSV/JSON parity checks\nPreliminary variable dictionary",
        edge=TEAL,
        body_size=10.2,
    )
    _box(
        ax,
        0.54,
        0.28,
        0.38,
        0.22,
        "What remains unvalidated",
        "Benchmark reproduction accuracy\nScopus/Google Scholar contribution\nDatabase drift effects\nManual audit of inferred fields\nFinal country/institution conclusions",
        edge=RED,
        body_size=10.2,
    )
    ax.text(0.08, 0.17, "Reporting status: these counts should appear as pipeline feasibility results, not as final scientometric findings.", fontsize=11.4, color=MUTED)
    _save(fig, "figure_4_preliminary_results_summary")


def build_validation_readiness_status() -> None:
    fig, ax = _canvas(16, 8.4)
    _title(
        ax,
        "Preliminary validation readiness dashboard",
        "The manuscript can advance as a methods draft while benchmark reruns and paid/institutional metadata checks are pending.",
    )

    columns = [
        ("Validation component", 0.30, 28),
        ("Current status", 0.20, 19),
        ("Evidence now", 0.26, 28),
        ("Next action", 0.22, 24),
    ]
    x0 = 0.04
    xs = [x0]
    for _, width, _ in columns[:-1]:
        xs.append(xs[-1] + width)
    y_header = 0.735
    row_h = 0.102

    for (label, width, wrap), x in zip(columns, xs):
        _cell(ax, x, y_header, width, 0.085, label, face="#EAF0F6", edge=INK, weight="bold", size=11.0, wrap=wrap)

    rows = [
        ("DOI ingestion and reconciliation", "Complete", "Closed-corpus DOI run completed", "Carry DOI loss log into benchmarks"),
        ("Author-paper table construction", "Complete", "7,361 records; 35 fields; CSV/JSON parity", "Freeze schema and variable dictionary"),
        ("Benchmark protocol extraction", "Drafted", "Three benchmark candidates selected", "Finalize Yan & Wang first-run protocol"),
        ("Scopus enrichment", "Pending", "Access dependency identified", "Confirm institutional/API access"),
        ("Google Scholar / SerpAPI checks", "Pending", "Cost and query need scoped", "Run one-month validation batch if approved"),
        ("Manual audit sample", "Pending", "Audit targets defined", "Sample authors, affiliations, inferred fields"),
    ]

    status_colors = {"Complete": GREEN, "Drafted": GOLD, "Pending": RED}
    for r, row in enumerate(rows):
        y = y_header - (r + 1) * row_h
        face = PANEL if r % 2 == 0 else PALE
        for c, (text, x) in enumerate(zip(row, xs)):
            width = columns[c][1]
            wrap = columns[c][2]
            color = INK
            weight = "normal"
            if c == 0:
                weight = "bold"
            if c == 1:
                color = status_colors[text]
                weight = "bold"
            _cell(ax, x, y, width, row_h, text, face=face, edge=GRID, color=color, weight=weight, size=9.1, wrap=wrap)

    ax.text(
        0.04,
        0.06,
        "Decision gate: final results should be locked only after benchmark reruns, source-specific mismatch analysis, and manual audit.",
        fontsize=10.8,
        color=MUTED,
    )
    _save(fig, "figure_5_validation_readiness_status")


def main() -> None:
    _configure()
    build_validation_workflow()
    build_benchmark_matrix()
    build_second_run_expansion()
    build_preliminary_results_summary()
    build_validation_readiness_status()
    print(f"Validation manuscript figures written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
