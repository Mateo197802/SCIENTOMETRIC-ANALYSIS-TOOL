from src.utils.author_matcher import is_same_author


def test_semantic_scholar_null_external_ids_is_not_a_match():
    openalex_author = {
        "ORCID": "No data",
        "RAW_SCOPUS_ID_OA": "No data",
    }
    semantic_author = {
        "authorId": "123",
        "name": "Example Author",
        "externalIds": None,
    }

    assert (
        is_same_author(
            openalex_author,
            semantic_author,
            api_type="semantic_scholar",
        )
        is False
    )
