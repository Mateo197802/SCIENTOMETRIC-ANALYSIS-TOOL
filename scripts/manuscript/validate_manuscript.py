"""Validate numerical, citation, and terminology consistency in the manuscript."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
MANUSCRIPT_PATH = BASE_DIR / "manuscript" / "text" / "manuscript.md"
SUPPLEMENT_PATH = BASE_DIR / "manuscript" / "text" / "supplement.md"
REFERENCE_PATH = (
    BASE_DIR / "manuscript" / "references" / "references_vancouver.md"
)
TABLE_DIR = BASE_DIR / "manuscript" / "tables"

APPROVED_TITLE = (
    "Geographic Patterns of Scientific Leadership and Bibliometric Impact "
    "in the ML4Africa Research Corpus"
)

PROHIBITED = [
    "all African machine learning for health research",
    "systematic review of the ML4Africa corpus",
    "country of origin",
    "nationality was defined",
    "parachute research index",
    "proves that",
    "caused by",
]

EXPECTED_PLACEHOLDERS = {
    "FIGURE:1",
    "FIGURE:2",
    "FIGURE:3",
    "FIGURE:4",
    "FIGURE:5",
    "TABLE:1",
    "TABLE:2",
    "TABLE:3",
    "REFERENCES",
    "SUPPLEMENT",
}

EXPECTED_SUPPLEMENTARY_PLACEHOLDERS = {
    f"SUPPLEMENTARY_TABLE:S{index}" for index in range(1, 9)
}


def _citation_numbers(text: str) -> list[int]:
    numbers: list[int] = []
    for match in re.finditer(r"\[([0-9,\- ]+)\]", text):
        for part in match.group(1).split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                start, end = (int(value) for value in part.split("-", 1))
                numbers.extend(range(start, end + 1))
            else:
                numbers.append(int(part))
    return numbers


def _first_appearance(numbers: list[int]) -> list[int]:
    seen: list[int] = []
    for number in numbers:
        if number not in seen:
            seen.append(number)
    return seen


def _extract_placeholders(text: str) -> set[str]:
    return set(re.findall(r"\{\{([^{}]+)\}\}", text))


def _validate_numeric_traceability(manuscript: str) -> None:
    table_1 = pd.read_csv(TABLE_DIR / "table_1_corpus_characteristics.csv")
    table_2 = pd.read_csv(TABLE_DIR / "table_2_collaboration_leadership.csv")
    table_3 = pd.read_csv(TABLE_DIR / "table_3_bibliometric_impact.csv")

    corpus_values = dict(zip(table_1["MEASURE"], table_1["VALUE"]))
    required_counts = {
        "1,158": int(corpus_values["Input DOI values"]),
        "7,361": int(corpus_values["Author-paper records"]),
        "5,675": int(corpus_values["Distinct OpenAlex author IDs"]),
    }
    for rendered, numeric in required_counts.items():
        assert f"{numeric:,}" == rendered
        assert rendered in manuscript

    collaboration = table_2[
        table_2["OUTCOME"].eq("Collaboration composition")
    ]
    for row in collaboration.itertuples(index=False):
        assert f"{int(row.PAPERS)} ({float(row.PERCENT):.1f}%)" in manuscript

    leadership = table_2[
        table_2["OUTCOME"].eq("Leadership in mixed collaborations")
    ]
    required_leadership = {
        ("First author", "Africa only"),
        ("First author", "Outside Africa only"),
        ("Last author", "Africa only"),
        ("Last author", "Outside Africa only"),
        ("Corresponding author", "Africa only"),
        ("Corresponding author", "Outside Africa only"),
        ("Corresponding author", "Both regions"),
    }
    for row in leadership.itertuples(index=False):
        if (row.ROLE, row.CATEGORY) in required_leadership:
            assert f"{float(row.PERCENT):.1f}%" in manuscript

    for row in table_3.itertuples(index=False):
        assert f"{int(row.AUTHORS):,}" in manuscript
        low, high = row.HINDEX_IQR.split("-")
        iqr = f"IQR, {int(float(low))}-{int(float(high))}"
        assert f"{int(row.HINDEX_MEDIAN)} ({iqr})" in manuscript


def _validate_references(manuscript: str) -> None:
    references = [
        line.strip()
        for line in REFERENCE_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(references) == 20
    expected_prefixes = [f"{index}." for index in range(1, 21)]
    assert [
        reference.split(maxsplit=1)[0] for reference in references
    ] == expected_prefixes

    numbers = _citation_numbers(manuscript)
    assert set(numbers) == set(range(1, 21))
    assert _first_appearance(numbers) == list(range(1, 21))


def validate_manuscript() -> None:
    manuscript = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    supplement = SUPPLEMENT_PATH.read_text(encoding="utf-8")

    assert manuscript.startswith(f"# {APPROVED_TITLE}")
    _validate_numeric_traceability(manuscript)
    _validate_references(manuscript)

    lowered = f"{manuscript}\n{supplement}".lower()
    for phrase in PROHIBITED:
        assert phrase.lower() not in lowered, f"Prohibited phrase: {phrase}"

    assert _extract_placeholders(manuscript) == EXPECTED_PLACEHOLDERS
    assert (
        _extract_placeholders(supplement)
        == EXPECTED_SUPPLEMENTARY_PLACEHOLDERS
    )
    assert manuscript.count("{{FIGURE:") == 5
    assert manuscript.count("{{TABLE:") == 3
    assert supplement.count("{{SUPPLEMENTARY_TABLE:") == 8

    assert "name-inferred" in supplement.lower()
    assert "llm-inferred" in supplement.lower()
    assert "not self-identified gender" in supplement.lower()
    assert "not ground truth" in supplement.lower()
    assert "Editorial completion required" in manuscript
    assert "TBD" not in manuscript
    assert "TODO" not in manuscript

    print("Manuscript validation passed")


def main() -> None:
    validate_manuscript()


if __name__ == "__main__":
    main()
