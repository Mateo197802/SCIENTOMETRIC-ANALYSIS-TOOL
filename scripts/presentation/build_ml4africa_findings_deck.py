"""Build an HTML presentation for the ML4Africa scientometric findings."""

from __future__ import annotations

import base64
import csv
import html
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = BASE_DIR / "data" / "analysis"
ASSET_FIGURE_DIR = BASE_DIR / "assets" / "figures" / "analytics"
OUTPUT_DIR = BASE_DIR / "output" / "presentations"
OUTPUT_PATH = OUTPUT_DIR / "ML4Africa_scientometric_findings_presentation.html"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def image_data_uri(path: Path) -> str:
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    suffix = path.suffix.lower().lstrip(".")
    mime = "image/svg+xml" if suffix == "svg" else f"image/{suffix}"
    return f"data:{mime};base64,{payload}"


def pct(value: float) -> str:
    return f"{value:.1f}%"


def number(value: float | int | str) -> str:
    if isinstance(value, str):
        value = float(value)
    if float(value).is_integer():
        return f"{int(value):,}"
    return f"{value:,.1f}"


def horizontal_bars(rows: list[dict[str, object]], value_key: str = "value") -> str:
    max_value = max(float(row[value_key]) for row in rows) or 1
    parts = ['<div class="bar-list">']
    for row in rows:
        value = float(row[value_key])
        width = value / max_value * 100
        label = html.escape(str(row["label"]))
        value_label = html.escape(str(row["value_label"]))
        parts.append(
            f"""
            <div class="bar-row">
              <div class="bar-label">{label}</div>
              <div class="bar-track"><div class="bar-fill" style="width:{width:.2f}%"></div></div>
              <div class="bar-value">{value_label}</div>
            </div>
            """
        )
    parts.append("</div>")
    return "\n".join(parts)


def leadership_matrix(rows: list[dict[str, str]]) -> str:
    roles = ["First author", "Last author", "Corresponding author"]
    categories = ["Africa only", "Outside Africa only", "Both regions", "Unknown only"]
    colors = {
        "Africa only": "#0B7A75",
        "Outside Africa only": "#17324D",
        "Both regions": "#A3BEFA",
        "Unknown only": "#D7DBE7",
    }
    by_role = {
        role: [row for row in rows if row["ROLE"] == role]
        for role in roles
    }
    parts = ['<div class="stacked-wrapper">']
    for role in roles:
        parts.append(f'<div class="stacked-row"><div class="stacked-role">{role}</div>')
        parts.append('<div class="stacked-bar">')
        for category in categories:
            match = next(
                row for row in by_role[role] if row["LEADERSHIP_REGION"] == category
            )
            value = float(match["PERCENT"])
            label = f"{value:.1f}%"
            color = colors[category]
            parts.append(
                f'<div class="stack-segment" style="width:{value:.2f}%;background:{color}" '
                f'title="{html.escape(category)} {label}">{label if value >= 6 else ""}</div>'
            )
        parts.append("</div></div>")
    parts.append(
        """
        <div class="legend">
          <span><b style="background:#0B7A75"></b>Africa only</span>
          <span><b style="background:#17324D"></b>Outside Africa only</span>
          <span><b style="background:#A3BEFA"></b>Both regions</span>
          <span><b style="background:#D7DBE7"></b>Unknown only</span>
        </div>
        """
    )
    parts.append("</div>")
    return "\n".join(parts)


def impact_cards(rows: list[dict[str, str]]) -> str:
    ordered = sorted(rows, key=lambda row: row["AFFILIATION_REGION"] == "Africa")
    cards = []
    for row in ordered:
        cards.append(
            f"""
            <div class="impact-card">
              <div class="impact-region">{html.escape(row["AFFILIATION_REGION"])}</div>
              <div class="impact-grid">
                <div><strong>{number(row["AUTHORS"])}</strong><span>authors</span></div>
                <div><strong>{number(row["HINDEX_MEDIAN"])}</strong><span>median H-index</span></div>
                <div><strong>{number(row["CITATIONS_MEDIAN"])}</strong><span>median citations</span></div>
                <div><strong>{number(row["WORKS_MEDIAN"])}</strong><span>median works</span></div>
              </div>
              <p>IQR H-index: {html.escape(row["HINDEX_Q1"])}-{html.escape(row["HINDEX_Q3"])}</p>
            </div>
            """
        )
    return '<div class="impact-cards">' + "\n".join(cards) + "</div>"


def coverage_grid(rows: list[dict[str, str]]) -> str:
    wanted = [
        "PAPER_TITLE",
        "DOI",
        "AUTHOR_POS_OA",
        "AFFILIATION_OA",
        "GEO_COUNTRY_OA",
        "AUTHOR_ID_OA",
        "ORCID",
        "GENDER",
        "PROFILE_CLASSIFICATION",
    ]
    labels = {
        "PAPER_TITLE": "Title",
        "DOI": "DOI",
        "AUTHOR_POS_OA": "Authorship position",
        "AFFILIATION_OA": "Affiliation",
        "GEO_COUNTRY_OA": "Affiliation country",
        "AUTHOR_ID_OA": "OpenAlex author ID",
        "ORCID": "ORCID",
        "GENDER": "Name-inferred gender",
        "PROFILE_CLASSIFICATION": "LLM profile",
    }
    row_map = {row["FIELD"]: row for row in rows}
    cards = []
    for key in wanted:
        row = row_map[key]
        coverage = float(row["COVERAGE_PERCENT"])
        cards.append(
            f"""
            <div class="coverage-card">
              <strong>{coverage:.1f}%</strong>
              <span>{html.escape(labels[key])}</span>
            </div>
            """
        )
    return '<div class="coverage-grid">' + "\n".join(cards) + "</div>"


def slide(kicker: str, title: str, body: str, theme: str = "") -> str:
    return f"""
    <section class="slide {theme}">
      <div class="kicker">{html.escape(kicker)}</div>
      <h2>{html.escape(title)}</h2>
      {body}
      <footer>ML4Africa Scientometric Analysis Tool | Closed DOI corpus analysis</footer>
    </section>
    """


def build_html() -> str:
    summary = json.loads((ANALYSIS_DIR / "analysis_summary.json").read_text(encoding="utf-8"))
    collaboration = summary["collaboration_composition"]
    leadership = read_csv(ANALYSIS_DIR / "mixed_leadership.csv")
    impact = read_csv(ANALYSIS_DIR / "impact_summary.csv")
    coverage = read_csv(ANALYSIS_DIR / "field_coverage.csv")

    pipeline_image = image_data_uri(
        ASSET_FIGURE_DIR / "01_scientometric_analysis_workflow.png"
    )

    collaboration_bars = horizontal_bars(
        [
            {
                "label": row["CATEGORY"],
                "value": row["PERCENT"],
                "value_label": f'{row["PAPERS"]:,} papers | {pct(row["PERCENT"])}',
            }
            for row in collaboration
        ]
    )

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ML4Africa Scientometric Findings</title>
  <style>
    :root {{
      --navy: #17324D;
      --ink: #102A43;
      --teal: #0B7A75;
      --muted: #667085;
      --paper: #F7F7F3;
      --panel: #FFFFFF;
      --line: #D8DEE9;
      --blue-light: #EAF1FE;
      --teal-light: #EAF7F5;
      --gold: #FFE15B;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: #111827;
      color: var(--ink);
      font-family: "Aptos", "Segoe UI", Arial, sans-serif;
    }}
    .deck {{
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      position: relative;
    }}
    .slide {{
      width: 100vw;
      height: 100vh;
      padding: 5.2vh 6vw 6.5vh;
      background:
        radial-gradient(circle at 88% 12%, rgba(11,122,117,.14), transparent 26%),
        linear-gradient(135deg, #FCFCFD, var(--paper));
      display: none;
      position: absolute;
      inset: 0;
    }}
    .slide.active {{ display: block; }}
    .cover {{
      background:
        radial-gradient(circle at 78% 20%, rgba(255,225,91,.22), transparent 28%),
        linear-gradient(135deg, #071B36, #17324D 55%, #0B7A75);
      color: white;
    }}
    .cover h1 {{
      font-family: Georgia, "Times New Roman", serif;
      font-size: clamp(46px, 6vw, 84px);
      line-height: .98;
      margin: 10vh 0 3vh;
      max-width: 1040px;
    }}
    .cover .subtitle {{
      font-size: clamp(22px, 2vw, 34px);
      color: rgba(255,255,255,.78);
      max-width: 980px;
      line-height: 1.32;
    }}
    .kicker {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      color: var(--teal);
      font-size: 14px;
      letter-spacing: .14em;
      text-transform: uppercase;
      font-weight: 800;
      margin-bottom: 18px;
    }}
    .kicker::before {{
      content: "";
      width: 28px;
      height: 3px;
      background: var(--teal);
      display: inline-block;
    }}
    h2 {{
      font-family: Georgia, "Times New Roman", serif;
      color: var(--navy);
      font-size: clamp(34px, 4.5vw, 60px);
      line-height: 1.05;
      margin: 0 0 26px;
      max-width: 1100px;
    }}
    .two-col {{
      display: grid;
      grid-template-columns: 1.1fr .9fr;
      gap: 38px;
      align-items: center;
    }}
    .three-col {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
    }}
    .metric-rail {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-top: 8vh;
    }}
    .metric-card, .callout, .impact-card, .coverage-card {{
      background: rgba(255,255,255,.86);
      border: 1px solid var(--line);
      border-radius: 22px;
      padding: 26px;
      box-shadow: 0 18px 42px rgba(16,42,67,.08);
    }}
    .cover .metric-card {{
      background: rgba(255,255,255,.12);
      border-color: rgba(255,255,255,.2);
      box-shadow: none;
    }}
    .metric-card strong {{
      display: block;
      font-size: clamp(38px, 5vw, 70px);
      color: var(--teal);
      line-height: .95;
    }}
    .cover .metric-card strong {{ color: white; }}
    .metric-card span {{
      display: block;
      margin-top: 12px;
      font-size: 18px;
      color: var(--muted);
      line-height: 1.25;
    }}
    .cover .metric-card span {{ color: rgba(255,255,255,.72); }}
    .claim {{
      font-size: clamp(22px, 2.4vw, 34px);
      line-height: 1.25;
      color: var(--ink);
      max-width: 1060px;
    }}
    .muted {{ color: var(--muted); }}
    .proof-image {{
      width: 100%;
      max-height: 62vh;
      object-fit: contain;
      background: white;
      border: 1px solid var(--line);
      border-radius: 20px;
      padding: 12px;
    }}
    .proof-image.tight {{ max-height: 56vh; }}
    .bar-list {{ display: grid; gap: 19px; }}
    .bar-row {{
      display: grid;
      grid-template-columns: 250px 1fr 180px;
      align-items: center;
      gap: 16px;
      font-size: 18px;
    }}
    .bar-label {{ font-weight: 700; color: var(--navy); }}
    .bar-track {{
      height: 28px;
      border-radius: 999px;
      background: #EEF2F7;
      overflow: hidden;
      border: 1px solid #D7DBE7;
    }}
    .bar-fill {{
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--teal), #2E4780);
    }}
    .bar-value {{
      font-family: Consolas, "SF Mono", monospace;
      color: var(--ink);
      font-size: 16px;
    }}
    .stacked-wrapper {{ display: grid; gap: 20px; }}
    .stacked-row {{
      display: grid;
      grid-template-columns: 210px 1fr;
      align-items: center;
      gap: 18px;
    }}
    .stacked-role {{ font-size: 20px; font-weight: 800; color: var(--navy); }}
    .stacked-bar {{
      display: flex;
      height: 48px;
      overflow: hidden;
      border-radius: 15px;
      border: 1px solid var(--line);
      background: white;
    }}
    .stack-segment {{
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 15px;
    }}
    .legend {{
      display: flex;
      gap: 22px;
      flex-wrap: wrap;
      margin-left: 228px;
      color: var(--muted);
      font-size: 15px;
    }}
    .legend span {{ display: inline-flex; align-items: center; gap: 8px; }}
    .legend b {{
      width: 18px;
      height: 18px;
      border-radius: 4px;
      display: inline-block;
      border: 1px solid rgba(0,0,0,.1);
    }}
    .impact-cards {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 26px;
    }}
    .impact-region {{
      color: var(--teal);
      text-transform: uppercase;
      font-weight: 900;
      letter-spacing: .08em;
      margin-bottom: 18px;
    }}
    .impact-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 18px;
    }}
    .impact-grid strong {{
      display: block;
      font-size: 42px;
      color: var(--navy);
      line-height: 1;
    }}
    .impact-grid span {{
      color: var(--muted);
      font-size: 15px;
    }}
    .impact-card p {{ color: var(--muted); font-size: 16px; margin-bottom: 0; }}
    .coverage-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }}
    .coverage-card strong {{
      display: block;
      font-size: 36px;
      color: var(--teal);
    }}
    .coverage-card span {{
      display: block;
      margin-top: 8px;
      color: var(--navy);
      font-weight: 700;
    }}
    ul.big-list {{
      font-size: clamp(21px, 2vw, 30px);
      line-height: 1.35;
      margin: 0;
      padding-left: 30px;
    }}
    ul.big-list li {{ margin-bottom: 16px; }}
    .step-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 18px;
    }}
    .step {{
      background: white;
      border-left: 7px solid var(--teal);
      border-radius: 18px;
      padding: 24px;
      border-top: 1px solid var(--line);
      border-right: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
    }}
    .step strong {{ color: var(--navy); font-size: 22px; }}
    .step p {{ color: var(--muted); font-size: 17px; line-height: 1.35; margin-bottom: 0; }}
    .source-note {{
      margin-top: 22px;
      color: var(--muted);
      font-size: 15px;
      line-height: 1.35;
    }}
    footer {{
      position: absolute;
      left: 6vw;
      bottom: 3.4vh;
      color: #98A2B3;
      font-size: 12px;
      letter-spacing: .02em;
    }}
    .nav {{
      position: fixed;
      right: 24px;
      bottom: 20px;
      z-index: 10;
      display: flex;
      align-items: center;
      gap: 10px;
      color: white;
      font-size: 14px;
      font-family: Consolas, monospace;
    }}
    .nav button {{
      background: rgba(255,255,255,.12);
      color: white;
      border: 1px solid rgba(255,255,255,.22);
      border-radius: 10px;
      padding: 9px 12px;
      cursor: pointer;
    }}
    @media print {{
      body, .deck {{ background: white; height: auto; overflow: visible; }}
      .slide {{ display: block !important; position: relative; page-break-after: always; width: 1280px; height: 720px; }}
      .nav {{ display: none; }}
    }}
  </style>
</head>
<body>
  <main class="deck">
    <section class="slide cover active">
      <div class="kicker" style="color:#FFE15B">ML4Africa | Scientometrics</div>
      <h1>Geographic patterns of scientific leadership and bibliometric impact</h1>
      <p class="subtitle">A closed-corpus analysis of machine-learning-for-health research involving African affiliations.</p>
      <div class="metric-rail">
        <div class="metric-card"><strong>{summary["input_dois"]:,}</strong><span>DOI values processed</span></div>
        <div class="metric-card"><strong>{summary["author_paper_records"]:,}</strong><span>author-paper records</span></div>
        <div class="metric-card"><strong>{summary["distinct_openalex_author_ids"]:,}</strong><span>distinct valid OpenAlex author IDs</span></div>
      </div>
      <footer style="color:rgba(255,255,255,.55)">Prepared from committed analysis outputs | {OUTPUT_PATH.name}</footer>
    </section>

    {slide(
        "Core Finding",
        "The full closed corpus was reconciled into an author-level evidence base.",
        f'''
        <div class="three-col">
          <div class="metric-card"><strong>{summary["input_dois"]:,}</strong><span>input DOIs</span></div>
          <div class="metric-card"><strong>{summary["output_dois"]:,}</strong><span>DOIs present in the final output</span></div>
          <div class="metric-card"><strong>0</strong><span>missing DOI values after reconciliation</span></div>
        </div>
        <p class="claim" style="margin-top:34px">The analysis starts from a fixed denominator, not a search-derived sample. This makes the findings auditable for the supplied ML4Africa corpus, but not automatically generalizable to the full field.</p>
        <p class="source-note">Source: data/analysis/analysis_summary.json and doi_reconciliation.csv.</p>
        '''
    )}

    {slide(
        "Workflow",
        "The tool expanded each DOI into paper, author, affiliation, identifier and impact layers.",
        f'''
        <img class="proof-image" src="{pipeline_image}" alt="Scientometric workflow diagram">
        <p class="source-note">Executed sources: OpenAlex, PubMed, Semantic Scholar, ORCID, Genderize and Azure OpenAI. Scopus and Google Scholar were implemented but disabled for the completed run.</p>
        '''
    )}

    {slide(
        "Corpus Composition",
        "Africa-only production and mixed international collaboration are both central in the corpus.",
        f'''
        <div class="two-col">
          <div>{collaboration_bars}</div>
          <div class="callout">
            <p class="claim"><strong>89.2%</strong> of papers were either Africa-only or mixed Africa/outside-Africa collaborations.</p>
            <p class="muted">This is a publication-time affiliation classification. It does not measure nationality, origin, study site or data origin.</p>
          </div>
        </div>
        <p class="source-note">Denominator: {summary["input_dois"]:,} DOI-level papers.</p>
        '''
    )}

    {slide(
        "Byline Leadership",
        "Mixed collaborations show role-specific leadership patterns rather than a single uniform signal.",
        f'''
        {leadership_matrix(leadership)}
        <div class="two-col" style="margin-top:28px">
          <div class="callout"><strong>Last authorship</strong><p class="muted">African-affiliated last authors appear near parity: 49.9% Africa-only vs 46.5% outside-Africa-only.</p></div>
          <div class="callout"><strong>First and corresponding authorship</strong><p class="muted">Outside-African affiliations are more common in first and corresponding-author positions.</p></div>
        </div>
        <p class="source-note">Denominator: 499 mixed Africa + outside-Africa papers.</p>
        '''
    )}

    {slide(
        "Bibliometric Impact",
        "OpenAlex profile indicators are descriptively higher in the outside-African affiliation stratum.",
        f'''
        {impact_cards(impact)}
        <p class="claim" style="margin-top:28px">These are cumulative database-recorded indicators, not measures of intrinsic research quality or individual contribution.</p>
        '''
    )}

    {slide(
        "Metadata Coverage",
        "The analytical table is strong on core identifiers and paper metadata, with expected gaps in source-specific fields.",
        f'''
        {coverage_grid(coverage)}
        <p class="source-note">Coverage denominator: {summary["author_paper_records"]:,} author-paper records. Missing-value sentinels were treated as absent.</p>
        '''
    )}

    {slide(
        "Interpretation",
        "The findings identify monitoring targets, not causal claims.",
        '''
        <ul class="big-list">
          <li>The corpus contains substantial Africa-only production as well as extensive international collaboration.</li>
          <li>Authorship position should be treated as a leadership signal, not a full contribution measure.</li>
          <li>H-index, citations and works counts reflect cumulative scholarly profiles and database coverage.</li>
          <li>The current classification uses publication-time affiliation evidence, not nationality or study location.</li>
        </ul>
        '''
    )}

    {slide(
        "Next Steps",
        "Scopus and Google Scholar are the most important metadata expansions for the next run.",
        '''
        <div class="step-grid">
          <div class="step"><strong>1. Enable Scopus enrichment</strong><p>Use Scopus identifiers, affiliation history and citation metadata to strengthen author disambiguation and impact comparisons.</p></div>
          <div class="step"><strong>2. Add Google Scholar checks</strong><p>Use targeted Scholar validation for profiles that are missing or ambiguous in OpenAlex/Semantic Scholar.</p></div>
          <div class="step"><strong>3. Validate authorship roles</strong><p>Manually audit a stratified sample of first, last and corresponding-author assignments against publisher full text.</p></div>
          <div class="step"><strong>4. Add study-location variables</strong><p>Separate affiliation geography from study site, data origin and population geography before making equity interpretations.</p></div>
        </div>
        '''
    )}

    {slide(
        "Decision Agenda",
        "The next meeting should move from descriptive findings to validation and publication strategy.",
        '''
        <div class="two-col">
          <ul class="big-list">
            <li>Confirm final author list, affiliations and corresponding author.</li>
            <li>Decide whether Scopus/Google Scholar expansion is required before submission.</li>
            <li>Select the manual-validation sample and reviewer assignments.</li>
            <li>Define the manuscript target journal or conference format.</li>
          </ul>
          <div class="callout">
            <p class="claim"><strong>Recommended position:</strong> submit current results as a reproducible closed-corpus baseline, while framing Scopus and Google Scholar as the next validation layer.</p>
          </div>
        </div>
        '''
    )}
  </main>
  <div class="nav">
    <button onclick="prevSlide()">Prev</button>
    <span id="counter"></span>
    <button onclick="nextSlide()">Next</button>
  </div>
  <script>
    const slides = Array.from(document.querySelectorAll('.slide'));
    let current = 0;
    function showSlide(index) {{
      current = Math.max(0, Math.min(slides.length - 1, index));
      slides.forEach((slide, i) => slide.classList.toggle('active', i === current));
      document.getElementById('counter').textContent = `${{current + 1}} / ${{slides.length}}`;
      location.hash = `slide-${{current + 1}}`;
    }}
    function nextSlide() {{ showSlide(current + 1); }}
    function prevSlide() {{ showSlide(current - 1); }}
    document.addEventListener('keydown', (event) => {{
      if (['ArrowRight', 'PageDown', ' '].includes(event.key)) nextSlide();
      if (['ArrowLeft', 'PageUp', 'Backspace'].includes(event.key)) prevSlide();
    }});
    const match = location.hash.match(/slide-(\\d+)/);
    showSlide(match ? Number(match[1]) - 1 : 0);
  </script>
</body>
</html>
"""
    return html_doc


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    html_doc = "\n".join(line.rstrip() for line in build_html().splitlines()) + "\n"
    OUTPUT_PATH.write_text(html_doc, encoding="utf-8")
    print(f"HTML presentation built: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
