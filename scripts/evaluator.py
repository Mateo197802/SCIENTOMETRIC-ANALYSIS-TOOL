"""
SENT Evaluator - Scientometric Analysis Tool
Compares machine-extracted data (MASTER_AUTHOR_TABLE) against raw web data (OpenAlex JSON).
Generates modular outputs and publication-quality comparative graphs.
"""
import os
import pandas as pd
import requests
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ─── PATHS ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR      = os.path.join(BASE_DIR, "data")
MAQUINA_DIR   = os.path.join(DATA_DIR, "output", "csv")
WEB_DIR       = os.path.join(DATA_DIR, "output_web")
ASSETS_DIR    = os.path.join(BASE_DIR, "assets")
GRAFICAS_DIR  = os.path.join(ASSETS_DIR, "figures")
MASTER_CSV    = os.path.join(MAQUINA_DIR, "MASTER_AUTHOR_TABLE.csv")

for d in [MAQUINA_DIR, WEB_DIR, GRAFICAS_DIR]:
    os.makedirs(d, exist_ok=True)

# ─── STYLE ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "figure.facecolor": "#FAFAFA",
    "axes.facecolor": "#FAFAFA",
    "axes.edgecolor": "#CCCCCC",
    "grid.color": "#E0E0E0",
    "grid.linestyle": "--",
    "grid.alpha": 0.7,
})

PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860"]
DOI_LABELS = {
    "10.1080/0142159X.2026.2653205": "Celi 1\n(Med. Teacher 2026)",
    "10.1371/journal.pdig.0001194":  "Celi 2\n(PLOS Dig. Health 2026)",
    "10.1038/sdata.2016.35":         "Celi 3\n(MIMIC-III 2016)",
    "10.1038/nature12160":           "Random 1\n(Nature 2013)",
    "10.1016/j.cell.2004.12.018":   "Random 2\n(Cell 2005)",
}

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def fetch_openalex(doi):
    """Fetch raw data from OpenAlex for a single DOI."""
    url = f"https://api.openalex.org/works/doi:{doi}"
    try:
        resp = requests.get(url, params={"mailto": "test@example.com"}, timeout=15)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"  [WARN] Could not fetch {doi}: {e}")
    return None


def normalize(name):
    """Normalize author name for fuzzy matching."""
    if not isinstance(name, str):
        return ""
    return " ".join(name.lower().strip().split())


def match_authors(machine_names, web_names):
    """Return (matched, only_machine, only_web) sets."""
    m_norm = {normalize(n): n for n in machine_names}
    w_norm = {normalize(n): n for n in web_names}
    matched = set(m_norm.keys()) & set(w_norm.keys())
    only_m  = set(m_norm.keys()) - set(w_norm.keys())
    only_w  = set(w_norm.keys()) - set(m_norm.keys())
    return matched, only_m, only_w


def field_completeness(df, fields):
    """Return dict {field: pct_filled}  (0-100)."""
    result = {}
    for f in fields:
        if f not in df.columns:
            result[f] = 0.0
            continue
        col = df[f]
        empty = col.isna().sum() + (col.astype(str).isin(["No data", "UNKNOWN", "NO_ORCID", "NOT_FOUND", "SKIP", "NOT_FOUND_IN_PM", "NOT_FOUND_IN_SC", "NOT_FOUND_IN_SS", "NOT_INDEXED_IN_GS", "nan", ""])).sum()
        result[f] = round(((len(col) - empty) / len(col)) * 100, 1) if len(col) > 0 else 0.0
    return result


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    if not os.path.exists(MASTER_CSV):
        print(f"ERROR: {MASTER_CSV} not found. Run main.py first.")
        return

    df = pd.read_csv(MASTER_CSV)
    df.to_csv(os.path.join(MAQUINA_DIR, "MASTER_AUTHOR_TABLE.csv"), index=False)
    dois = df["DOI"].unique().tolist()

    print(f"{'='*70}")
    print(f" SCIENTOMETRIC ANALYSIS TOOL -- EVALUATION REPORT")
    print(f" Total records: {len(df)} authors across {len(dois)} DOIs")
    print(f"{'='*70}\n")

    # Collect stats per DOI
    stats = []
    all_field_stats = []

    CORE_FIELDS = [
        "AUTHOR_NAME", "AFFILIATION_OA", "GEO_COUNTRY_OA", "ORCID",
        "WORKS_COUNT_OA", "CITATIONS_OA", "HINDEX_OA",
        "PMID_PM", "MESH_PM", "AUTHOR_ID_SC",
        "INFLUENTIAL_CITATIONS_SS", "AUTHOR_ID_SS",
        "INTERESTS_GS", "ORCID_EMPLOYMENT", "GENDER", "PROFILE_CLASSIFICATION"
    ]

    for doi in dois:
        doi_safe = str(doi).replace("/", "_")
        doi_df = df[df["DOI"] == doi].copy()
        doi_df.to_csv(os.path.join(MAQUINA_DIR, f"{doi_safe}_maquina.csv"), index=False)

        # Fetch web
        web_data = fetch_openalex(doi)
        if web_data:
            with open(os.path.join(WEB_DIR, f"{doi_safe}_web.json"), "w", encoding="utf-8") as f:
                json.dump(web_data, f, indent=2, ensure_ascii=False)

        web_authors = [a["author"]["display_name"] for a in web_data.get("authorships", [])] if web_data else []
        machine_authors = doi_df["AUTHOR_NAME"].tolist()

        matched, only_m, only_w = match_authors(machine_authors, web_authors)

        # Field completeness
        fc = field_completeness(doi_df, CORE_FIELDS)

        label = DOI_LABELS.get(doi, doi)
        author_accuracy = (len(matched) / len(web_authors) * 100) if web_authors else 0
        avg_completeness = np.mean(list(fc.values()))

        stat = {
            "DOI": doi,
            "Label": label.replace("\n", " "),
            "Expected_Authors": len(web_authors),
            "Extracted_Authors": len(machine_authors),
            "Matched_Authors": len(matched),
            "Author_Accuracy_Pct": round(author_accuracy, 1),
            "Avg_Field_Completeness_Pct": round(avg_completeness, 1),
        }
        stats.append(stat)
        all_field_stats.append({"DOI": doi, **fc})

        # Console report
        print(f"  DOI: {doi}")
        print(f"    Title  : {doi_df['PAPER_TITLE'].iloc[0] if len(doi_df) > 0 else 'N/A'}")
        print(f"    Authors: Machine={len(machine_authors)}  Web={len(web_authors)}  Matched={len(matched)}")
        print(f"    Accuracy (author match): {author_accuracy:.1f}%")
        print(f"    Avg field completeness : {avg_completeness:.1f}%")
        if only_m:
            print(f"    [!] Only in Machine: {only_m}")
        if only_w:
            print(f"    [!] Only in Web:     {only_w}")
        print()

    stats_df = pd.DataFrame(stats)
    field_df = pd.DataFrame(all_field_stats)
    stats_df.to_csv(os.path.join(DATA_DIR, "evaluation_summary.csv"), index=False)
    field_df.to_csv(os.path.join(DATA_DIR, "field_completeness_detail.csv"), index=False)

    # ─── GRAPH 1: Author Accuracy (Grouped Bar) ────────────────────────────
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(stats_df))
    w = 0.28

    bars1 = ax.bar(x - w, stats_df["Expected_Authors"], w, label="Expected (Web)", color="#4C72B0", edgecolor="white", linewidth=0.5)
    bars2 = ax.bar(x,     stats_df["Extracted_Authors"], w, label="Extracted (Machine)", color="#DD8452", edgecolor="white", linewidth=0.5)
    bars3 = ax.bar(x + w, stats_df["Matched_Authors"],   w, label="Matched",             color="#55A868", edgecolor="white", linewidth=0.5)

    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.15, str(int(h)), ha="center", va="bottom", fontsize=9, fontweight="bold")

    labels = [DOI_LABELS.get(d, d) for d in stats_df["DOI"]]
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Number of Authors")
    ax.set_title("Author Extraction Accuracy: Web vs Machine vs Matched")
    ax.legend(loc="upper right", framealpha=0.9)
    ax.grid(axis="y")
    ax.set_ylim(0, stats_df["Expected_Authors"].max() + 3)
    fig.tight_layout()
    fig.savefig(os.path.join(GRAFICAS_DIR, "01_accuracy_authors.png"), dpi=180)
    plt.close(fig)
    print("[OK] Graph saved: 01_accuracy_authors.png")

    # ─── GRAPH 2: Author Match % per DOI (Horizontal bar) ──────────────────
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#55A868" if v >= 90 else "#DD8452" if v >= 70 else "#C44E52" for v in stats_df["Author_Accuracy_Pct"]]
    bars = ax.barh(labels, stats_df["Author_Accuracy_Pct"], color=colors, edgecolor="white", height=0.55)
    for bar, val in zip(bars, stats_df["Author_Accuracy_Pct"]):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f"{val}%", va="center", fontsize=10, fontweight="bold")
    ax.set_xlim(0, 110)
    ax.set_xlabel("Author Match Accuracy (%)")
    ax.set_title("Per-DOI Author Matching Accuracy")
    ax.axvline(100, color="#999", ls="--", lw=0.8)
    ax.grid(axis="x")
    fig.tight_layout()
    fig.savefig(os.path.join(GRAFICAS_DIR, "02_accuracy_percentage.png"), dpi=180)
    plt.close(fig)
    print("[OK] Graph saved: 02_accuracy_percentage.png")

    # ─── GRAPH 3: Field Completeness Heatmap ──────────────────────────────
    heatmap_data = field_df.set_index("DOI")[CORE_FIELDS]
    heatmap_data.index = [DOI_LABELS.get(d, d).replace("\n", " ") for d in heatmap_data.index]

    fig, ax = plt.subplots(figsize=(14, 5))
    im = ax.imshow(heatmap_data.values, cmap="RdYlGn", aspect="auto", vmin=0, vmax=100)
    ax.set_xticks(np.arange(len(CORE_FIELDS)))
    ax.set_xticklabels([f.replace("_", "\n") for f in CORE_FIELDS], fontsize=7, rotation=45, ha="right")
    ax.set_yticks(np.arange(len(heatmap_data)))
    ax.set_yticklabels(heatmap_data.index, fontsize=9)
    for i in range(len(heatmap_data)):
        for j in range(len(CORE_FIELDS)):
            val = heatmap_data.values[i, j]
            color = "white" if val < 40 else "black"
            ax.text(j, i, f"{val:.0f}%", ha="center", va="center", fontsize=7, color=color, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Completeness %")
    ax.set_title("Field-Level Data Completeness Heatmap (per DOI)")
    fig.tight_layout()
    fig.savefig(os.path.join(GRAFICAS_DIR, "03_field_completeness_heatmap.png"), dpi=180)
    plt.close(fig)
    print("[OK] Graph saved: 03_field_completeness_heatmap.png")

    # ─── GRAPH 4: Radar Chart — Avg per source ────────────────────────────
    source_groups = {
        "OpenAlex":         ["AUTHOR_NAME", "AFFILIATION_OA", "GEO_COUNTRY_OA", "ORCID", "WORKS_COUNT_OA", "CITATIONS_OA", "HINDEX_OA"],
        "PubMed":           ["PMID_PM", "MESH_PM"],
        "Scopus":           ["AUTHOR_ID_SC"],
        "Semantic Scholar": ["INFLUENTIAL_CITATIONS_SS", "AUTHOR_ID_SS"],
        "Google Scholar":   ["INTERESTS_GS"],
        "ORCID":            ["ORCID_EMPLOYMENT"],
        "Azure GPT-4o":     ["GENDER", "PROFILE_CLASSIFICATION"],
    }
    avg_by_source = {}
    for source, fields in source_groups.items():
        vals = [field_df[f].mean() for f in fields if f in field_df.columns]
        avg_by_source[source] = np.mean(vals) if vals else 0

    categories = list(avg_by_source.keys())
    values = list(avg_by_source.values())
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color="#4C72B0", alpha=0.25)
    ax.plot(angles, values, color="#4C72B0", linewidth=2, marker="o", markersize=6)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylim(0, 105)
    ax.set_title("Data Source Coverage (Avg. Completeness %)", y=1.08, fontsize=13, fontweight="bold")
    for angle, val, cat in zip(angles[:-1], values[:-1], categories):
        ax.text(angle, val + 5, f"{val:.0f}%", ha="center", fontsize=8, fontweight="bold", color="#333")
    fig.tight_layout()
    fig.savefig(os.path.join(GRAFICAS_DIR, "04_source_coverage_radar.png"), dpi=180)
    plt.close(fig)
    print("[OK] Graph saved: 04_source_coverage_radar.png")

    # ─── GRAPH 5: Overall Score Summary ───────────────────────────────────
    overall_author_acc = stats_df["Author_Accuracy_Pct"].mean()
    overall_completeness = stats_df["Avg_Field_Completeness_Pct"].mean()
    overall_score = (overall_author_acc * 0.5 + overall_completeness * 0.5)

    fig, ax = plt.subplots(figsize=(8, 4))
    metrics = ["Author Match\nAccuracy", "Field\nCompleteness", "Overall\nScore"]
    vals = [overall_author_acc, overall_completeness, overall_score]
    colors = ["#4C72B0", "#55A868", "#DD8452"]
    bars = ax.barh(metrics, vals, color=colors, edgecolor="white", height=0.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height()/2, f"{val:.1f}%", va="center", fontsize=12, fontweight="bold")
    ax.set_xlim(0, 115)
    ax.set_title("Scientometric Tool - Overall Performance Score")
    ax.axvline(100, color="#999", ls="--", lw=0.8)
    ax.grid(axis="x")
    fig.tight_layout()
    fig.savefig(os.path.join(GRAFICAS_DIR, "05_overall_score.png"), dpi=180)
    plt.close(fig)
    print("[OK] Graph saved: 05_overall_score.png")

    # ─── FINAL SUMMARY ──────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f" FINAL EVALUATION SUMMARY")
    print(f"{'='*70}")
    print(f"  DOIs processed            : {len(dois)}")
    print(f"  Total authors extracted    : {len(df)}")
    print(f"  Author Match Accuracy (avg): {overall_author_acc:.1f}%")
    print(f"  Field Completeness (avg)   : {overall_completeness:.1f}%")
    print(f"  * OVERALL SCORE            : {overall_score:.1f}%")
    print(f"{'='*70}")
    print(f"\nAll outputs saved to: {BASE_DIR}")
    print(f"  |-- data/output/       ({len(os.listdir(MAQUINA_DIR))} files)")
    print(f"  |-- data/output_web/   ({len(os.listdir(WEB_DIR))} files)")
    print(f"  +-- assets/figures/    ({len(os.listdir(GRAFICAS_DIR))} graphs)")


if __name__ == "__main__":
    main()
