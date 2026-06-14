import pandas as pd

from src.analysis.manuscript_metrics import (
    build_collaboration_leadership_table,
    build_corpus_table,
    build_impact_table,
    corpus_characteristics,
    publication_year_summary,
)


def test_publication_year_summary_uses_distinct_dois():
    data = pd.DataFrame(
        {
            "DOI_NORMALIZED": ["a", "a", "b", "c"],
            "YEAR": [2020, 2020, 2021, 2021],
        }
    )

    result = publication_year_summary(data)

    assert result.to_dict("records") == [
        {"YEAR": 2020, "PAPERS": 1},
        {"YEAR": 2021, "PAPERS": 2},
    ]


def test_publication_year_summary_excludes_missing_years():
    data = pd.DataFrame(
        {
            "DOI_NORMALIZED": ["a", "b", "c"],
            "YEAR": [2020, "No data", None],
        }
    )

    result = publication_year_summary(data)

    assert result.to_dict("records") == [{"YEAR": 2020, "PAPERS": 1}]


def test_corpus_characteristics_reports_units_without_conflation():
    input_df = pd.DataFrame({"DOI": ["a", "b"]})
    data = pd.DataFrame(
        {
            "DOI_NORMALIZED": ["a", "a", "b"],
            "YEAR": [2020, 2020, 2021],
            "AUTHOR_ID_OA": ["A1", "A2", "A1"],
            "AUTHOR_KEY": ["oa:A1", "oa:A2", "oa:A1"],
            "AFFILIATION_REGION": ["Africa", "Outside Africa", "Africa"],
        }
    )

    result = corpus_characteristics(input_df, data)
    values = dict(zip(result["METRIC"], result["VALUE"]))

    assert values["Input DOI values"] == 2
    assert values["Output DOI values"] == 2
    assert values["Author-paper records"] == 3
    assert values["Distinct OpenAlex author IDs"] == 2
    assert values["Observed minimum publication year"] == 2020
    assert values["Observed maximum publication year"] == 2021


def test_corpus_characteristics_excludes_fallback_author_ids():
    input_df = pd.DataFrame({"DOI": ["a"]})
    data = pd.DataFrame(
        {
            "DOI_NORMALIZED": ["a", "a", "a", "a"],
            "YEAR": [2020, 2020, 2020, 2020],
            "AUTHOR_ID_OA": [
                "A1",
                "PubMed_Fallback",
                "Semantic_Fallback",
                "No data",
            ],
            "AUTHOR_KEY": [
                "oa:A1",
                "name:second",
                "name:third",
                "name:fourth",
            ],
            "AFFILIATION_REGION": [
                "Africa",
                "Africa",
                "Outside Africa",
                "Unknown",
            ],
        }
    )

    result = corpus_characteristics(input_df, data)
    values = dict(zip(result["METRIC"], result["VALUE"]))

    assert values["Distinct OpenAlex author IDs"] == 1


def test_build_corpus_table_includes_selected_field_coverage():
    characteristics = pd.DataFrame(
        {
            "METRIC": ["Input DOI values", "Author-paper records"],
            "VALUE": [1158, 7361],
        }
    )
    coverage = pd.DataFrame(
        {
            "FIELD": ["AFFILIATION_OA", "GEO_COUNTRY_OA", "ORCID"],
            "POPULATED_RECORDS": [6664, 6353, 4928],
            "TOTAL_RECORDS": [7361, 7361, 7361],
            "COVERAGE_PERCENT": [90.5, 86.3, 66.9],
        }
    )

    result = build_corpus_table(characteristics, coverage)

    assert result.columns.tolist() == [
        "SECTION",
        "MEASURE",
        "VALUE",
        "DENOMINATOR",
        "PERCENT",
    ]
    assert result.loc[result["MEASURE"].eq("Affiliation country populated")].iloc[
        0
    ].to_dict() == {
        "SECTION": "Metadata coverage",
        "MEASURE": "Affiliation country populated",
        "VALUE": 6353,
        "DENOMINATOR": 7361,
        "PERCENT": 86.3,
    }


def test_build_collaboration_leadership_table_keeps_doi_denominators():
    collaboration = pd.DataFrame(
        {
            "CATEGORY": ["Mixed Africa + outside"],
            "PAPERS": [499],
            "PERCENT": [43.1],
        }
    )
    leadership = pd.DataFrame(
        {
            "ROLE": ["First author"],
            "LEADERSHIP_REGION": ["Africa only"],
            "PAPERS": [204],
            "PERCENT": [40.9],
            "MIXED_PAPERS": [499],
        }
    )

    result = build_collaboration_leadership_table(
        collaboration, leadership, total_papers=1158
    )

    assert result.to_dict("records") == [
        {
            "OUTCOME": "Collaboration composition",
            "ROLE": "All papers",
            "CATEGORY": "Mixed Africa + outside",
            "PAPERS": 499,
            "DENOMINATOR": 1158,
            "PERCENT": 43.1,
        },
        {
            "OUTCOME": "Leadership in mixed collaborations",
            "ROLE": "First author",
            "CATEGORY": "Africa only",
            "PAPERS": 204,
            "DENOMINATOR": 499,
            "PERCENT": 40.9,
        },
    ]


def test_build_impact_table_formats_median_and_interquartile_range():
    impact = pd.DataFrame(
        {
            "AFFILIATION_REGION": ["Africa"],
            "AUTHORS": [2663],
            "HINDEX_MEDIAN": [5.0],
            "HINDEX_Q1": [2.0],
            "HINDEX_Q3": [11.0],
            "CITATIONS_MEDIAN": [100.0],
            "WORKS_MEDIAN": [16.0],
        }
    )

    result = build_impact_table(impact)

    assert result.to_dict("records") == [
        {
            "AFFILIATION_REGION": "Africa",
            "AUTHORS": 2663,
            "HINDEX_MEDIAN": 5.0,
            "HINDEX_IQR": "2.0-11.0",
            "CITATIONS_MEDIAN": 100.0,
            "WORKS_MEDIAN": 16.0,
        }
    ]
