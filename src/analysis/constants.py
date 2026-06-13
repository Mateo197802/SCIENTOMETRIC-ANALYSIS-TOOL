"""Shared constants for the scientometric analysis package."""

AFRICAN_COUNTRY_CODES = frozenset(
    """
    DZ AO BJ BW BF BI CV CM CF TD KM CD CG CI DJ EG GQ ER SZ ET GA GM GH GN
    GW KE LS LR LY MG MW ML MR MU MA MZ NA NE NG RW ST SN SC SL SO ZA SS SD
    TZ TG TN UG ZM ZW EH
    """.split()
)

MISSING_SENTINELS = frozenset(
    {
        "",
        "N/A",
        "NAN",
        "NO DATA",
        "NONE",
        "NOT FOUND",
        "NOT_FOUND_IN_PM",
        "NOT_FOUND_IN_SC",
        "NOT_FOUND_IN_SS",
        "NO_ORCID",
        "NO_ORCID_SS",
        "SKIP",
        "UNKNOWN",
    }
)

EXPECTED_MASTER_COLUMNS = (
    "PAPER_TITLE",
    "DOI",
    "YEAR",
    "OPEN_ACCESS_OA",
    "FUNDING_OA",
    "AUTHOR_NAME",
    "AUTHOR_POS_OA",
    "IS_CORRESPONDING_OA",
    "AFFILIATION_OA",
    "GEO_COUNTRY_OA",
    "AUTHOR_ID_OA",
    "WORKS_COUNT_OA",
    "CITATIONS_OA",
    "HINDEX_OA",
    "I10INDEX_OA",
    "2YR_MEAN_OA",
    "TOPICS_OA",
    "PRIMARY_TOPIC_OA",
    "KEYWORDS_OA",
    "PMID_PM",
    "MESH_PM",
    "FUNDING_PM",
    "AUTHOR_NAME_PM",
    "AFFILIATION_PM",
    "INFLUENTIAL_CITATIONS_SS",
    "CITATION_CONTEXTS_SS",
    "AUTHOR_ID_SS",
    "AUTHOR_NAME_SS",
    "ORCID_SS",
    "HINDEX_SS",
    "CITATIONS_SS",
    "ORCID",
    "ORCID_EMPLOYMENT",
    "GENDER",
    "PROFILE_CLASSIFICATION",
)
