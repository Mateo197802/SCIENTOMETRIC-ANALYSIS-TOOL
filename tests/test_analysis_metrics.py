import pandas as pd

from src.analysis.metrics import (
    add_analysis_columns,
    analysis_summary,
    build_author_key,
    classify_affiliation_region,
    collaboration_summary,
    country_impact_summary,
    country_summary,
    field_coverage,
    gender_role_summary,
    impact_summary,
    mixed_country_leadership_summary,
    mixed_leadership_summary,
    profile_summary,
)


def _row(
    doi: str,
    name: str,
    country: str,
    position: str,
    corresponding: bool = False,
    author_id: str = "No data",
    profile: str = "COMPUTER_SCIENCE | Unknown",
    gender: str = "Unknown",
    hindex: int = 1,
) -> dict[str, object]:
    return {
        "DOI": doi,
        "AUTHOR_NAME": name,
        "AUTHOR_ID_OA": author_id,
        "GEO_COUNTRY_OA": country,
        "AUTHOR_POS_OA": position,
        "IS_CORRESPONDING_OA": corresponding,
        "PROFILE_CLASSIFICATION": profile,
        "GENDER": gender,
        "HINDEX_OA": hindex,
        "CITATIONS_OA": 2,
        "WORKS_COUNT_OA": 3,
    }


def test_classify_affiliation_region():
    assert classify_affiliation_region("NG") == "Africa"
    assert classify_affiliation_region("us") == "Outside Africa"
    assert classify_affiliation_region("UNKNOWN") == "Unknown"
    assert classify_affiliation_region(None) == "Unknown"


def test_build_author_key_keeps_fallback_authors_distinct():
    first = pd.Series(
        {"AUTHOR_ID_OA": "PubMed_Fallback", "AUTHOR_NAME": "Ada N. Example"}
    )
    second = pd.Series(
        {"AUTHOR_ID_OA": "PubMed_Fallback", "AUTHOR_NAME": "Bola Example"}
    )

    assert build_author_key(first) == "name:adanexample"
    assert build_author_key(second) == "name:bolaexample"
    assert build_author_key(first) != build_author_key(second)


def test_collaboration_summary_classifies_papers_from_known_affiliations():
    raw = pd.DataFrame(
        [
            _row("10.1/mixed", "A", "NG", "first"),
            _row("10.1/mixed", "B", "US", "last"),
            _row("10.1/africa", "C", "NG", "first"),
            _row("10.1/africa", "D", "GH", "last"),
            _row("10.1/outside", "E", "US", "first"),
            _row("10.1/outside", "F", "GB", "last"),
        ]
    )

    summary = collaboration_summary(add_analysis_columns(raw))

    assert summary.set_index("CATEGORY")["PAPERS"].to_dict() == {
        "Africa-only known affiliations": 1,
        "Mixed Africa + outside": 1,
        "No African affiliation detected": 1,
    }
    assert summary["PERCENT"].sum() == 100.0


def test_mixed_leadership_uses_paper_denominators_and_tracks_both_regions():
    raw = pd.DataFrame(
        [
            _row("10.1/one", "A", "NG", "first", True),
            _row("10.1/one", "B", "US", "middle"),
            _row("10.1/one", "C", "US", "last", True),
            _row("10.1/one", "Extra", "US", "middle"),
            _row("10.1/two", "D", "US", "first", True),
            _row("10.1/two", "E", "NG", "middle"),
            _row("10.1/two", "F", "NG", "last"),
        ]
    )

    summary = mixed_leadership_summary(add_analysis_columns(raw))
    pivot = summary.pivot(index="ROLE", columns="LEADERSHIP_REGION", values="PAPERS")

    assert pivot.loc["First author"].to_dict() == {
        "Africa only": 1,
        "Both regions": 0,
        "Outside Africa only": 1,
        "Unknown only": 0,
    }
    assert pivot.loc["Last author"].to_dict() == {
        "Africa only": 1,
        "Both regions": 0,
        "Outside Africa only": 1,
        "Unknown only": 0,
    }
    assert pivot.loc["Corresponding author"].to_dict() == {
        "Africa only": 0,
        "Both regions": 1,
        "Outside Africa only": 1,
        "Unknown only": 0,
    }
    assert summary.groupby("ROLE")["PERCENT"].sum().round(8).eq(100.0).all()


def test_impact_summary_deduplicates_author_within_affiliation_region():
    raw = pd.DataFrame(
        [
            _row("10.1/a", "Ada", "NG", "first", author_id="A1", hindex=5),
            _row("10.1/b", "Ada", "NG", "last", author_id="A1", hindex=5),
            _row("10.1/c", "Bola", "NG", "first", author_id="A2", hindex=15),
            _row("10.1/d", "Chris", "US", "first", author_id="A3", hindex=30),
        ]
    )

    summary = impact_summary(add_analysis_columns(raw)).set_index(
        "AFFILIATION_REGION"
    )

    assert summary.loc["Africa", "AUTHORS"] == 2
    assert summary.loc["Africa", "HINDEX_MEDIAN"] == 10.0
    assert summary.loc["Outside Africa", "AUTHORS"] == 1


def test_profile_summary_counts_each_author_once_per_region():
    raw = pd.DataFrame(
        [
            _row(
                "10.1/a",
                "Ada",
                "NG",
                "first",
                author_id="A1",
                profile="CLINICAL | Female",
            ),
            _row(
                "10.1/b",
                "Ada",
                "NG",
                "last",
                author_id="A1",
                profile="CLINICAL | Female",
            ),
            _row(
                "10.1/c",
                "Bola",
                "NG",
                "first",
                author_id="A2",
                profile="COMPUTER_SCIENCE | Male",
            ),
        ]
    )

    summary = profile_summary(add_analysis_columns(raw)).set_index("BASE_PROFILE")

    assert summary.loc["CLINICAL", "AUTHORS"] == 1
    assert summary.loc["COMPUTER_SCIENCE", "AUTHORS"] == 1
    assert summary["PERCENT"].sum() == 100.0


def test_gender_role_summary_excludes_unknown_inference():
    raw = pd.DataFrame(
        [
            _row("10.1/a", "Ada", "NG", "first", gender="Female"),
            _row("10.1/a", "Bola", "NG", "last", gender="Male"),
            _row("10.1/a", "Unknown", "NG", "middle", gender="Unknown"),
        ]
    )

    summary = gender_role_summary(add_analysis_columns(raw))
    africa_all = summary[
        summary["AFFILIATION_REGION"].eq("Africa")
        & summary["ROLE"].eq("All author-paper records")
    ].iloc[0]

    assert africa_all["KNOWN_GENDER_RECORDS"] == 2
    assert africa_all["FEMALE_PERCENT"] == 50.0


def test_country_summary_counts_distinct_papers_and_author_keys():
    raw = pd.DataFrame(
        [
            _row("10.1/a", "Ada", "NG", "first", author_id="A1"),
            _row("10.1/a", "Bola", "NG", "last", author_id="A2"),
            _row("10.1/b", "Ada", "NG", "first", author_id="A1"),
        ]
    )

    summary = country_summary(add_analysis_columns(raw), min_papers=1).iloc[0]

    assert summary["PAPERS"] == 2
    assert summary["AUTHOR_PAPER_RECORDS"] == 3
    assert summary["DISTINCT_AUTHOR_KEYS"] == 2


def test_field_coverage_treats_pipeline_sentinels_as_missing():
    raw = pd.DataFrame(
        [
            _row("10.1/a", "Ada", "NG", "first"),
            _row("10.1/b", "Bola", "NG", "last"),
        ]
    )
    raw["ORCID"] = ["0000-0001", "No data"]

    coverage = field_coverage(add_analysis_columns(raw)).set_index("FIELD")

    assert coverage.loc["ORCID", "POPULATED_RECORDS"] == 1
    assert coverage.loc["ORCID", "COVERAGE_PERCENT"] == 50.0


def test_analysis_summary_uses_doi_and_valid_openalex_id_counts():
    input_df = pd.DataFrame({"DOI": ["10.1/a", "10.1/b"]})
    raw = pd.DataFrame(
        [
            _row("10.1/a", "Ada", "NG", "first", author_id="A1"),
            _row("10.1/a", "Fallback", "US", "last", author_id="PubMed_Fallback"),
            _row("10.1/b", "Bola", "NG", "first", author_id="A2"),
        ]
    )

    summary = analysis_summary(input_df, add_analysis_columns(raw))

    assert summary["input_dois"] == 2
    assert summary["output_dois"] == 2
    assert summary["author_paper_records"] == 3
    assert summary["distinct_openalex_author_ids"] == 2


def test_country_impact_summary_deduplicates_author_country_observations():
    raw = pd.DataFrame(
        [
            _row("10.1/a", "Ada", "NG", "first", author_id="A1", hindex=4),
            _row("10.1/b", "Ada", "NG", "last", author_id="A1", hindex=7),
            _row("10.1/c", "Bola", "NG", "first", author_id="A2", hindex=11),
        ]
    )

    summary = country_impact_summary(
        add_analysis_columns(raw),
        countries_per_region=1,
        min_authors=1,
    ).iloc[0]

    assert summary["COUNTRY"] == "NG"
    assert summary["AUTHORS"] == 2
    assert summary["HINDEX_MEDIAN"] == 9.0
    assert bool(summary["SELECTED_FOR_FIGURE"])


def test_country_impact_summary_selects_by_sample_size_within_region():
    raw = pd.DataFrame(
        [
            _row("10.1/a", "A", "NG", "first", author_id="NG1", hindex=4),
            _row("10.1/b", "B", "NG", "last", author_id="NG2", hindex=6),
            _row("10.1/c", "C", "GH", "first", author_id="GH1", hindex=80),
            _row("10.1/d", "D", "US", "first", author_id="US1", hindex=10),
            _row("10.1/e", "E", "US", "last", author_id="US2", hindex=12),
            _row("10.1/f", "F", "GB", "first", author_id="GB1", hindex=90),
        ]
    )

    summary = country_impact_summary(
        add_analysis_columns(raw),
        countries_per_region=1,
        min_authors=1,
    )
    selected = set(summary.loc[summary["SELECTED_FOR_FIGURE"], "COUNTRY"])

    assert selected == {"NG", "US"}


def test_mixed_country_leadership_uses_country_specific_doi_denominators():
    raw = pd.DataFrame(
        [
            _row("10.1/one", "A", "NG", "first", True, author_id="A1"),
            _row("10.1/one", "B", "US", "last", author_id="B1"),
            _row("10.1/two", "C", "NG", "middle", author_id="C1"),
            _row("10.1/two", "D", "US", "first", True, author_id="D1"),
            _row("10.1/two", "E", "US", "last", author_id="E1"),
            _row("10.1/three", "F", "GH", "first", True, author_id="F1"),
            _row("10.1/three", "G", "GH", "last", author_id="G1"),
            _row("10.1/three", "H", "US", "middle", author_id="H1"),
        ]
    )

    summary = mixed_country_leadership_summary(
        add_analysis_columns(raw),
        country_limit=2,
        min_mixed_papers=1,
    ).set_index("COUNTRY")

    assert summary.loc["NG", "MIXED_PAPERS"] == 2
    assert summary.loc["NG", "FIRST_AUTHOR_PAPERS"] == 1
    assert summary.loc["NG", "FIRST_AUTHOR_PERCENT"] == 50.0
    assert summary.loc["NG", "LAST_AUTHOR_PERCENT"] == 0.0
    assert summary.loc["NG", "CORRESPONDING_AUTHOR_PERCENT"] == 50.0


def test_mixed_country_leadership_selects_by_mixed_paper_volume():
    raw = pd.DataFrame(
        [
            _row("10.1/one", "A", "NG", "middle", author_id="A1"),
            _row("10.1/one", "B", "US", "first", True, author_id="B1"),
            _row("10.1/one", "C", "US", "last", author_id="C1"),
            _row("10.1/two", "D", "NG", "middle", author_id="D1"),
            _row("10.1/two", "E", "US", "first", True, author_id="E1"),
            _row("10.1/two", "F", "US", "last", author_id="F1"),
            _row("10.1/three", "G", "GH", "first", True, author_id="G1"),
            _row("10.1/three", "H", "GH", "last", author_id="H1"),
            _row("10.1/three", "I", "US", "middle", author_id="I1"),
        ]
    )

    summary = mixed_country_leadership_summary(
        add_analysis_columns(raw),
        country_limit=1,
        min_mixed_papers=1,
    )
    selected = summary.loc[summary["SELECTED_FOR_FIGURE"]].iloc[0]

    assert selected["COUNTRY"] == "NG"
    assert selected["MIXED_PAPERS"] == 2
    assert selected["FIRST_AUTHOR_PERCENT"] == 0.0
