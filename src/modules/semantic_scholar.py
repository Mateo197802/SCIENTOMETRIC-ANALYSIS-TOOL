import requests
import unicodedata
import re
import time
import logging

logger = logging.getLogger(__name__)

def normalize_name(name):
    """
    Strips accents, lowercases, and removes non-alphabet characters
    to perform fuzzy matching across different data sources.
    """
    if not name: return ""
    name_nfd = unicodedata.normalize('NFD', name)
    name_no_accents = re.sub(r'[\u0300-\u036f]', '', name_nfd).lower()
    return re.sub(r'[^a-z]', '', name_no_accents)

def process_semantic_scholar(doi, current_authors, config):
    if not config.get("semanticActive"):
        for auth in current_authors:
            auth.update({
                "INFLUENTIAL_CITATIONS_SS": 0,
                "CITATION_CONTEXTS_SS": "No data",
                "AUTHOR_ID_SS": "N/A",
                "AUTHOR_NAME_SS": "SKIP",
                "ORCID_SS": "NO_ORCID_SS",
                "HINDEX_SS": 0,
                "CITATIONS_SS": 0
            })
        return current_authors

    logger.info(f"[SemanticScholar] Fetching data for {doi}...")
    headers = {"x-api-key": config.get("semanticKey")}
    
    infl_citations = 0
    citation_contexts = "N/A"
    ss_authors = []
    
    try:
        url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
        params = {
            "fields": "title,year,authors.name,authors.authorId,authors.hIndex,authors.citationCount,influentialCitationCount,authors.externalIds"
        }
        
        res = requests.get(url, params=params, headers=headers, timeout=10)
        res.raise_for_status()
        ss_paper = res.json()
        
        infl_citations = ss_paper.get("influentialCitationCount", 0)
        ss_authors = ss_paper.get("authors", [])
    except Exception as e:
        logger.debug(f"[SemanticScholar] Search Error: {e}")

    # Match authors found in previous steps against Semantic Scholar records
    final_rows = []
    for auth in current_authors:
        author_name_norm = normalize_name(auth.get("AUTHOR_NAME", ""))
        
        match_ss = None
        if author_name_norm:
            for ss in ss_authors:
                ss_name_norm = normalize_name(ss.get("name", ""))
                if not ss_name_norm: continue
                # Checking for inclusion (e.g. "John Doe" in "John Doe Smith")
                if ss_name_norm in author_name_norm or author_name_norm in ss_name_norm:
                    match_ss = ss
                    break
        
        orcid_ss = "NO_ORCID_SS"
        if match_ss and match_ss.get("externalIds") and match_ss["externalIds"].get("ORCID"):
            orcid_ss = match_ss["externalIds"]["ORCID"]
            
        auth.update({
            "INFLUENTIAL_CITATIONS_SS": infl_citations,
            "CITATION_CONTEXTS_SS": citation_contexts,
            "AUTHOR_ID_SS": match_ss.get("authorId", "NO_ID_SS") if match_ss else "NOT_FOUND_IN_SS",
            "AUTHOR_NAME_SS": match_ss.get("name", "NOT_FOUND_IN_SS") if match_ss else "NOT_FOUND_IN_SS",
            "ORCID_SS": orcid_ss,
            "HINDEX_SS": match_ss.get("hIndex", 0) if match_ss else 0,
            "CITATIONS_SS": match_ss.get("citationCount", 0) if match_ss else 0
        })
        final_rows.append(auth)
        
    # Process "Ghost Authors" only found in Semantic Scholar
    base_data = current_authors[0] if current_authors else {}
    for ss in ss_authors:
        if not ss.get("name") or not ss["name"].strip(): continue
        ss_name_norm = normalize_name(ss["name"])
        
        exists = False
        for auth in current_authors:
            auth_name_norm = normalize_name(auth.get("AUTHOR_NAME", ""))
            if not auth_name_norm: continue
            if auth_name_norm in ss_name_norm or ss_name_norm in auth_name_norm:
                exists = True
                break
                
        if not exists:
            orcid_ss = "NO_ORCID_SS"
            if ss.get("externalIds") and ss["externalIds"].get("ORCID"):
                orcid_ss = ss["externalIds"]["ORCID"]
                
            ghost = {
                "PAPER_TITLE": base_data.get("PAPER_TITLE", "No Title"),
                "DOI": base_data.get("DOI", doi),
                "YEAR": base_data.get("YEAR", "n/d"),
                "AUTHOR_NAME": ss.get("name"),
                "AUTHOR_POS_OA": "Unknown",
                "IS_CORRESPONDING_OA": False,
                "AUTHOR_ID_OA": "Semantic_Fallback",
                "ORCID": "NO_ORCID",
                "OPEN_ACCESS_OA": False,
                "FUNDING_OA": "No data",
                "AFFILIATION_OA": "MISSING_IN_OA",
                "GEO_COUNTRY_OA": "UNKNOWN",
                "WORKS_COUNT_OA": 0,
                "CITATIONS_OA": 0,
                "HINDEX_OA": 0,
                "I10INDEX_OA": 0,
                "2YR_MEAN_OA": 0.0,
                "KEYWORDS_OA": "No data",
                "PMID_PM": "N/A",
                "MESH_PM": "No data",
                "FUNDING_PM": "No data",
                "AUTHOR_NAME_PM": "SKIP",
                "AFFILIATION_PM": "N/A",
                "AUTHOR_ID_SC": "N/A",
                "AUTHOR_NAME_SC": "SKIP",
                "AFFILIATION_SC": "N/A",
                "FUNDING_SC": "No data",
                
                "INFLUENTIAL_CITATIONS_SS": infl_citations,
                "CITATION_CONTEXTS_SS": citation_contexts,
                "AUTHOR_ID_SS": ss.get("authorId", "NO_ID_SS"),
                "AUTHOR_NAME_SS": ss.get("name"),
                "ORCID_SS": orcid_ss,
                "HINDEX_SS": ss.get("hIndex", 0),
                "CITATIONS_SS": ss.get("citationCount", 0)
            }
            final_rows.append(ghost)
            
    return final_rows
