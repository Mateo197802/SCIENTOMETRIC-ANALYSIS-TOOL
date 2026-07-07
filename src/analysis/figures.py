"""Rendering functions for the preliminary scientometric figure package."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator

NAVY = "#102A43"
TEAL = "#0F8B8D"
GOLD = "#E9B44C"
BLUE = "#4C78A8"
SLATE = "#627D98"
LIGHT = "#EAF0F6"
PALE = "#F7F9FC"
RED = "#C84C4C"


def _configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 17,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "axes.edgecolor": "#BCCCDC",
            "axes.linewidth": 0.8,
            "axes.grid": False,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "svg.hashsalt": "scientometric-analysis-tool",
        }
    )


def _save(
    fig: plt.Figure,
    name: str,
    briefing_dir: Path,
    analysis_dir: Path,
) -> None:
    briefing_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        briefing_dir / f"{name}.png",
        dpi=220,
        bbox_inches="tight",
        facecolor="white",
    )
    fig.savefig(
        analysis_dir / f"{name}.png",
        dpi=300,
        bbox_inches="tight",
        facecolor="white",
    )
    svg_path = analysis_dir / f"{name}.svg"
    fig.savefig(
        svg_path,
        bbox_inches="tight",
        facecolor="white",
        metadata={"Date": None},
    )
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    plt.close(fig)


def _short_category(value: str) -> str:
    labels = {
        "Africa-only known affiliations": "Africa-only\naffiliations",
        "Mixed Africa + outside": "Africa + outside\ncollaboration",
        "No African affiliation detected": "No African\naffiliation detected",
        "Unknown affiliations only": "Unknown\naffiliations only",
    }
    return labels.get(value, value)


def render_corpus_overview(
    summary: dict[str, object],
    coverage: pd.DataFrame,
    briefing_dir: Path,
    analysis_dir: Path,
) -> None:
    fig = plt.figure(figsize=(13.2, 7.4))
    grid = fig.add_gridspec(2, 4, height_ratios=[0.9, 1.4], hspace=0.42)
    cards = [
        ("Input DOI values", summary["input_dois"]),
        ("Reconciled DOI values", summary["output_dois"]),
        ("Author-paper records", summary["author_paper_records"]),
        ("Distinct OpenAlex author IDs", summary["distinct_openalex_author_ids"]),
    ]
    card_colors = [NAVY, TEAL, BLUE, GOLD]
    for index, ((label, value), color) in enumerate(zip(cards, card_colors)):
        axis = fig.add_subplot(grid[0, index])
        axis.set_facecolor(PALE)
        for spine in axis.spines.values():
            spine.set_color(LIGHT)
        axis.set_xticks([])
        axis.set_yticks([])
        axis.text(
            0.5,
            0.62,
            f"{int(value):,}",
            ha="center",
            va="center",
            fontsize=25,
            fontweight="bold",
            color=color,
        )
        axis.text(
            0.5,
            0.26,
            label,
            ha="center",
            va="center",
            fontsize=10.5,
            color=NAVY,
        )

    axis = fig.add_subplot(grid[1, :])
    preferred = [
        "GEO_COUNTRY_OA",
        "AFFILIATION_OA",
        "ORCID",
        "PROFILE_CLASSIFICATION",
        "GENDER",
    ]
    selected = coverage[coverage["FIELD"].isin(preferred)].copy()
    if selected.empty:
        selected = coverage.nlargest(5, "COVERAGE_PERCENT")
    selected["LABEL"] = (
        selected["FIELD"]
        .replace(
            {
                "GEO_COUNTRY_OA": "Affiliation country",
                "AFFILIATION_OA": "OpenAlex affiliation",
                "ORCID": "ORCID",
                "PROFILE_CLASSIFICATION": "Research profile",
                "GENDER": "Name-based gender",
            }
        )
        .astype(str)
    )
    selected = selected.sort_values("COVERAGE_PERCENT")
    bars = axis.barh(
        selected["LABEL"],
        selected["COVERAGE_PERCENT"],
        color=TEAL,
        height=0.58,
    )
    axis.set_xlim(0, 104)
    axis.set_xlabel("Populated author-paper records (%)")
    axis.set_title("Metadata coverage in the final master table", loc="left")
    axis.xaxis.set_major_locator(MaxNLocator(6))
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.tick_params(axis="y", length=0)
    for bar, percent in zip(bars, selected["COVERAGE_PERCENT"]):
        axis.text(
            min(float(percent) + 1.2, 100.5),
            bar.get_y() + bar.get_height() / 2,
            f"{percent:.1f}%",
            va="center",
            fontweight="bold",
            color=NAVY,
        )

    fig.suptitle(
        "Closed DOI stress-test corpus: complete DOI reconciliation",
        x=0.06,
        y=0.98,
        ha="left",
        fontsize=20,
        fontweight="bold",
        color=NAVY,
    )
    fig.text(
        0.06,
        0.02,
        "Author-paper records are not unique people. Coverage excludes pipeline missing-value sentinels.",
        color=SLATE,
        fontsize=9,
    )
    _save(fig, "01_corpus_overview", briefing_dir, analysis_dir)


def render_collaboration_composition(
    collaboration: pd.DataFrame,
    briefing_dir: Path,
    analysis_dir: Path,
) -> None:
    data = collaboration.sort_values("PAPERS")
    fig, axis = plt.subplots(figsize=(11.8, 6.8))
    colors = {
        "Africa-only known affiliations": TEAL,
        "Mixed Africa + outside": GOLD,
        "No African affiliation detected": NAVY,
        "Unknown affiliations only": SLATE,
    }
    bars = axis.barh(
        [_short_category(value) for value in data["CATEGORY"]],
        data["PAPERS"],
        color=[colors[value] for value in data["CATEGORY"]],
        height=0.62,
    )
    axis.set_title("Collaboration structure across papers", loc="left", color=NAVY)
    axis.set_xlabel("Papers (DOI-level classification)")
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.tick_params(axis="y", length=0)
    axis.xaxis.set_major_locator(MaxNLocator(integer=True))
    maximum = max(data["PAPERS"].max(), 1)
    axis.set_xlim(0, maximum * 1.24)
    for bar, (_, row) in zip(bars, data.iterrows()):
        axis.text(
            bar.get_width() + maximum * 0.025,
            bar.get_y() + bar.get_height() / 2,
            f"{int(row['PAPERS']):,}  |  {row['PERCENT']:.1f}%",
            va="center",
            fontweight="bold",
            color=NAVY,
        )
    fig.text(
        0.10,
        0.03,
        "Region is based on publication-time affiliation country, not nationality or origin.",
        color=SLATE,
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    _save(fig, "02_collaboration_composition", briefing_dir, analysis_dir)


def render_mixed_leadership(
    leadership: pd.DataFrame,
    briefing_dir: Path,
    analysis_dir: Path,
) -> None:
    pivot = leadership.pivot(
        index="ROLE", columns="LEADERSHIP_REGION", values="PERCENT"
    ).reindex(["First author", "Last author", "Corresponding author"])
    order = ["Africa only", "Outside Africa only", "Both regions", "Unknown only"]
    pivot = pivot.reindex(columns=order, fill_value=0)
    fig, axis = plt.subplots(figsize=(12.2, 6.7))
    left = np.zeros(len(pivot))
    colors = [TEAL, NAVY, GOLD, SLATE]
    for category, color in zip(order, colors):
        values = pivot[category].fillna(0).to_numpy()
        bars = axis.barh(
            pivot.index,
            values,
            left=left,
            color=color,
            label=category,
            height=0.58,
        )
        for bar, value in zip(bars, values):
            if value >= 7:
                axis.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:.1f}%",
                    ha="center",
                    va="center",
                    fontsize=9,
                    fontweight="bold",
                    color="white" if color != GOLD else NAVY,
                )
        left += values
    mixed_papers = int(leadership["MIXED_PAPERS"].max()) if len(leadership) else 0
    axis.set_xlim(0, 100)
    axis.set_xlabel("Mixed-collaboration papers (%)")
    axis.set_title(
        f"Leadership affiliation in mixed collaborations (N={mixed_papers:,} papers)",
        loc="left",
        color=NAVY,
    )
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.tick_params(axis="y", length=0)
    axis.legend(
        ncol=4,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        frameon=False,
    )
    fig.text(
        0.08,
        0.025,
        "A paper may have multiple corresponding authors; 'Both regions' retains that joint leadership signal.",
        color=SLATE,
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.09, 1, 1))
    _save(
        fig,
        "03_mixed_collaboration_leadership",
        briefing_dir,
        analysis_dir,
    )


def render_impact_gap(
    observations: pd.DataFrame,
    impact: pd.DataFrame,
    briefing_dir: Path,
    analysis_dir: Path,
) -> None:
    region_order = ["Africa", "Outside Africa"]
    values = [
        observations.loc[
            observations["AFFILIATION_REGION"].eq(region), "HINDEX_OA"
        ]
        .dropna()
        .to_numpy()
        for region in region_order
    ]
    combined = np.concatenate([value for value in values if len(value)])
    upper = max(float(np.quantile(combined, 0.99)), 1.0)
    fig, axis = plt.subplots(figsize=(11.8, 6.7))
    box = axis.boxplot(
        values,
        orientation="horizontal",
        tick_labels=["African affiliation", "Outside-African affiliation"],
        patch_artist=True,
        showfliers=False,
        widths=0.5,
        medianprops={"color": GOLD, "linewidth": 2.4},
        whiskerprops={"color": SLATE},
        capprops={"color": SLATE},
    )
    for patch, color in zip(box["boxes"], [TEAL, NAVY]):
        patch.set_facecolor(color)
        patch.set_alpha(0.9)
    rng = np.random.default_rng(197802)
    for position, (region_values, color) in enumerate(
        zip(values, [TEAL, NAVY]), start=1
    ):
        sample = (
            rng.choice(region_values, size=500, replace=False)
            if len(region_values) > 500
            else region_values
        )
        jitter = rng.normal(position, 0.055, len(sample))
        axis.scatter(
            np.clip(sample, 0, upper),
            jitter,
            s=10,
            alpha=0.16,
            color=color,
            edgecolors="none",
        )
    axis.set_xlim(0, upper * 1.08)
    axis.set_xlabel("OpenAlex H-index (axis limited at the 99th percentile)")
    axis.set_title(
        "Bibliometric impact differs by affiliation region",
        loc="left",
        color=NAVY,
    )
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.tick_params(axis="y", length=0)
    for position, region in enumerate(region_order, start=1):
        row = impact[impact["AFFILIATION_REGION"].eq(region)].iloc[0]
        axis.text(
            upper * 0.98,
            position + 0.24,
            (
                f"N={int(row['AUTHORS']):,}  |  median {row['HINDEX_MEDIAN']:.1f}  "
                f"(IQR {row['HINDEX_Q1']:.1f}-{row['HINDEX_Q3']:.1f})"
            ),
            ha="right",
            color=NAVY,
            fontsize=9.5,
            fontweight="bold",
        )
    fig.text(
        0.08,
        0.03,
        "One observation per author and affiliation region. Descriptive comparison; no causal inference.",
        color=SLATE,
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    _save(fig, "04_bibliometric_impact_gap", briefing_dir, analysis_dir)


def render_profile_composition(
    profiles: pd.DataFrame,
    briefing_dir: Path,
    analysis_dir: Path,
) -> None:
    totals = profiles.groupby("BASE_PROFILE")["AUTHORS"].sum().sort_values(
        ascending=False
    )
    keep = list(totals.head(6).index)
    data = profiles.copy()
    data["DISPLAY_PROFILE"] = np.where(
        data["BASE_PROFILE"].isin(keep), data["BASE_PROFILE"], "OTHER"
    )
    grouped = (
        data.groupby(["AFFILIATION_REGION", "DISPLAY_PROFILE"])["AUTHORS"]
        .sum()
        .reset_index()
    )
    grouped["PERCENT"] = grouped.groupby("AFFILIATION_REGION")["AUTHORS"].transform(
        lambda values: values / values.sum() * 100
    )
    pivot = grouped.pivot(
        index="AFFILIATION_REGION",
        columns="DISPLAY_PROFILE",
        values="PERCENT",
    ).fillna(0)
    regions = [region for region in ["Africa", "Outside Africa"] if region in pivot.index]
    categories = [category for category in keep if category in pivot.columns]
    if "OTHER" in pivot.columns:
        categories.append("OTHER")
    palette = [NAVY, TEAL, GOLD, BLUE, "#7A5195", "#EF8354", SLATE]
    fig, axis = plt.subplots(figsize=(12.6, 6.8))
    left = np.zeros(len(regions))
    region_totals = grouped.groupby("AFFILIATION_REGION")["AUTHORS"].sum()
    region_labels = [
        (
            "African affiliation"
            if region == "Africa"
            else "Outside-African affiliation"
        )
        + f" (N={int(region_totals[region]):,})"
        for region in regions
    ]
    for category, color in zip(categories, palette):
        values = pivot.loc[regions, category].to_numpy()
        bars = axis.barh(
            region_labels,
            values,
            left=left,
            height=0.58,
            color=color,
            label=category.replace("_", " ").title(),
        )
        for bar, value in zip(bars, values):
            if value >= 7:
                axis.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:.1f}%",
                    ha="center",
                    va="center",
                    fontsize=8.5,
                    fontweight="bold",
                    color="white" if color != GOLD else NAVY,
                )
        left += values
    axis.set_xlim(0, 100)
    axis.set_xlabel("Distinct author-region observations (%)")
    axis.set_title(
        "Research profile composition by affiliation region",
        loc="left",
        color=NAVY,
    )
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.tick_params(axis="y", length=0)
    axis.legend(
        ncol=3,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        frameon=False,
        fontsize=8.5,
    )
    fig.text(
        0.08,
        0.025,
        "Profiles are LLM-inferred from available publication metadata and require manual validation.",
        color=SLATE,
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.11, 1, 1))
    _save(
        fig,
        "05_research_profile_composition",
        briefing_dir,
        analysis_dir,
    )


def render_country_hindex_distribution(
    country_impact: pd.DataFrame,
    briefing_dir: Path,
    analysis_dir: Path,
) -> None:
    selected = country_impact.loc[
        country_impact["SELECTED_FOR_FIGURE"].eq(True)
    ].copy()
    fig, axes = plt.subplots(1, 2, figsize=(14.2, 7.3), sharex=True)
    regions = [
        ("Africa", "African affiliations", TEAL),
        ("Outside Africa", "Outside-African affiliations", NAVY),
    ]
    maximum = max(float(selected["HINDEX_Q3"].max()) if len(selected) else 0, 1)
    for axis, (region, title, color) in zip(axes, regions):
        data = selected[selected["AFFILIATION_REGION"].eq(region)].sort_values(
            ["HINDEX_MEDIAN", "COUNTRY"]
        )
        if data.empty:
            axis.text(
                0.5,
                0.5,
                "Insufficient eligible countries",
                ha="center",
                va="center",
                transform=axis.transAxes,
                color=SLATE,
            )
            axis.set_yticks([])
        else:
            positions = np.arange(len(data))
            axis.hlines(
                positions,
                data["HINDEX_Q1"],
                data["HINDEX_Q3"],
                color=color,
                linewidth=4,
                alpha=0.48,
            )
            axis.scatter(
                data["HINDEX_MEDIAN"],
                positions,
                s=72,
                color=color,
                edgecolor="white",
                linewidth=1.2,
                zorder=3,
            )
            axis.set_yticks(
                positions,
                [
                    f"{row.COUNTRY}  (N={int(row.AUTHORS):,})"
                    for row in data.itertuples()
                ],
            )
            for position, row in zip(positions, data.itertuples()):
                axis.text(
                    row.HINDEX_Q3 + maximum * 0.025,
                    position,
                    f"{row.HINDEX_MEDIAN:.1f}",
                    va="center",
                    color=NAVY,
                    fontsize=9,
                    fontweight="bold",
                )
        axis.set_title(title, loc="left", fontsize=14, color=NAVY)
        axis.set_xlim(0, maximum * 1.2)
        axis.grid(axis="x", color=LIGHT, linewidth=0.8)
        axis.spines[["top", "right", "left"]].set_visible(False)
        axis.tick_params(axis="y", length=0)
        axis.set_xlabel("OpenAlex H-index")

    fig.suptitle(
        "OpenAlex H-index distribution by affiliation country",
        x=0.07,
        y=0.98,
        ha="left",
        fontsize=19,
        fontweight="bold",
        color=NAVY,
    )
    fig.text(
        0.07,
        0.025,
        (
            "Point = median; line = interquartile range. One observation per author-country pair. "
            "Country denotes publication-time affiliation, not origin or nationality."
        ),
        color=SLATE,
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 0.94), w_pad=4)
    _save(
        fig,
        "06_country_hindex_distribution",
        briefing_dir,
        analysis_dir,
    )


def render_mixed_country_leadership(
    country_leadership: pd.DataFrame,
    briefing_dir: Path,
    analysis_dir: Path,
) -> None:
    data = country_leadership.loc[
        country_leadership["SELECTED_FOR_FIGURE"].eq(True)
    ].sort_values(["MIXED_PAPERS", "COUNTRY"], ascending=[False, True])
    fig, axis = plt.subplots(figsize=(11.8, 7.2))
    if data.empty:
        axis.text(
            0.5,
            0.5,
            "Insufficient eligible countries",
            ha="center",
            va="center",
            transform=axis.transAxes,
            color=SLATE,
        )
        axis.set_axis_off()
    else:
        columns = [
            "FIRST_AUTHOR_PERCENT",
            "LAST_AUTHOR_PERCENT",
            "CORRESPONDING_AUTHOR_PERCENT",
        ]
        matrix = data[columns].to_numpy(dtype=float)
        cmap = LinearSegmentedColormap.from_list(
            "leadership",
            [PALE, "#A8DADC", TEAL, NAVY],
        )
        image = axis.imshow(matrix, cmap=cmap, vmin=0, vmax=100, aspect="auto")
        axis.set_xticks(
            np.arange(3),
            ["First author", "Last author", "Corresponding author"],
        )
        axis.set_yticks(
            np.arange(len(data)),
            [
                f"{row.COUNTRY}  (N={int(row.MIXED_PAPERS):,})"
                for row in data.itertuples()
            ],
        )
        axis.tick_params(axis="both", length=0)
        for row_index in range(matrix.shape[0]):
            for column_index in range(matrix.shape[1]):
                value = matrix[row_index, column_index]
                axis.text(
                    column_index,
                    row_index,
                    f"{value:.1f}%",
                    ha="center",
                    va="center",
                    color="white" if value >= 45 else NAVY,
                    fontsize=10,
                    fontweight="bold",
                )
        colorbar = fig.colorbar(image, ax=axis, pad=0.025, fraction=0.04)
        colorbar.set_label("Country-participating mixed papers (%)")
        colorbar.outline.set_visible(False)
        axis.spines[["top", "right", "bottom", "left"]].set_visible(False)

    axis.set_title(
        "African-country leadership participation in mixed collaborations",
        loc="left",
        color=NAVY,
        pad=18,
    )
    fig.text(
        0.10,
        0.025,
        (
            "Denominator: mixed-collaboration papers with at least one author affiliated with the country. "
            "Role percentages are independent and may overlap."
        ),
        color=SLATE,
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    _save(
        fig,
        "07_mixed_collaboration_country_leadership",
        briefing_dir,
        analysis_dir,
    )


def render_doi_reconciliation(
    reconciliation: pd.DataFrame,
    validation_dir: Path,
) -> None:
    validation_dir.mkdir(parents=True, exist_ok=True)
    total = int(len(reconciliation))
    present = int(reconciliation["STATUS"].eq("present").sum())
    missing = int(reconciliation["STATUS"].eq("missing").sum())
    fig, axis = plt.subplots(figsize=(8.8, 5.4))
    labels = ["Input DOI values", "Present in master", "Missing"]
    values = [total, present, missing]
    bars = axis.bar(labels, values, color=[NAVY, TEAL, RED], width=0.62)
    axis.set_title("DOI reconciliation", loc="left", color=NAVY)
    axis.set_ylabel("Unique DOI values")
    axis.spines[["top", "right"]].set_visible(False)
    axis.yaxis.set_major_locator(MaxNLocator(integer=True))
    for bar, value in zip(bars, values):
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(total * 0.02, 0.5),
            f"{value:,}",
            ha="center",
            fontweight="bold",
            color=NAVY,
        )
    axis.set_ylim(0, max(total * 1.12, 1))
    fig.tight_layout()
    fig.savefig(
        validation_dir / "01_doi_reconciliation.png",
        dpi=240,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)


def render_all_figures(
    summary: dict[str, object],
    collaboration: pd.DataFrame,
    leadership: pd.DataFrame,
    observations: pd.DataFrame,
    impact: pd.DataFrame,
    profiles: pd.DataFrame,
    coverage: pd.DataFrame,
    reconciliation: pd.DataFrame,
    country_impact: pd.DataFrame,
    country_leadership: pd.DataFrame,
    figure_root: Path,
) -> None:
    """Render all briefing, analysis, and validation figures."""
    _configure_style()
    briefing_dir = figure_root / "briefing"
    analysis_dir = figure_root / "analysis"
    render_corpus_overview(summary, coverage, briefing_dir, analysis_dir)
    render_collaboration_composition(
        collaboration, briefing_dir, analysis_dir
    )
    render_mixed_leadership(leadership, briefing_dir, analysis_dir)
    render_impact_gap(observations, impact, briefing_dir, analysis_dir)
    render_profile_composition(profiles, briefing_dir, analysis_dir)
    render_country_hindex_distribution(
        country_impact, briefing_dir, analysis_dir
    )
    render_mixed_country_leadership(
        country_leadership, briefing_dir, analysis_dir
    )
    render_doi_reconciliation(reconciliation, figure_root / "validation")
